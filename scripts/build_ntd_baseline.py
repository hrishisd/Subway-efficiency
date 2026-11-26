#!/usr/bin/env python3
"""Build the US heavy-rail baseline rows from the raw NTD extracts.

Reads the extracts in data/raw/ntd/ (see data/raw/ntd/README.md for the exact
queries), and rewrites every observation whose source_id starts with "ntd_"
and whose obs_id ends with "_ntd". Other rows in data/observations.csv are kept.
Also checks the extracts for internal consistency before writing.

Run from the repository root: python3 scripts/build_ntd_baseline.py
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "ntd"
OBS = ROOT / "data" / "observations.csv"
MI_TO_KM = 1.609344  # exact, by definition of the international mile

SYSTEMS = {  # NTD ID -> system_id (heavy rail mode "HR", directly operated "DO")
    "20008": "nyc_subway",
    "50066": "chicago_l",
    "30030": "wmata_metrorail",
    "10003": "mbta_subway",
    "30019": "septa_subway",
    "90003": "bart",
    "20098": "path",
}

SRC_TS = "ntd_ts21_by_mode"
SRC_EMP = "ntd_employees_by_mode"
SRC_BRK = "ntd_breakdowns"
SCOPE = "metro_with_allocated_overhead"
YEAR_BASIS = "ntd_report_year"

TS_FIELDS = {  # TS2.1 field -> (metric_id, unit, currency)
    "Operating Expenses": ("opex_total", "USD", "USD"),
    "Operating Expenses - Vehicle Operations": ("opex_vehicle_operations", "USD", "USD"),
    "Operating Expenses - Vehicle Maintenance": ("opex_vehicle_maintenance", "USD", "USD"),
    "Operating Expenses - Facility Maintenance": ("opex_facility_maintenance", "USD", "USD"),
    "Operating Expenses - General Administration": ("opex_general_administration", "USD", "USD"),
    "Fares": ("fare_revenue", "USD", "USD"),
    "Vehicle Revenue Miles": ("car_revenue_miles", "mi", ""),
    "Vehicle Revenue Hours": ("car_revenue_hours", "hours", ""),
    "Unlinked Passenger Trips": ("unlinked_trips", "trips", ""),
    "Passenger Miles Traveled": ("passenger_miles", "mi", ""),
    "Directional Route Miles": ("directional_route_miles", "mi", ""),
    "Vehicles Operated in Maximum Service": ("cars_max_service", "cars", ""),
}

FUNCS = ["vehicle_operations", "vehicle_maintenance", "facility_maintenance",
         "general_administration", "capital_labor"]
OPERATING_FUNCS = FUNCS[:4]

FIELDNAMES = ["obs_id", "system_id", "year", "year_basis", "metric_id", "value",
              "value_low", "value_high", "unit", "currency", "price_basis", "scope",
              "value_type", "verification", "source_id", "source_locator",
              "method_id", "inputs", "notes"]


def fmt(x, derived=False):
    """Reported values keep their digits; derived values keep 6 significant digits."""
    if x == int(x):
        return str(int(x))
    if derived:
        return str(round(x)) if abs(x) >= 1e5 else f"{x:.6g}"
    return f"{x:.10g}"


def num(s):
    return float(s) if s not in ("", None) else 0.0


class Builder:
    def __init__(self):
        self.rows = {}

    def add(self, system, year, metric, value, unit, *, currency="", value_type="reported",
            source, locator, method="", inputs=(), notes="", tag="", price_basis=None):
        oid = f"{system}_{year}_{metric}{tag}_ntd"
        assert oid not in self.rows, oid
        self.rows[oid] = {
            "obs_id": oid, "system_id": system, "year": str(year), "year_basis": YEAR_BASIS,
            "metric_id": metric, "value": fmt(value, value_type != "reported"), "value_low": "", "value_high": "",
            "unit": unit, "currency": currency,
            "price_basis": price_basis or ("nominal" if currency else ""),
            "scope": SCOPE, "value_type": value_type, "verification": "unverified",
            "source_id": source, "source_locator": locator, "method_id": method,
            "inputs": ";".join(inputs), "notes": notes,
        }
        return oid

    def val(self, system, year, metric):
        r = self.rows.get(f"{system}_{year}_{metric}_ntd")
        return None if r is None else float(r["value"])

    def oid(self, system, year, metric):
        o = f"{system}_{year}_{metric}_ntd"
        return o if o in self.rows else None


def check(ts, emp, brk):
    errors = []
    for (nid, year), f in ts.items():
        parts = sum(f[k] for k in f if k.startswith("Operating Expenses - "))
        if abs(parts - f["Operating Expenses"]) > 0.5:
            errors.append(f"TS2.1 {nid} {year}: functions do not sum to total")
    for (nid, year, ftpt), r in emp.items():
        if abs(sum(num(r[f"{fn}_hours"]) for fn in FUNCS) - num(r["total_hours"])) > 0.5:
            errors.append(f"employees {nid} {year} {ftpt}: hours do not sum")
        if abs(sum(num(r[f"{fn}_count"]) for fn in FUNCS) - num(r["total_employee_count"])) > 0.05:
            errors.append(f"employees {nid} {year} {ftpt}: counts do not sum")
    for (nid, year), r in brk.items():
        if num(r["total_mechanical_failures"]) != num(r["major_mechanical_failures"]) + num(r["other_mechanical_failures"]):
            errors.append(f"breakdowns {nid} {year}: failures do not sum")
        if (nid, year) in ts and num(r["vehicle_passenger_car_revenue_miles"]) != ts[(nid, year)]["Vehicle Revenue Miles"]:
            errors.append(f"breakdowns {nid} {year}: car revenue miles differ from TS2.1")
    return errors


def main():
    ts = defaultdict(dict)
    with open(RAW / "ts21_hr_2015_2025.csv", newline="") as f:
        for r in csv.DictReader(f):
            for y in range(2015, 2026):
                ts[(r["ntd_id"], y)][r["field"]] = float(r[str(y)])
    emp = {}
    with open(RAW / "employees_hr_2022_2025.csv", newline="") as f:
        for r in csv.DictReader(f):
            emp[(r["ntd_id"], int(r["report_year"]), r["full_or_part_time"])] = r
    brk = {}
    with open(RAW / "breakdowns_hr_2022_2025.csv", newline="") as f:
        for r in csv.DictReader(f):
            brk[(r["ntd_id"], int(r["report_year"]))] = r

    with open(RAW / "profiles_nyct_hr_2012_2014.csv", newline="") as f:
        profiles = list(csv.DictReader(f))
    with open(RAW / "opex_by_type_nyct_hr_2022_2025.csv", newline="") as f:
        by_type = list(csv.DictReader(f))
    cpi = {}
    with open(ROOT / "data" / "price_indices.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["index_id"] == "us_cpi_u":
                cpi[int(r["year"])] = float(r["value"])

    errors = check(ts, emp, brk)
    for r in profiles:  # printed ratios in the same PDF must match our transcription
        o = float(r["opex_total"])
        for den, col in (("car_revenue_miles", "printed_opex_per_vrm"), ("car_revenue_hours", "printed_opex_per_vrh"),
                         ("passenger_miles", "printed_opex_per_pmt"), ("unlinked_trips", "printed_opex_per_upt")):
            if round(o / float(r[den]), 2) != float(r[col]):
                errors.append(f"profile {r['report_year']}: {col} does not match")
    for r in by_type:
        parts = sum(float(v) for k, v in r.items() if k not in ("report_year", "total") and v)
        if abs(parts - float(r["total"])) > 0.5:
            errors.append(f"by-type {r['report_year']}: classes do not sum")
        if abs(float(r["total"]) - ts[("20008", int(r["report_year"]))]["Operating Expenses"]) > 0.5:
            errors.append(f"by-type {r['report_year']}: total differs from TS2.1")
    if errors:
        print("\n".join(errors))
        return 1

    b = Builder()
    # ---- reported: TS2.1 -------------------------------------------------
    for (nid, year), fields in sorted(ts.items()):
        sysid = SYSTEMS[nid]
        for field, (metric, unit, cur) in TS_FIELDS.items():
            b.add(sysid, year, metric, fields[field], unit, currency=cur, source=SRC_TS,
                  locator=f"Dataset npsm-38gk; ntd_id={nid}, mode=HR, type_of_service=DO, "
                          f"report_year={year}, field=\"{field}\"; column value")
    # ---- reported: employees ---------------------------------------------
    for (nid, year, ftpt), r in sorted(emp.items()):
        sysid = SYSTEMS[nid]
        tag = "ft" if ftpt == "Full Time" else "pt"
        for fn in FUNCS + ["total"]:
            for kind, col, unit in (("count", f"{fn}_count" if fn != "total" else "total_employee_count", "employees"),
                                    ("hours", f"{fn}_hours", "hours")):
                if r[col] == "":
                    continue
                b.add(sysid, year, f"employee_{kind}_{fn}_{tag}", num(r[col]), unit, source=SRC_EMP,
                      locator=f"Dataset uyv8-9jek; ntd_id={nid}, mode=HR, report_year={year}, "
                              f"full_or_part_time=\"{ftpt}\"; column {col}")
    # ---- reported: breakdowns --------------------------------------------
    for (nid, year), r in sorted(brk.items()):
        sysid = SYSTEMS[nid]
        for col, metric, unit in (("major_mechanical_failures", "major_mechanical_failures", "failures"),
                                  ("other_mechanical_failures", "other_mechanical_failures", "failures"),
                                  ("total_mechanical_failures", "total_mechanical_failures", "failures"),
                                  ("train_revenue_miles", "train_revenue_miles", "mi")):
            b.add(sysid, year, metric, num(r[col]), unit, source=SRC_BRK,
                  locator=f"Dataset amkt-4ehs; ntd_id={nid}, mode=HR, type_of_service=DO, "
                          f"report_year={year}; column {col}")

    # ---- reported: NTD agency profiles, NYC 2012-2014 ------------------------
    labels = {"opex_total": ("Operating Expenses", "USD", "USD"),
              "fare_revenue": ("Fare Revenues", "USD", "USD"),
              "car_revenue_miles": ("Annual Vehicle Revenue Miles", "mi", ""),
              "car_revenue_hours": ("Annual Vehicle Revenue Hours", "hours", ""),
              "unlinked_trips": ("Annual Unlinked Trips", "trips", ""),
              "passenger_miles": ("Annual Passenger Miles", "mi", ""),
              "directional_route_miles": ("Fixed Guideway Directional Route Miles", "mi", ""),
              "cars_max_service": ("Vehicles Operated in Maximum Service", "cars", "")}
    for r in profiles:
        year = int(r["report_year"])
        for metric, (label, unit, cur) in labels.items():
            b.add("nyc_subway", year, metric, float(r[metric]), unit, currency=cur, source=r["source_id"],
                  locator=f"Heavy Rail row of the modal characteristics table, column \"{label}\"",
                  notes="Single-year NTD agency profile; series before 2015 is not from TS2.1. "
                        "No breakdown by function in this source.")
    # ---- reported: NYC operating expense by object class, 2022-2025 ---------
    for r in by_type:
        year = int(r["report_year"])
        for col in r:
            if col in ("report_year", "total") or r[col] == "":
                continue
            b.add("nyc_subway", year, f"opex_type_{col}", float(r[col]), "USD", currency="USD",
                  source="ntd_opex_by_type",
                  locator=f"Dataset j5uj-anzx; ntd_id=20008, mode=HR, type_of_service=DO, "
                          f"report_year={year}; column {col}")

    # ---- derived ----------------------------------------------------------
    def derive(sysid, year, metric, value, unit, inputs, method, currency="", notes=""):
        src = b.rows[inputs[0]]["source_id"]
        b.add(sysid, year, metric, value, unit, currency=currency, value_type="derived",
              source=src, locator="Computed from the input rows listed in inputs",
              method=method, inputs=inputs, notes=notes)

    for sysid in SYSTEMS.values():
        for year in range(2012, 2026):
            g = lambda m: b.val(sysid, year, m)
            o = lambda m: b.oid(sysid, year, m)
            if o("opex_total") is None:
                continue
            # unit conversions
            for src_m, dst_m in (("car_revenue_miles", "car_km"), ("passenger_miles", "passenger_km"),
                                 ("directional_route_miles", "directional_route_km"),
                                 ("train_revenue_miles", "train_km")):
                if o(src_m):
                    derive(sysid, year, dst_m, g(src_m) * MI_TO_KM, "km", [o(src_m)], "ntd_miles_to_km")
            opex = g("opex_total")
            ga = g("opex_general_administration")
            derive(sysid, year, "opex_per_car_km", opex / g("car_km"), "USD/car-km",
                   [o("opex_total"), o("car_km")], "ntd_unit_ratios", "USD")
            if ga is not None:
                derive(sysid, year, "opex_excl_ga_per_car_km", (opex - ga) / g("car_km"), "USD/car-km",
                       [o("opex_total"), o("opex_general_administration"), o("car_km")], "ntd_unit_ratios", "USD")
            derive(sysid, year, "opex_per_car_hour", opex / g("car_revenue_hours"), "USD/car-hour",
                   [o("opex_total"), o("car_revenue_hours")], "ntd_unit_ratios", "USD")
            derive(sysid, year, "opex_per_passenger_km", opex / g("passenger_km"), "USD/passenger-km",
                   [o("opex_total"), o("passenger_km")], "ntd_unit_ratios", "USD")
            derive(sysid, year, "opex_per_trip", opex / g("unlinked_trips"), "USD/trip",
                   [o("opex_total"), o("unlinked_trips")], "ntd_unit_ratios", "USD")
            derive(sysid, year, "farebox_recovery", g("fare_revenue") / opex, "ratio",
                   [o("fare_revenue"), o("opex_total")], "ntd_unit_ratios")
            derive(sysid, year, "avg_trip_length_km", g("passenger_km") / g("unlinked_trips"), "km",
                   [o("passenger_km"), o("unlinked_trips")], "ntd_unit_ratios")
            derive(sysid, year, "avg_car_load", g("passenger_km") / g("car_km"), "passengers",
                   [o("passenger_km"), o("car_km")], "ntd_unit_ratios")
            if o("train_km"):
                derive(sysid, year, "avg_cars_per_train", g("car_km") / g("train_km"), "cars",
                       [o("car_km"), o("train_km")], "ntd_unit_ratios",
                       notes="Car revenue km (TS2.1) over train revenue km (Breakdowns table)")
            if o("major_mechanical_failures") and g("major_mechanical_failures") > 0:
                derive(sysid, year, "mdbf", g("car_km") / g("major_mechanical_failures"), "car-km",
                       [o("car_km"), o("major_mechanical_failures")], "ntd_mdbf_major",
                       notes="Major mechanical failures only; see method note")
            # staff
            ins_c = [o(f"employee_count_{fn}_{t}") for fn in OPERATING_FUNCS for t in ("ft", "pt")]
            ins_c = [i for i in ins_c if i]
            if ins_c:
                ins_h = [o(f"employee_hours_{fn}_{t}") for fn in OPERATING_FUNCS for t in ("ft", "pt")]
                ins_h = [i for i in ins_h if i]
                staff = sum(float(b.rows[i]["value"]) for i in ins_c)
                hours = sum(float(b.rows[i]["value"]) for i in ins_h)
                derive(sysid, year, "employees_operating", staff, "employees", ins_c, "ntd_operating_staff")
                derive(sysid, year, "employee_hours_operating", hours, "hours", ins_h, "ntd_operating_staff")
                for fn in OPERATING_FUNCS:
                    ii = [i for i in (o(f"employee_count_{fn}_ft"), o(f"employee_count_{fn}_pt")) if i]
                    derive(sysid, year, f"employees_{fn}", sum(float(b.rows[i]["value"]) for i in ii),
                           "employees", ii, "ntd_operating_staff")
                eo = o("employees_operating")
                derive(sysid, year, "employees_per_million_car_km", staff / (g("car_km") / 1e6),
                       "employees per million car-km", [eo, o("car_km")], "ntd_unit_ratios")
                derive(sysid, year, "passenger_km_per_employee", g("passenger_km") / staff,
                       "passenger-km per employee", [o("passenger_km"), eo], "ntd_unit_ratios")
                derive(sysid, year, "trips_per_employee", g("unlinked_trips") / staff,
                       "trips per employee", [o("unlinked_trips"), eo], "ntd_unit_ratios")
                derive(sysid, year, "opex_per_employee_hour", opex / hours, "USD/hour",
                       [o("opex_total"), o("employee_hours_operating")], "ntd_unit_ratios", "USD",
                       notes="All operating expense (not only labor) per operating labor hour")

    # ---- derived: constant 2024 dollars (CPI-U) ------------------------------
    REAL = ["opex_total", "fare_revenue", "opex_per_car_km", "opex_excl_ga_per_car_km",
            "opex_per_passenger_km", "opex_per_trip", "opex_per_car_hour"]
    for oid, r in list(b.rows.items()):
        if r["metric_id"] not in REAL or r["price_basis"] != "nominal":
            continue
        year = int(r["year"])
        factor = cpi[2024] / cpi[year]
        b.add(r["system_id"], year, r["metric_id"], float(r["value"]) * factor, r["unit"], currency="USD",
              value_type="derived", source="fred_cpiaucns",
              locator=f"CPI-U annual averages for {year} and 2024 in data/price_indices.csv",
              method="ntd_cpi_real_2024", inputs=[oid], tag="_real2024", price_basis="real_USD_2024_CPI-U",
              notes=f"Nominal value x CPI-U 2024 / CPI-U {year} = x {factor:.4f}")

    # ---- merge with other rows and write ------------------------------------
    with open(OBS, newline="", encoding="utf-8") as f:
        keep = [r for r in csv.DictReader(f) if not r["obs_id"].endswith("_ntd")]
    allrows = keep + list(b.rows.values())
    allrows.sort(key=lambda r: (r["system_id"], int(r["year"]), r["metric_id"], r["obs_id"]))
    with open(OBS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, lineterminator="\n")
        w.writeheader()
        w.writerows(allrows)
    print(f"wrote {len(b.rows)} NTD rows; {len(keep)} other rows kept")
    return 0


if __name__ == "__main__":
    sys.exit(main())
