"""Shared data access for the report build (scripts/build_report.py).

pick(system, year, metric) returns the row the report uses for a value, applying one
fixed preference order so every table and chart uses the same row:
  money:  real_USD_2024_GDP_deflator (US systems) or PPP_USD_2024 (others)
  scope:  metro_only, then metro_with_allocated_overhead, then any other scope
A value counts as an ESTIMATE if its row, or any row in its input chain, is `estimated`.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBS = {r["obs_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/observations.csv"), encoding="utf-8"))}
FACTORS = list(csv.DictReader(open(os.path.join(ROOT, "data/factors.csv"), encoding="utf-8")))
REL = list(csv.DictReader(open(os.path.join(ROOT, "data/reliability.csv"), encoding="utf-8")))
SYSTEMS = {r["system_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/systems.csv"), encoding="utf-8"))}

US = {"nyc_subway", "path", "wmata_metrorail", "mbta_subway", "septa_subway", "chicago_l", "bart"}
MONEY = {"opex_per_car_km", "opex_per_passenger_km", "opex_per_trip", "opex_per_train_km",
         "opex_excl_ga_per_car_km", "opex_total", "fare_revenue", "opex_per_car_hour"}
SCOPE_ORDER = ["metro_only", "metro_with_allocated_overhead", "metro_with_allocated_infrastructure",
               "whole_agency", "smrt_trains_heavy_rail", "beijing_three_operators", "hk_transport_operations_all"]

_INDEX = {}
for r in OBS.values():
    _INDEX.setdefault((r["system_id"], int(r["year"]), r["metric_id"]), []).append(r)

_est_cache = {}
def is_estimate(oid, depth=0):
    if oid in _est_cache:
        return _est_cache[oid]
    r = OBS.get(oid)
    res = False
    if r is not None:
        if r["value_type"] == "estimated":
            res = True
        elif depth < 12:
            res = any(is_estimate(i.strip(), depth + 1) for i in r["inputs"].split(";") if i.strip() in OBS)
    _est_cache[oid] = res
    return res

class V:
    def __init__(self, row):
        self.row = row
        self.oid = row["obs_id"]
        self.value = float(row["value"])
        self.low = float(row["value_low"]) if row["value_low"] else None
        self.high = float(row["value_high"]) if row["value_high"] else None
        self.est = is_estimate(self.oid)
        self.source_id = row["source_id"]
        self.verification = row["verification"]

def pick(system, year, metric, scope=None):
    rows = _INDEX.get((system, year, metric), [])
    if metric in MONEY:
        want = "real_USD_2024_GDP_deflator" if system in US else "PPP_USD_2024"
        rows = [r for r in rows if r["price_basis"] == want]
    rows = [r for r in rows if r["scope"] != "unknown" and "levy" not in r["obs_id"]]
    if scope:
        rows = [r for r in rows if r["scope"] == scope]
    if not rows:
        return None
    rows.sort(key=lambda r: SCOPE_ORDER.index(r["scope"]) if r["scope"] in SCOPE_ORDER else 99)
    return V(rows[0])

def obs(oid):
    return V(OBS[oid])
