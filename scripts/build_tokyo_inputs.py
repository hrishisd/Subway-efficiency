#!/usr/bin/env python3
"""Write data/peers/tokyo_metro.csv and data/peers/tokyo_toei.csv.

Inputs:
  data/raw/asia/mlit_yardstick_tokyo.csv  transcription of MLIT railway
      statistics (yardstick table), FY2015-FY2023, with sum checks below.
  STAFF below: Tokyo Metro staff from its annual securities reports.
  TOEI_STAFF below: Toei subway staff (see methods/toei_subway_staff.md).

Run from the repository root, then run scripts/build_peers.py and
scripts/validate.py.
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "asia" / "mlit_yardstick_tokyo.csv"
FIELDS = ["obs_id", "system_id", "year", "year_basis", "metric_id", "value",
          "value_low", "value_high", "unit", "currency", "price_basis", "scope",
          "value_type", "verification", "source_id", "source_locator",
          "method_id", "inputs", "notes"]
OPS = {"東京地下鉄": "tokyo_metro", "東京都": "tokyo_toei"}
SCOPE = "metro_with_allocated_overhead"
YB = "fiscal_apr_mar"

# item_en in the raw file -> (metric_id, multiplier, unit, currency)
REPORTED = {
    "route_km": ("route_km", 1, "km", ""),
    "stations": ("stations", 1, "count", ""),
    "car_km": ("car_km", 1000, "km", ""),
    "train_km": ("train_km", 1000, "km", ""),
    "passengers": ("unlinked_trips", 1000, "trips", ""),
    "passenger_km": ("passenger_km", 1000, "km", ""),
    "fare_revenue": ("fare_revenue", 1000, "JPY", "JPY"),
    "operating_expenses_gross": ("opex_incl_depreciation", 1000, "JPY", "JPY"),
    "depreciation": ("depreciation", 1000, "JPY", "JPY"),
    "general_administration": ("opex_general_administration", 1000, "JPY", "JPY"),
}
NOTES = {
    "unlinked_trips": "輸送人員 (passengers carried) of this operator. A trip that transfers between two lines of the same operator counts once; a trip that continues onto another operator counts in both. Not the same as NTD boardings.",
    "car_km": "旅客車両キロ. Includes cars of other companies that through-run on this operator's lines (settled by car-use fees).",
    "opex_incl_depreciation": "営業費計（厚生福利施設収入控除前）: railway business operating expense including depreciation, taxes (諸税) and leases.",
    "opex_general_administration": "一般管理費 計 (general administration of the railway business).",
    "fare_revenue": "旅客運輸収入 計 (commuter-pass plus ordinary fares).",
}

# Tokyo Metro: staff at fiscal year end (31 March of year+1), from the
# 従業員の状況 section of the securities report for that year end.
# year -> (consolidated 運輸業 segment, parent company 運輸業 segment)
STAFF = {
    2015: (10291, 9223), 2016: (10455, 9400), 2017: (10587, 9497),
    2019: (10875, 9776), 2020: (10914, 9789), 2021: (10878, 9782),
    2022: (10621, 9598), 2023: (10435, 9431), 2024: (10370, 9350),
}

# Toei subway: filled once a source is found. year -> (value, source_id, locator, value_type, low, high, method)
LOC = "p.5 and p.16, 職員数 (年度末現在); re-employed short-time staff in brackets excluded"
TOEI_NOTE = "Head count at fiscal year end of the Toei Subway business (高速電車事業), all in the operating account. Short-time re-employed staff (about 60-95) excluded. Not FTE."
TOEI_STAFF = {
    2017: (3493, "tokyo_audit_toei_subway_fy2018", LOC + ", prior-year column", "reported", "", "", "", TOEI_NOTE),
    2018: (3485, "tokyo_audit_toei_subway_fy2018", LOC, "reported", "", "", "", TOEI_NOTE),
    2019: (3460, "tokyo_audit_toei_subway_fy2019", LOC, "reported", "", "", "", TOEI_NOTE),
    2020: (3480, "tokyo_audit_toei_subway_fy2020", LOC, "reported", "", "", "", TOEI_NOTE),
    2021: (3562, "tokyo_audit_toei_subway_fy2021", LOC, "reported", "", "", "", TOEI_NOTE),
    2022: (3584, "tokyo_audit_toei_subway_fy2022", LOC, "reported", "", "", "", TOEI_NOTE),
    2023: (3587, "tokyo_audit_toei_subway_fy2023", LOC, "reported", "", "", "", TOEI_NOTE),
}

# Toei: 一般会計補助金 in the operating account (営業外収益), million yen.
# year -> (value, source_id, table)
TOEI_SUBSIDY = {
    2017: (4638, "tokyo_audit_toei_subway_fy2018", "表10, p.17, prior-year column"),
    2018: (4273, "tokyo_audit_toei_subway_fy2018", "表10, p.17"),
    2019: (3904, "tokyo_audit_toei_subway_fy2019", "表10, p.17"),
    2020: (3535, "tokyo_audit_toei_subway_fy2020", "表10, p.17"),
    2021: (2882, "tokyo_audit_toei_subway_fy2021", "表10, p.17"),
    2022: (2675, "tokyo_audit_toei_subway_fy2022", "表12, p.17"),
    2023: (6123, "tokyo_audit_toei_subway_fy2023", "表12, p.17"),
}


def sum_checks(d):
    for (y, op), v in sorted(d.items()):
        s = sum(v[k] for k in ("track_maintenance", "electrical_maintenance", "vehicle_maintenance",
                               "train_operation", "station_and_traffic", "maintenance_management",
                               "transport_management"))
        assert s == v["transport_expenses_total"], (y, op, "check 1")
        s = v["transport_expenses_total"] + v["publicity"] + v["welfare_facilities"] + v["general_administration"]
        assert s == v["opex_before_depreciation_and_taxes"], (y, op, "check 2")
        s = v["opex_before_depreciation_and_taxes"] + v["depreciation"] + v["taxes"]
        assert abs(s - v["operating_expenses_gross"]) <= 1, (y, op, "check 3")


def row(**k):
    r = {f: "" for f in FIELDS}
    r.update(k)
    r["verification"] = r["verification"] or "unverified"
    return r


def fmt(x):
    return str(int(round(x))) if abs(x) >= 1e5 else f"{x:.6g}"


def main():
    raw = list(csv.DictReader(open(RAW, encoding="utf-8")))
    d = defaultdict(dict)
    ja = {}
    for r in raw:
        d[(int(r["fiscal_year"]), r["operator"])][r["item_en"]] = float(r["value"])
        ja[r["item_en"]] = r["item_ja"]
    sum_checks(d)
    out = defaultdict(list)
    for (y, op), v in sorted(d.items()):
        sid = OPS[op]
        src = f"mlit_yardstick_fy{y}"
        ids = {}
        for item, (metric, mult, unit, cur) in REPORTED.items():
            if item not in v:
                continue
            oid = f"{sid}_{y}_{metric}_mlit"
            ids[metric] = oid
            out[sid].append(row(
                obs_id=oid, system_id=sid, year=y, year_basis=YB, metric_id=metric,
                value=fmt(v[item] * mult), unit=unit, currency=cur,
                price_basis="nominal" if cur else "", scope=SCOPE, value_type="reported",
                source_id=src,
                source_locator=f"Table 地下鉄事業者, column {op}, row {ja[item]}"
                               + (" (千円; multiplied by 1,000)" if cur else (" (千; multiplied by 1,000)" if mult == 1000 else "")),
                notes=NOTES.get(metric, "")))
        # opex_total = 営業費計 - 減価償却費
        out[sid].append(row(
            obs_id=f"{sid}_{y}_opex_total_mlit", system_id=sid, year=y, year_basis=YB,
            metric_id="opex_total",
            value=fmt((v["operating_expenses_gross"] - v["depreciation"]) * 1000),
            unit="JPY", currency="JPY", price_basis="nominal", scope=SCOPE,
            value_type="derived", source_id=src,
            source_locator="Computed from the input rows listed in inputs",
            method_id="mlit_opex_excl_depreciation",
            inputs=f"{ids['opex_incl_depreciation']};{ids['depreciation']}",
            notes="Railway operating expense excluding depreciation, to match the NTD definition. Includes taxes and leases."))
    # passenger-km estimate for years without a published value
    for sid in ("tokyo_metro", "tokyo_toei"):
        rows = out[sid]
        by = defaultdict(dict)
        for r in rows:
            by[int(r["year"])][r["metric_id"]] = r
        known = {y: float(m["passenger_km"]["value"]) / float(m["unlinked_trips"]["value"])
                 for y, m in by.items() if "passenger_km" in m}
        base = sum(known.values()) / len(known)
        lo_b, hi_b = min(known.values()), max(known.values())
        for y, m in sorted(by.items()):
            if "passenger_km" in m:
                continue
            trips = float(m["unlinked_trips"]["value"])
            wide = 0.10 if y in (2020, 2021, 2022) else 0.05
            rows.append(row(
                obs_id=f"{sid}_{y}_passenger_km_est", system_id=sid, year=y, year_basis=YB,
                metric_id="passenger_km", value=fmt(trips * base),
                value_low=fmt(trips * lo_b * (1 - wide)), value_high=fmt(trips * hi_b * (1 + wide)),
                unit="km", scope=SCOPE, value_type="estimated",
                source_id=f"mlit_yardstick_fy{y}",
                source_locator="Trips from this source; trip length from the FY2015-FY2018 rows listed in inputs",
                method_id="tokyo_passenger_km_from_trip_length",
                inputs=";".join([m["unlinked_trips"]["obs_id"]] + [by[k]["passenger_km"]["obs_id"] for k in sorted(known)] + [by[k]["unlinked_trips"]["obs_id"] for k in sorted(known)]),
                notes=f"ESTIMATE. Trips x mean FY2015-FY2018 trip length ({base:.3f} km); range uses min/max trip length minus/plus {int(wide*100)}%."))
    # Tokyo Metro staff
    for y, (cons, parent) in STAFF.items():
        fye = y + 1
        src = f"tokyometro_yuho_fye{fye}"
        loc = f"第1【企業の概況】5【従業員の状況】as of 31 March {fye}"
        out["tokyo_metro"].append(row(
            obs_id=f"tokyo_metro_{y}_employees_fte_yuho", system_id="tokyo_metro", year=y, year_basis=YB,
            metric_id="employees_fte", value=str(cons), unit="employees", scope=SCOPE,
            value_type="reported", source_id=src,
            source_locator=loc + ", (1) 連結会社の状況, 運輸業 segment 従業員数 (temporary staff, shown in brackets, excluded)",
            notes="Head count at fiscal year end (就業人員), Tokyo Metro group transport segment (company plus transport subsidiaries). Not FTE. Outside contractors excluded."))
        out["tokyo_metro"].append(row(
            obs_id=f"tokyo_metro_{y}_employees_headcount_parent_yuho", system_id="tokyo_metro", year=y, year_basis=YB,
            metric_id="employees_headcount_parent", value=str(parent), unit="employees", scope=SCOPE,
            value_type="reported", source_id=src,
            source_locator=loc + ", (2) 提出会社の状況, 運輸業 segment",
            notes="Head count of Tokyo Metro Co. itself in the transport segment."))
    for y, (val, src, loc, vt, lo, hi, meth, note) in TOEI_STAFF.items():
        out["tokyo_toei"].append(row(
            obs_id=f"tokyo_toei_{y}_employees_fte_{'est' if vt == 'estimated' else 'toei'}", system_id="tokyo_toei",
            year=y, year_basis=YB, metric_id="employees_fte", value=str(val), value_low=lo, value_high=hi,
            unit="employees", scope=SCOPE, value_type=vt, source_id=src, source_locator=loc,
            method_id=meth, notes=note))
    for y, (val, src, tab) in TOEI_SUBSIDY.items():
        out["tokyo_toei"].append(row(
            obs_id=f"tokyo_toei_{y}_operating_subsidy_toei", system_id="tokyo_toei", year=y, year_basis=YB,
            metric_id="operating_subsidy", value=str(val * 1000000), unit="JPY", currency="JPY",
            price_basis="nominal", scope=SCOPE, value_type="reported", source_id=src,
            source_locator=f"一般会計補助金 合計, {tab} (百万円; multiplied by 1,000,000)",
            notes="Tokyo government general-account subsidy in the operating account. Mostly repays interest and principal of special subway bonds (地下鉄事業特例債) and public pension contributions, not day-to-day operations. Toei covers its operating cost from fares."))
    for sid, rows in out.items():
        rows.sort(key=lambda r: (int(r["year"]), r["metric_id"], r["obs_id"]))
        p = ROOT / "data" / "peers" / f"{sid}.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"{p.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
