#!/usr/bin/env python3
"""Build peer-system rows in data/observations.csv from per-system input files.

Each file data/peers/<system_id>.csv has the same columns as observations.csv
and holds that system's hand-entered rows: `reported` values copied from
sources, and `estimated` values with a method note and a low-high range.

This script:
  1. Adds the standard ratio rows (method `peer_unit_ratios`) for every
     system, year and scope where the inputs exist. A ratio is made only when
     exactly one row exists for each input metric in that system, year and
     scope. If any input is `estimated`, the ratio is `estimated` too and its
     low and high values come from the inputs' ranges.
  2. Adds a PPP row (method `ppp_usd_2024`, obs_id suffix `_ppp24`) for every
     money row, reported or derived, that is not already in 2024 PPP dollars.
  3. Rewrites every row of the systems that have a peer file, keeping all
     other rows of observations.csv as they are, and sorts the file.

Run from the repository root: python3 scripts/build_peers.py
Then run: python3 scripts/validate.py
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OBS = ROOT / "data" / "observations.csv"
PEERS = ROOT / "data" / "peers"
FACTORS = ROOT / "data" / "raw" / "ppp" / "ppp_deflator.csv"
BASE_YEAR = 2024

FIELDNAMES = ["obs_id", "system_id", "year", "year_basis", "metric_id", "value",
              "value_low", "value_high", "unit", "currency", "price_basis", "scope",
              "value_type", "verification", "source_id", "source_locator",
              "method_id", "inputs", "notes"]

COUNTRY_ISO3 = {
    "United States": "USA", "United Kingdom": "GBR", "France": "FRA",
    "Spain": "ESP", "Germany": "DEU", "Turkey": "TUR", "Japan": "JPN",
    "South Korea": "KOR", "China": "CHN", "Singapore": "SGP",
}
CURRENCY_ISO3 = {"USD": "USA", "GBP": "GBR", "TRY": "TUR", "JPY": "JPN",
                 "KRW": "KOR", "CNY": "CHN", "HKD": "HKG", "SGD": "SGP"}
EURO_SYSTEMS_ISO3 = {"France": "FRA", "Spain": "ESP", "Germany": "DEU"}

# metric -> (numerator metric, denominator metric, multiplier, unit template)
# {c} in the unit is replaced by the money currency.
RATIOS = {
    "opex_per_car_km": ("opex_total", "car_km", 1, "{c}/car-km"),
    "opex_per_train_km": ("opex_total", "train_km", 1, "{c}/train-km"),
    "opex_per_passenger_km": ("opex_total", "passenger_km", 1, "{c}/passenger-km"),
    "opex_per_trip": ("opex_total", "unlinked_trips", 1, "{c}/trip"),
    "farebox_recovery": ("fare_revenue", "opex_total", 1, "ratio"),
    "avg_trip_length_km": ("passenger_km", "unlinked_trips", 1, "km"),
    "avg_car_load": ("passenger_km", "car_km", 1, "passengers"),
    "avg_cars_per_train": ("car_km", "train_km", 1, "cars"),
    "employees_per_million_car_km": ("employees_fte", "car_km", 1e6, "employees/million km"),
    "passenger_km_per_employee": ("passenger_km", "employees_fte", 1, "km/employee"),
    "trips_per_employee": ("unlinked_trips", "employees_fte", 1, "trips/employee"),
}
MONEY_RATIOS = {"opex_per_car_km", "opex_per_train_km", "opex_per_passenger_km", "opex_per_trip"}


def fmt(x):
    """Six significant figures, or a whole number for large values."""
    if x is None:
        return ""
    if abs(x) >= 1e5:
        return str(int(round(x)))
    return f"{x:.6g}"


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(s):
    return float(s) if s not in (None, "") else None


def ratio_row(metric, num_row, den_row):
    numer, denom, mult, unit_t = RATIOS[metric]
    n, d = float(num_row["value"]), float(den_row["value"])
    value = n / d * mult
    estimated = "estimated" in (num_row["value_type"], den_row["value_type"])
    low = high = None
    if estimated:
        n_lo = num(num_row["value_low"]) or n
        n_hi = num(num_row["value_high"]) or n
        d_lo = num(den_row["value_low"]) or d
        d_hi = num(den_row["value_high"]) or d
        low, high = n_lo / d_hi * mult, n_hi / d_lo * mult
    money_row = num_row if num_row["currency"] else den_row
    currency = money_row["currency"] if metric in MONEY_RATIOS else ""
    price_basis = money_row["price_basis"] if metric in MONEY_RATIOS else ""
    sid = num_row["system_id"]
    tag = num_row["obs_id"].rsplit("_", 1)[-1]
    return {
        "obs_id": f"{sid}_{num_row['year']}_{metric}_{tag}",
        "system_id": sid, "year": num_row["year"], "year_basis": num_row["year_basis"],
        "metric_id": metric, "value": fmt(value), "value_low": fmt(low), "value_high": fmt(high),
        "unit": unit_t.format(c=currency), "currency": currency, "price_basis": price_basis,
        "scope": num_row["scope"],
        "value_type": "estimated" if estimated else "derived",
        "verification": "unverified",
        "source_id": num_row["source_id"],
        "source_locator": "Computed from the input rows listed in inputs",
        "method_id": "peer_unit_ratios",
        "inputs": f"{num_row['obs_id']};{den_row['obs_id']}",
        "notes": "Inherits the estimate flag and range from its inputs." if estimated else "",
    }


def ppp_row(row, iso3, factors):
    year = int(row["year"])
    ppp_id = f"ppp_{iso3.lower()}_{year}"
    d_id, d_base = f"us_gdp_deflator_{year}", f"us_gdp_deflator_{BASE_YEAR}"
    missing = [f for f in (ppp_id, d_id, d_base) if f not in factors]
    if missing:
        print(f"  skip PPP for {row['obs_id']}: no factor {missing}", file=sys.stderr)
        return None
    k = factors[d_base] / factors[d_id] / factors[ppp_id]
    conv = lambda s: fmt(float(s) * k) if s else ""
    out = dict(row)
    out.update({
        "obs_id": row["obs_id"] + "_ppp24",
        "value": conv(row["value"]), "value_low": conv(row["value_low"]),
        "value_high": conv(row["value_high"]),
        "unit": row["unit"].replace(row["currency"], "USD", 1) if row["currency"] else row["unit"],
        "currency": "USD", "price_basis": f"PPP_USD_{BASE_YEAR}",
        "value_type": "estimated" if row["value_type"] == "estimated" else "derived",
        "verification": "unverified",
        "source_locator": "Computed from the input row and price factors listed in inputs",
        "method_id": "ppp_usd_2024",
        "inputs": f"{row['obs_id']};{ppp_id};{d_id};{d_base}",
        "notes": "Inherits the estimate flag and range from its input." if row["value_type"] == "estimated" else "",
    })
    return out


def main():
    systems = {r["system_id"]: r for r in read_csv(ROOT / "data" / "systems.csv")}
    factors = {r["factor_id"]: float(r["value"]) for r in read_csv(FACTORS)}
    peer_files = sorted(PEERS.glob("*.csv"))
    managed = {p.stem for p in peer_files}
    new_rows = []
    for p in peer_files:
        rows = read_csv(p)
        sid = p.stem
        if sid not in systems:
            sys.exit(f"{p}: {sid} is not in data/systems.csv")
        for r in rows:
            if r["system_id"] != sid:
                sys.exit(f"{p}: row {r['obs_id']} has system_id {r['system_id']}")
        country = systems[sid]["country"]
        derived = []
        groups = defaultdict(lambda: defaultdict(list))
        for r in rows:
            groups[(r["year"], r["scope"])][r["metric_id"]].append(r)
        for (year, scope), by_metric in sorted(groups.items()):
            for metric, (numer, denom, _, _) in RATIOS.items():
                if by_metric.get(metric):
                    continue  # entered by hand
                ns, ds = by_metric.get(numer, []), by_metric.get(denom, [])
                if len(ns) == 1 and len(ds) == 1:
                    derived.append(ratio_row(metric, ns[0], ds[0]))
        all_rows = rows + derived
        ppp = []
        for r in all_rows:
            cur = r["currency"]
            if not cur or r["price_basis"] != "nominal" or r["metric_id"] == "farebox_recovery":
                continue
            if cur == "EUR":
                iso3 = EURO_SYSTEMS_ISO3.get(country)
            else:
                iso3 = CURRENCY_ISO3.get(cur)
            if not iso3:
                print(f"  skip PPP for {r['obs_id']}: unknown currency {cur}", file=sys.stderr)
                continue
            row = ppp_row(r, iso3, factors)
            if row:
                ppp.append(row)
        new_rows += all_rows + ppp
        print(f"{sid}: {len(rows)} input rows, {len(derived)} ratio rows, {len(ppp)} PPP rows")

    old = read_csv(OBS)
    new_ids = {r["obs_id"] for r in new_rows}
    dropped = [r["obs_id"] for r in old if r["system_id"] in managed and r["obs_id"] not in new_ids]
    for d in dropped:
        print(f"  removed row no longer in a peer file: {d}", file=sys.stderr)
    kept = [r for r in old if r["system_id"] not in managed]
    out = kept + [{k: r.get(k, "") for k in FIELDNAMES} for r in new_rows]
    out.sort(key=lambda r: (r["system_id"], int(r["year"]), r["metric_id"], r["obs_id"]))
    with open(OBS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} rows to {OBS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
