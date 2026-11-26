#!/usr/bin/env python3
"""Write data/peers/hong_kong_mtr.csv from the transcription in data/raw/asia/mtr_hk.py.

Three scopes, kept apart on purpose:
  hk_transport_operations_all  MTR's whole Hong Kong transport operations
      (heavy rail, Airport Express, Light Rail, buses, intercity trains and,
      from late 2018, the high-speed rail section). Reported P&L figures.
  hk_rail_excl_hsr_mtr_definition  MTR's own published unit costs for its
      Hong Kong rail network excluding high-speed rail.
  metro_only  Domestic plus Cross-boundary heavy-rail lines (the urban metro
      including East Rail). Cost and staff are ESTIMATES (see methods).
Run from the repository root, then scripts/build_peers.py and scripts/validate.py.
"""
import csv
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = runpy.run_path(str(ROOT / "data" / "raw" / "asia" / "mtr_hk.py"))
FIELDS = ["obs_id", "system_id", "year", "year_basis", "metric_id", "value",
          "value_low", "value_high", "unit", "currency", "price_basis", "scope",
          "value_type", "verification", "source_id", "source_locator",
          "method_id", "inputs", "notes"]
SID = "hong_kong_mtr"
TEN = "mtr_ar2025_ten_year_stats"
TEN_LOC = "Ten-Year Statistics, Hong Kong Transport Operations, row '{row}', column {y}"
ALL, RAIL, METRO = "hk_transport_operations_all", "hk_rail_excl_hsr_mtr_definition", "metro_only"
# Cost per car-km of Airport Express and Light Rail relative to heavy rail, for the range.
R_LOW, R_HIGH = 0.5, 2.0


def fmt(x):
    return str(int(round(x))) if abs(x) >= 1e5 else f"{x:.6g}"


def row(**k):
    r = {f: "" for f in FIELDS}
    r.update(system_id=SID, year_basis="calendar", verification="unverified")
    r.update(k)
    return r


def main():
    out = []
    ten = {k: dict(zip(D["YEARS"], v)) for k, v in D["TEN_YEAR"].items()}
    for y in sorted(D["YEARS"]):
        t = {k: v[y] for k, v in ten.items()}
        ids = {}

        def rep(metric, value, unit, scope, tag, src, loc, cur="", note=""):
            oid = f"{SID}_{y}_{metric}_{tag}"
            ids[(metric, scope)] = oid
            out.append(row(obs_id=oid, year=y, metric_id=metric, value=fmt(value), unit=unit,
                           currency=cur, price_basis="nominal" if cur else "", scope=scope,
                           value_type="reported", source_id=src, source_locator=loc, notes=note))
            return oid

        # --- whole Hong Kong transport operations (reported P&L)
        src, rev, staff_cost, total = D["PNL"][y]
        ploc = "Consolidated profit and loss account, page 2, '{}' ({} column; HK$ million, multiplied by 1,000,000)"
        rep("opex_total", total * 1e6, "HKD", ALL, "mtrall", src,
            ploc.format("Expenses relating to Hong Kong transport operations", y), "HKD",
            "Before depreciation and the variable annual payment to KCRC. Covers all Hong Kong transport operations, including buses, Light Rail, Airport Express, intercity and (from Sept 2018) high-speed rail.")
        rep("opex_staff_costs", staff_cost * 1e6, "HKD", ALL, "mtrall", src,
            ploc.format("Staff costs and related expenses", y), "HKD")
        rep("fare_revenue", rev * 1e6, "HKD", ALL, "mtrall", src,
            ploc.format("Revenue from Hong Kong transport operations", y), "HKD",
            "Total revenue of Hong Kong transport operations: fares of all services plus a small 'Others' line (under 1%).")
        rep("employees_fte", t["staff_hk_transport_operations"], "employees", ALL, "mtrall", TEN,
            TEN_LOC.format(row="Staff: Hong Kong - Transport Operations", y=y),
            note="Head count at year end of Hong Kong transport operations staff. Excludes corporate support, station commercial, capital works and property staff. Not FTE.")
        # --- MTR's own unit costs, rail excluding high-speed rail
        rep("opex_per_car_km", t["opex_per_car_km_hk_rail_excl_hsr"], "HKD/car-km", RAIL, "mtrrail", TEN,
            TEN_LOC.format(row="Hong Kong Transport Operations (excludes High Speed Rail): per car-km operated, operating costs (HK$)", y=y), "HKD",
            "MTR's published figure. Rounded to HK$0.1. Car-km of heavy rail, Airport Express and Light Rail. MTR does not list exactly which costs it leaves out besides high-speed rail.")
        rep("opex_per_trip", t["opex_per_passenger_hk_rail_excl_hsr"], "HKD/trip", RAIL, "mtrrail", TEN,
            TEN_LOC.format(row="Hong Kong Transport Operations (excludes High Speed Rail): per passenger carried, operating costs (HK$)", y=y), "HKD",
            "MTR's published figure per passenger carried. Not a boarding count: a journey across MTR lines counts once.")
        # --- metro only: Domestic + Cross-boundary heavy rail
        k_h = t["car_km_domestic_cross_boundary"] * 1000
        k_o = (t["car_km_airport_express"] + t["car_km_light_rail"]) * 1000
        ck = rep("car_km", k_h, "km", METRO, "mtr", TEN,
                 TEN_LOC.format(row="Car-km operated (thousand): Domestic and Cross-boundary", y=y) + " (thousand; multiplied by 1,000)")
        k_ae = rep("car_km", t["car_km_airport_express"] * 1000, "km", "airport_express_only", "mtrael", TEN,
                   TEN_LOC.format(row="Car-km operated (thousand): Airport Express", y=y) + " (thousand; multiplied by 1,000)")
        k_lr = rep("car_km", t["car_km_light_rail"] * 1000, "km", "light_rail_only", "mtrlr", TEN,
                   TEN_LOC.format(row="Car-km operated (thousand): Light Rail", y=y) + " (thousand; multiplied by 1,000)")
        p_d = rep("unlinked_trips", t["pax_domestic"] * 1000, "trips", "domestic_service_only", "mtrdom", TEN,
                  TEN_LOC.format(row="Total passengers (thousand): Domestic Service", y=y) + " (thousand; multiplied by 1,000)")
        p_c = rep("unlinked_trips", t["pax_cross_boundary"] * 1000, "trips", "cross_boundary_only", "mtrcb", TEN,
                  TEN_LOC.format(row="Total passengers (thousand): Cross-boundary Service", y=y) + " (thousand; multiplied by 1,000)")
        al = rep("avg_trip_length_km", t["avg_trip_km_domestic_cross_boundary"], "km", METRO, "mtr", TEN,
                 TEN_LOC.format(row="Average passenger km travelled: Domestic and Cross-boundary", y=y),
                 note="Rounded to 0.1 km in the source.")
        trips = (t["pax_domestic"] + t["pax_cross_boundary"]) * 1000
        tr = f"{SID}_{y}_unlinked_trips_mtr"
        out.append(row(obs_id=tr, year=y, metric_id="unlinked_trips", value=fmt(trips), unit="trips",
                       scope=METRO, value_type="derived", source_id=TEN,
                       source_locator="Computed from the input rows listed in inputs", method_id="hk_metro_derived",
                       inputs=f"{p_d};{p_c}",
                       notes="Domestic plus Cross-boundary passengers. A journey across MTR heavy-rail lines counts once."))
        pk = f"{SID}_{y}_passenger_km_mtr"
        out.append(row(obs_id=pk, year=y, metric_id="passenger_km", value=fmt(trips * t["avg_trip_km_domestic_cross_boundary"]),
                       unit="km", scope=METRO, value_type="derived", source_id=TEN,
                       source_locator="Computed from the input rows listed in inputs", method_id="hk_metro_derived",
                       inputs=f"{tr};{al}",
                       notes="Trips times average trip length (0.1 km rounding gives up to about 0.5% error)."))
        # estimated metro cost
        c = t["opex_per_car_km_hk_rail_excl_hsr"]
        k_tot = k_h + k_o
        s = k_o / k_tot
        base = c * k_tot * k_h / k_tot  # r = 1
        low = c * k_tot * k_h / (k_h + R_HIGH * k_o)
        high = c * k_tot * k_h / (k_h + R_LOW * k_o)
        oe = f"{SID}_{y}_opex_total_est"
        out.append(row(obs_id=oe, year=y, metric_id="opex_total", value=fmt(base * 1), value_low=fmt(low),
                       value_high=fmt(high), unit="HKD", currency="HKD", price_basis="nominal", scope=METRO,
                       value_type="estimated", source_id=TEN,
                       source_locator="Computed from the input rows listed in inputs",
                       method_id="hk_metro_cost_from_car_km",
                       inputs=f"{ids[('opex_per_car_km', RAIL)]};{ck};{k_ae};{k_lr}",
                       notes=f"ESTIMATE. MTR rail cost per car-km (excluding high-speed rail) times heavy-rail car-km; Airport Express and Light Rail ({s:.1%} of rail car-km) assumed to cost 0.5x to 2x heavy rail per car-km."))
        # estimated metro staff
        st = t["staff_hk_transport_operations"]
        share = base / (total * 1e6)
        out.append(row(obs_id=f"{SID}_{y}_employees_fte_est", year=y, metric_id="employees_fte",
                       value=fmt(st * share), value_low=fmt(st * low / (total * 1e6) * 0.85),
                       value_high=fmt(min(st, st * high / (total * 1e6) * 1.15)), unit="employees",
                       scope=METRO, value_type="estimated", source_id=TEN,
                       source_locator="Computed from the input rows listed in inputs",
                       method_id="hk_metro_staff_share",
                       inputs=f"{ids[('employees_fte', ALL)]};{oe};{ids[('opex_total', ALL)]}",
                       notes=f"ESTIMATE. Hong Kong transport operations staff times the metro's estimated share of operating cost ({share:.0%}), with an extra -15%/+15% for differences in labour intensity."))
    out.sort(key=lambda r: (int(r["year"]), r["metric_id"], r["obs_id"]))
    p = ROOT / "data" / "peers" / f"{SID}.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"{p.relative_to(ROOT)}: {len(out)} rows")


if __name__ == "__main__":
    main()
