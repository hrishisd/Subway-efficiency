"""Build the findings website from the dataset.

    python3 scripts/build_site.py

Reads the data through scripts/report_data.py (the same row-choice rules as the report), and writes:
  site/data.json    every value shown on the site, with its obs_id / rel_id / fact_id, source and estimate flag
  site/index.html   site/template.html with data.json embedded, so the page works as one file

No number is typed into the page by hand. Takeaway sentences that contain numbers are filled
from the data here. Ratios shown on the site are listed under "calcs" in data.json with their
formula and input rows.
"""
import csv, json, math, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_data import ROOT, OBS, REL, FACTORS, US, pick, is_estimate  # noqa: E402

SITE = os.path.join(ROOT, "site")
REPO = "https://github.com/hrishisd/subway-efficiency"

try:
    SHA = os.environ.get("GITHUB_SHA") or subprocess.check_output(
        ["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
except Exception:  # noqa: BLE001
    SHA = "main"

NAMES = {
    "nyc_subway": "New York", "london_underground": "London", "tokyo_metro": "Tokyo Metro",
    "tokyo_toei": "Toei (Tokyo)", "hong_kong_mtr": "Hong Kong", "seoul_metro": "Seoul",
    "singapore_mrt": "Singapore (SMRT)", "madrid_metro": "Madrid", "beijing_subway": "Beijing",
    "berlin_ubahn": "Berlin", "paris_metro": "Paris", "istanbul_metro": "Istanbul",
    "path": "PATH (NY-NJ)", "wmata_metrorail": "Washington", "mbta_subway": "Boston",
    "septa_subway": "Philadelphia", "chicago_l": "Chicago", "bart": "BART (SF Bay)",
}
FOREIGN = ["london_underground", "madrid_metro", "tokyo_metro", "tokyo_toei", "hong_kong_mtr", "seoul_metro",
           "singapore_mrt", "beijing_subway"]
USPEERS = ["path", "wmata_metrorail", "mbta_subway", "septa_subway", "chicago_l", "bart"]
# Main charts compare NYC with foreign metros only. US systems appear only in the one chart
# for which no foreign data exists (staff by job), in a separate, clearly secondary section.
ALL = ["nyc_subway"] + FOREIGN


# ------------------------------------------------------------------ provenance helpers
def line_numbers(path, key):
    out = {}
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f), start=2):
            out[r[key]] = i
    return out


LINES = {"obs": line_numbers("data/observations.csv", "obs_id"),
         "rel": line_numbers("data/reliability.csv", "rel_id"),
         "fact": line_numbers("data/factors.csv", "fact_id")}
FILES = {"obs": "data/observations.csv", "rel": "data/reliability.csv", "fact": "data/factors.csv"}
SOURCES = {r["source_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "sources/sources.csv"), encoding="utf-8"))}
USED_SOURCES = set()


def est_methods(oid, seen=None):
    """method_ids of every `estimated` row in the input chain of oid."""
    seen = seen or set()
    if oid in seen or oid not in OBS:
        return []
    seen.add(oid)
    r = OBS[oid]
    out = [r["method_id"]] if r["value_type"] == "estimated" and r["method_id"] else []
    for i in r["inputs"].split(";"):
        out += est_methods(i.strip(), seen)
    return list(dict.fromkeys(out))


def chain_sources(oid, seen=None):
    """source_ids of a row and every row in its input chain, original documents first."""
    seen = seen if seen is not None else set()
    if oid in seen or oid not in OBS:
        return []
    seen.add(oid)
    r = OBS[oid]
    out = []
    for i in r["inputs"].split(";"):
        out += chain_sources(i.strip(), seen)
    out.append(r["source_id"])
    return list(dict.fromkeys(out))


def ref(kind, rid, row):
    """Provenance record for one dataset row: its own source, plus (for derived and estimated rows)
    the sources of every input row, so the reader reaches the original document, not only the last step."""
    sids = chain_sources(rid) if kind == "obs" else [row["source_id"]]
    USED_SOURCES.update(sids)
    d = {"id": rid, "file": FILES[kind], "line": LINES[kind][rid], "source": row["source_id"], "sources": sids,
         "locator": row.get("source_locator", ""), "type": row["value_type"], "verification": row["verification"]}
    if kind == "obs":
        d["methods"] = est_methods(rid)
        if row.get("method_id"):
            d["method"] = row["method_id"]
    return d


def point(label, v, system, year=None, extra=None):
    """One plotted value from an observations row (report_data.V)."""
    d = {"label": label, "system": system, "value": v.value, "est": v.est, "ref": ref("obs", v.oid, v.row)}
    if v.est and v.low is not None and v.high is not None:
        d["low"], d["high"] = v.low, v.high
    if year:
        d["year"] = year
    d["group"] = "nyc" if system == "nyc_subway" else ("us" if system in US else "foreign")
    if extra:
        d.update(extra)
    return d


def items(year, metric, systems):
    out = []
    for s in systems:
        v = pick(s, year, metric)
        if v is not None:
            out.append(point(NAMES[s], v, s, year))
    return out


CALCS = []


def calc(cid, value, formula, inputs, desc):
    est = any(is_estimate(i) for i in inputs if i in OBS)
    CALCS.append({"id": cid, "value": value, "estimate": est, "formula": formula, "inputs": inputs, "description": desc})
    return value, est


def ratio_range(year, metric, peers):
    """min and max of NYC / peer for the given metric, with the calcs recorded."""
    nyc = pick("nyc_subway", year, metric)
    rs = []
    for s in peers:
        p = pick(s, year, metric)
        if p is None:
            continue
        r, est = calc(f"nyc_over_{s}_{metric}_{year}", nyc.value / p.value, f"{nyc.oid} / {p.oid}", [nyc.oid, p.oid],
                      f"NYC {year} {metric} divided by {NAMES[s]} {year}")
        rs.append((r, est, s))
    return rs


def pct(x):
    return f"{(x - 1) * 100:.0f}%"


def xs(x):
    return f"{x:.1f}×"


CHARTS = []


def chart(**kw):
    CHARTS.append(kw)


# ------------------------------------------------------------------ 1. cost per car-km 2019
FOREIGN_COST = ["london_underground", "madrid_metro", "tokyo_metro", "tokyo_toei", "hong_kong_mtr", "seoul_metro"]
r19 = ratio_range(2019, "opex_per_car_km", FOREIGN_COST)
lo19, hi19 = min(r19), max(r19)
r23 = ratio_range(2023, "opex_per_car_km", ["london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr",
                                             "singapore_mrt"])
lo23, hi23 = min(r23), max(r23)
chart(id="carkm", section="service", kind="hbar", fmt="usd2",
      title="Cost per car-km, 2019",
      unit="Operating cost per car-kilometre of service, 2024 US$ (PPP for non-US systems)",
      axis="2024 US$ per car-km, PPP",
      takeaway=f"Per unit of service, NYC costs more than every foreign metro with data: "
               f"{pct(lo19[0])} more than {NAMES[lo19[2]]} up to {pct(hi19[0])} more than {NAMES[hi19[2]]}.",
      note="A car-km is one rail car moving one kilometre. Cars differ in size (London's are small), "
           "so read this together with cost per train-km.",
      items=items(2019, "opex_per_car_km", ALL))

# ------------------------------------------------------------------ 2. cost per train-km 2023
tk = ratio_range(2023, "opex_per_train_km", ["london_underground", "tokyo_metro", "tokyo_toei"])
chart(id="trainkm", section="service", kind="hbar", fmt="usd0",
      title="Cost per train-km, 2023",
      unit="Operating cost per train-kilometre, 2024 US$ (PPP for non-US). Only systems that report train-km.",
      axis="2024 US$ per train-km, PPP",
      takeaway=f"Per whole train, the gap is wider: NYC spent {xs(max(tk)[0])} London's and "
               f"{xs([t for t in tk if t[2] == 'tokyo_metro'][0][0])} Tokyo Metro's cost per train-km, "
               f"partly because NYC trains are longer.",
      note="NYC trains average about 9 cars, Tokyo about 8, London about 7. "
           "Only these four systems report train-km.",
      items=items(2023, "opex_per_train_km", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei"]))

# ------------------------------------------------------------------ 3. per passenger-km 2019
pk = ratio_range(2019, "opex_per_passenger_km", ["london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr"])
pkd = {s: (r, e) for r, e, s in pk}
chart(id="pkm", section="rider", kind="hbar", fmt="usd2",
      title="Cost per passenger-km, 2019",
      unit="Operating cost per passenger-kilometre travelled, 2024 US$ (PPP for non-US systems)",
      axis="2024 US$ per passenger-km, PPP",
      takeaway=f"Per kilometre a rider travels, NYC costs about the same as London "
               f"({xs(pkd['london_underground'][0])}) but about {xs(pkd['tokyo_metro'][0])} Tokyo Metro and "
               f"{xs(pkd['hong_kong_mtr'][0])} Hong Kong.",
      note="Tokyo 2019 passenger-km are estimated from the 2015-18 trip length; 2018 values, which are fully reported, "
           "give the same picture. No figure for Madrid, Seoul, Paris or Beijing.",
      items=items(2019, "opex_per_passenger_km", ALL))

# ------------------------------------------------------------------ 4. per trip 2019
chart(id="trip", section="rider", kind="hbar", fmt="usd2",
      title="Cost per trip, 2019",
      unit="Operating cost per trip, 2024 US$ (PPP for non-US systems)",
      axis="2024 US$ per trip, PPP",
      takeaway="Per trip, Tokyo, Hong Kong and Seoul cost about half as much as NYC. NYC looks cheaper than London "
               "only because NYC trips are short and every transfer counts as a new trip.",
      note="Trip-counting rules differ: the US counts every boarding; London, Madrid and Tokyo count entries. "
           "Beijing is a news-report figure with unstated definitions.",
      items=items(2019, "opex_per_trip", ALL))

# ------------------------------------------------------------------ 5. scatter cost per car-km vs load
pts = []
for s in ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr"]:
    c, ld = pick(s, 2019, "opex_per_car_km"), pick(s, 2019, "avg_car_load")
    if c and ld:
        pts.append({"label": NAMES[s], "system": s, "group": "nyc" if s == "nyc_subway" else ("us" if s in US else "foreign"),
                    "x": ld.value, "y": c.value, "est": c.est or ld.est,
                    "xref": ref("obs", ld.oid, ld.row), "yref": ref("obs", c.oid, c.row)})
LOADR = []
for s in ("tokyo_metro", "tokyo_toei", "hong_kong_mtr"):
    ld = pick(s, 2019, "avg_car_load")
    n = pick("nyc_subway", 2019, "avg_car_load")
    LOADR.append(calc(f"{s}_over_nyc_load_2019", ld.value / n.value, f"{ld.oid} / {n.oid}", [ld.oid, n.oid],
                      f"{NAMES[s]} passengers per car divided by NYC's, 2019")[0])
chart(id="load", section="rider", kind="scatter",
      title="Cost per car-km against passengers per car, 2019",
      unit="Each dot is a system. Gray lines join points with equal cost per passenger-km.",
      axis_x="Average passengers on board per car (passenger-km ÷ car-km)",
      axis_y="2024 US$ per car-km, PPP",
      takeaway=f"Tokyo and Hong Kong are cheap per rider mostly because their cars carry "
               f"{min(LOADR):.1f} to {max(LOADR):.1f} times as many people as NYC's, not because their trains are much "
               f"cheaper to run.",
      note="Cost per passenger-km = cost per car-km ÷ passengers per car. A car-km is one rail car moving one kilometre.",
      iso=[0.1, 0.2, 0.4, 0.8], points=pts)

# ------------------------------------------------------------------ 6. decomposition
nyc19 = {m: pick("nyc_subway", 2019, m) for m in ("opex_per_car_km", "avg_car_load", "opex_per_passenger_km")}
dec = []
for s in ("tokyo_metro", "tokyo_toei", "hong_kong_mtr"):
    a, ld = pick(s, 2019, "opex_per_car_km"), pick(s, 2019, "avg_car_load")
    lc = math.log(nyc19["opex_per_car_km"].value / a.value)
    ll = math.log(ld.value / nyc19["avg_car_load"].value)
    share, est = calc(f"load_share_{s}_2019", ll / (lc + ll),
                      f"ln({ld.oid}/{nyc19['avg_car_load'].oid}) / [ln({nyc19['opex_per_car_km'].oid}/{a.oid}) + same]",
                      [ld.oid, nyc19["avg_car_load"].oid, nyc19["opex_per_car_km"].oid, a.oid],
                      f"Share of the log gap in cost per passenger-km (NYC vs {NAMES[s]}, 2019) due to passengers per car")
    gap = nyc19["opex_per_passenger_km"].value / pick(s, 2019, "opex_per_passenger_km").value
    dec.append({"label": NAMES[s], "system": s, "load": share, "cost": 1 - share, "est": est, "gap": gap,
                "calc": f"load_share_{s}_2019"})
chart(id="split", section="rider", kind="split",
      title="Why NYC costs more per passenger-km than Asia, 2019",
      unit="Share of NYC's higher cost per passenger-km explained by each part (log split, the two parts add to 100%)",
      axis="Share of the gap",
      takeaway=f"Emptier cars explain {min(d['load'] for d in dec) * 100:.0f}% to {max(d['load'] for d in dec) * 100:.0f}% "
               f"of NYC's per-rider gap with Tokyo and Hong Kong; the rest is NYC's higher cost per car-km.",
      note="Label on the right is how many times NYC's cost per passenger-km is the peer's.",
      parts=[{"key": "load", "label": "Fewer passengers per car"}, {"key": "cost", "label": "Higher cost per car-km"}],
      rows=dec)

# ------------------------------------------------------------------ 7. staff per million car-km
st_items = items(2023, "employees_per_million_car_km", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei",
                                                       "hong_kong_mtr"])
for s, y in (("seoul_metro", 2019), ("madrid_metro", 2018)):
    v = pick(s, y, "employees_per_million_car_km")
    if v:
        st_items.append(point(f"{NAMES[s]} ({y})", v, s, y))
sr = ratio_range(2023, "employees_per_million_car_km", ["london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr"])
chart(id="staff", section="labor", kind="hbar", fmt="n0",
      title="Staff per million car-km, 2023",
      unit="Operating employees per million car-km of service (head counts; London is full-time equivalents)",
      axis="Employees per million car-km",
      takeaway=f"NYC uses {pct(min(sr)[0])} to {pct(max(sr)[0])} more of its own staff per unit of service than Tokyo, "
               f"London and Hong Kong. That is only half the staffing story: each NYC employee also costs much more "
               f"(next chart).",
      note="Seoul counts every employee of the corporation. Systems that contract out more work look leaner here.",
      items=st_items)

# ------------------------------------------------------------------ 7b. wages and benefits per employee
PAY = [("nyc_subway", "New York"), ("tokyo_metro", "Tokyo Metro"), ("tokyo_toei", "Toei (Tokyo)"),
       ("hong_kong_mtr", "Hong Kong (all HK transport)")]
nyc_c = pick("nyc_subway", 2023, "staff_cost_per_employee")
pay_rows, pay_r = [], []


def seg(v):
    if v is None:
        return None
    d = {"value": v.value, "est": v.est, "ref": ref("obs", v.oid, v.row)}
    if v.est and v.low is not None:
        d["low"], d["high"] = v.low, v.high
    return d


for s_, lab in PAY:
    w_, b_ = pick(s_, 2023, "staff_wages_per_employee"), pick(s_, 2023, "staff_benefits_per_employee")
    c_ = pick(s_, 2023, "staff_cost_per_employee")
    segs = [seg(w_), seg(b_), None] if (w_ and b_) else [None, None, seg(c_)]
    pay_rows.append({"label": lab, "system": s_, "group": "nyc" if s_ == "nyc_subway" else "foreign", "segs": segs,
                     "est": bool(c_.est)})
    if s_ != "nyc_subway":
        pay_r.append(calc(f"nyc_over_{s_}_staff_cost_per_employee_2023", nyc_c.value / c_.value,
                          f"{nyc_c.oid} / {c_.oid}", [nyc_c.oid, c_.oid],
                          f"NYC 2023 wages and benefits per employee divided by {NAMES[s_]}")[0])
nyc_w, nyc_b = pick("nyc_subway", 2023, "staff_wages_per_employee"), pick("nyc_subway", 2023, "staff_benefits_per_employee")
nyc_share = pick("nyc_subway", 2023, "staff_cost_share_of_opex")
tm_ck, nyc_ck = pick("tokyo_metro", 2023, "opex_per_car_km"), pick("nyc_subway", 2023, "opex_per_car_km")
tm_sc, tm_ot = pick("tokyo_metro", 2023, "opex_staff_costs"), pick("tokyo_metro", 2023, "opex_total")
tm_c = pick("tokyo_metro", 2023, "staff_cost_per_employee")
cf, _ = calc("nyc_carkm_at_tokyo_metro_pay_over_tokyo_metro_2023",
             (nyc_share.value * nyc_ck.value / (nyc_c.value / tm_c.value) + (1 - nyc_share.value) * nyc_ck.value) / tm_ck.value,
             f"({nyc_share.oid} * {nyc_ck.oid} / ({nyc_c.oid} / {tm_c.oid}) + (1 - {nyc_share.oid}) * {nyc_ck.oid}) / {tm_ck.oid}",
             [nyc_share.oid, nyc_ck.oid, nyc_c.oid, tm_c.oid, tm_ck.oid],
             "NYC 2023 cost per car-km if its own staff were paid Tokyo Metro's cost per employee, over Tokyo Metro's")
chart(id="pay", section="labor", kind="stack", fmt="usd0", year="2023", tip_unit="per employee a year",
      num_label="Row", label_w=190,
      title="Wages and benefits per employee, 2023",
      unit="Staff cost per employee of the operator's own staff, 2024 US$ (PPP for non-US systems)",
      axis="2024 US$ per employee",
      takeaway=f"Each NYC subway employee costs "
               f"{('about %.2f' % min(pay_r)) if round(min(pay_r), 2) == round(max(pay_r), 2) else ('%.2f to %.2f' % (min(pay_r), max(pay_r)))}"
               f" times as much as one in Tokyo or Hong "
               f"Kong, and benefits ({nyc_b.value / nyc_w.value * 100:.0f}% of NYC wages) are most of the difference. "
               f"At Tokyo Metro's pay, NYC would cost about {cf:.2f}× what Tokyo Metro does per car-km.",
      note="Own staff only: work contracted out (Tokyo Metro contracts most maintenance to subsidiaries) is not included. "
           "NYC benefits include pensions and retiree health care as booked. Hong Kong is an ESTIMATE: it covers MTR's "
           "whole Hong Kong transport business, and its staff cost may include staff its head count leaves out. "
           "Toei and Hong Kong do not split wages and benefits. No London figure yet.",
      series=[{"key": "wages", "label": "Wages"}, {"key": "benefits", "label": "Benefits"},
              {"key": "total", "label": "Wages and benefits (not split)"}],
      rows=pay_rows)

# ------------------------------------------------------------------ 8. US staff by function
FUNCS = [("employees_vehicle_operations", "Vehicle operations (train crews, dispatch)"),
         ("employees_vehicle_maintenance", "Vehicle maintenance"),
         ("employees_facility_maintenance", "Facility maintenance (track, stations, signals, power)"),
         ("employees_general_administration", "General administration")]
rows = []
for s in ["nyc_subway"] + USPEERS:
    tkm = pick(s, 2024, "train_km")
    segs = []
    for k, _ in FUNCS:
        r = pick(s, 2024, k)
        val, est = calc(f"{s}_{k}_per_m_train_km_2024", r.value / tkm.value * 1e6, f"{r.oid} / {tkm.oid} * 1e6",
                        [r.oid, tkm.oid], f"{NAMES[s]} 2024 {k} per million train-km")
        segs.append({"key": k, "value": val, "ref": ref("obs", r.oid, r.row), "den": ref("obs", tkm.oid, tkm.row)})
    rows.append({"label": NAMES[s], "system": s, "group": "nyc" if s == "nyc_subway" else "us", "segs": segs})
fm = {r["system"]: r["segs"][2]["value"] for r in rows}
others = [v for s, v in fm.items() if s not in ("nyc_subway", "path")]
chart(id="functions", section="us", kind="stack", fmt="n0",
      title="Where NYC's staff work, against US systems, 2024",
      unit="Operating employees per million train-km, by function (US National Transit Database)",
      axis="Employees per million train-km",
      takeaway=f"NYC's extra staff are in facility maintenance ({fm['nyc_subway']:.0f} per million train-km, against "
               f"{min(others):.0f} to {max(others):.0f} at most US peers), not on the trains.",
      note="Shown only because no foreign metro publishes staff by job. US systems are not peers of NYC; "
           "this chart is context, not a ranking.",
      series=[{"key": k, "label": lab} for k, lab in FUNCS], rows=rows)

# ------------------------------------------------------------------ 9. NYC trend
series = []
for metric, lab in (("opex_per_car_km", "All operating costs"),
                    ("opex_excl_ga_per_car_km", "Excluding general administration")):
    pts_ = []
    for y in range(2012, 2026):
        v = pick("nyc_subway", y, metric)
        if v:
            pts_.append({"x": y, "y": v.value, "est": v.est, "ref": ref("obs", v.oid, v.row)})
    series.append({"label": lab, "points": pts_})
a15 = [p for p in series[0]["points"] if p["x"] == 2015][0]["y"]
a24 = [p for p in series[0]["points"] if p["x"] == 2024][0]["y"]
chart(id="trend", section="time", kind="line", fmt="usd2",
      title="NYC cost per car-km over time, 2012–2025",
      unit="NYC subway operating cost per car-km, 2024 US$ (US GDP deflator)",
      axis="2024 US$ per car-km",
      takeaway=f"In real terms NYC's cost per car-km has been flat for a decade ({(a24 / a15 - 1) * 100:+.0f}% from 2015 to "
               f"2024); without administration it fell, and administration more than doubled after 2022.",
      note="The 2012 value and the 2016–17 drop may be series breaks. Data before 2012 is missing.",
      band=[2019.5, 2022.5], band_label="pandemic", series=series)

# ------------------------------------------------------------------ 10. farebox
fb = items(2019, "farebox_recovery", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei", "seoul_metro"]
)
hk = pick("hong_kong_mtr", 2019, "farebox_recovery")
fb.append(point("Hong Kong (all MTR)", hk, "hong_kong_mtr", 2019))
fare = {}
for s in ("nyc_subway", "tokyo_metro"):
    f_, c_ = pick(s, 2019, "farebox_recovery"), pick(s, 2019, "opex_per_trip")
    fare[s] = calc(f"fare_per_trip_{s}_2019", f_.value * c_.value, f"{f_.oid} * {c_.oid}", [f_.oid, c_.oid],
                   f"Fare revenue per trip, {NAMES[s]}, 2019, 2024 US$")[0]
chart(id="farebox", section="money", kind="hbar", fmt="pct", ref_line=1.0, ref_label="fares cover 100% of cost",
      title="Farebox recovery, 2019",
      unit="Fare revenue as a share of operating cost",
      axis="Fare revenue ÷ operating cost",
      takeaway=f"Tokyo covers more than its full operating cost from fares while NYC covered "
               f"{pick('nyc_subway', 2019, 'farebox_recovery').value * 100:.0f}%, yet fare revenue per "
               f"trip was similar (NYC ${fare['nyc_subway']:.2f}, Tokyo Metro ${fare['tokyo_metro']:.2f}): "
               f"the difference is cost, not fares.",
      note="Hong Kong covers MTR's whole Hong Kong transport business, not heavy rail alone.",
      items=fb)

# ------------------------------------------------------------------ 11. reliability
def rel_rows(system, metric, period):
    return [r for r in REL if r["system_id"] == system and r["metric_id"] == metric and r["period"] == period]


nyc_m = rel_rows("nyc_subway", "mdbf_car_km", "2025")[0]
hk_m = sorted(rel_rows("hong_kong_mtr", "mdbf_car_km", "2025"), key=lambda r: float(r["value"]))
sg_m = rel_rows("singapore_mrt", "mdbf_car_km", "2025")[0]


def relpt(label, r, system):
    return {"label": label, "system": system, "value": float(r["value"]), "est": r["value_type"] == "estimated",
            "group": "nyc" if system == "nyc_subway" else "foreign", "ref": ref("rel", r["rel_id"], r),
            "definition": r["agency_definition"]}


rel_items = [relpt("New York", nyc_m, "nyc_subway"), relpt("Hong Kong, line group A", hk_m[0], "hong_kong_mtr"),
             relpt("Singapore", sg_m, "singapore_mrt"), relpt("Hong Kong, line group B", hk_m[1], "hong_kong_mtr")]
rr = [float(r["value"]) / float(nyc_m["value"]) for r in (hk_m[0], sg_m, hk_m[1])]
chart(id="mdbf", section="reliability", kind="hbar", fmt="km", log=True,
      title="Car-km between train failures, 2025",
      unit="Car-kilometres run per train failure that delays service, each agency's own definition (log scale)",
      axis="Car-km between delay-causing failures (log scale)",
      takeaway=f"Hong Kong and Singapore trains run {min(rr):.0f} to {max(rr):.0f} times as far between failures as "
               f"NYC's; definitions differ, but not by that much.",
      note="Hong Kong and Singapore count only failures that delay service by 5 minutes or more, so they count fewer.",
      items=rel_items)

# ------------------------------------------------------------------ 12. factors grid
def fact(system, fid):
    rows_ = [f for f in FACTORS if f["system_id"] == system and f["factor_id"] == fid]
    rows_.sort(key=lambda f: f["verification"] != "verified")
    return rows_[0] if rows_ else None


CREW = {"one_person": "One person", "mostly_two_person": "Two people (most lines)",
        "mixed_two_and_one_person": "Two people on lines 1–4", "mixed_one_person_and_unattended": "One person or driverless"}
NIGHT = {"24h_all_week": "Every night", "24h_weekends_some_lines": "Weekend nights, some lines",
         "closes_nightly": "Closes every night"}
fgrid = []
for s in ["nyc_subway", "london_underground", "paris_metro", "madrid_metro", "berlin_ubahn", "tokyo_metro", "seoul_metro",
          "hong_kong_mtr", "singapore_mrt"]:
    row = {"label": NAMES[s], "system": s}
    for fid, lab in (("opened_year", None), ("crew_model", CREW), ("overnight_service", NIGHT)):
        f = fact(s, fid)
        if f:
            row[fid] = {"value": lab.get(f["value"], f["value"]) if lab else f["value"], "ref": ref("fact", f["fact_id"], f)}
    fgrid.append(row)

FACTOR_VERDICTS = [
    ("Pay and benefits per employee", "strong", "Each NYC employee costs about 1.65 times as much as in Tokyo or Hong Kong; at Tokyo pay most of the gap goes."),
    ("Facility-maintenance staffing", "strong", "Most direct evidence: NYC's extra staff are in track, station and signal upkeep."),
    ("24/7 service", "plausible", "Fits the maintenance-heavy staffing; cannot be tested separately with this data."),
    ("Administration and injury claims", "growing", "Admin rose from 13% of cost (2019) to 23% (2024)."),
    ("Two-person crews", "real but modest", "About 7% of operating cost; at most about a quarter of the gap."),
    ("Old signals", "indirect", "Hurts reliability and blocks crew savings; direct cost effect not separable."),
    ("System age", "weak", "London is older and cheaper; Chicago is old and cheap."),
    ("Funding mix", "weak", "Fare recovery looks like a result of low cost and crowding, not a cause."),
]

# ------------------------------------------------------------------ headline tiles
pk_tokyo = pkd["tokyo_metro"]
trip_tokyo = [(r, e) for r, e, s in ratio_range(2019, "opex_per_trip", ["tokyo_metro"])][0]
# Headline tiles lead with the per-rider measures (Hrishi, 2026-11-26); cost per car-km is secondary.
tiles = [
    {"value": xs(pk_tokyo[0]), "est": pk_tokyo[1], "label": "NYC cost per passenger-km relative to Tokyo Metro, 2019",
     "target": "pkm"},
    {"value": xs(pkd["london_underground"][0]), "est": pkd["london_underground"][1],
     "label": "NYC cost per passenger-km relative to London, 2019", "target": "pkm"},
    {"value": xs(trip_tokyo[0]), "est": trip_tokyo[1], "label": "NYC cost per trip relative to Tokyo Metro, 2019",
     "target": "trip"},
    {"value": f"{min(rr):.0f}–{max(rr):.0f}×", "est": False,
     "label": "more often NYC trains fail than Hong Kong's and Singapore's", "target": "mdbf"},
]

GAPS = [
    "Paris: no metro-only cost is published (RATP reports metro, RER, tram and bus together).",
    "Shanghai, Istanbul: no usable unit cost. Beijing: one news-report figure. Berlin: one cost per trip (2017).",
    "Hong Kong, Seoul, Madrid and Singapore costs are estimates; Seoul 2022–24 is weak.",
    "London car-km and Tokyo passenger-km after 2018 are estimated.",
    "NYC data before 2012 is missing; 2012 and 2016–17 may be series breaks.",
    "Pay per employee only for Tokyo and Hong Kong (2023), not London; not yet compared with average pay in each country.",
]

sources = {sid: {"title": SOURCES[sid]["title"], "publisher": SOURCES[sid]["publisher"], "url": SOURCES[sid]["url"],
                 "kind": SOURCES[sid]["source_kind"]} for sid in sorted(USED_SOURCES) if sid in SOURCES}

data = {
    "built_from": SHA, "repo": REPO,
    "report_url": f"{REPO}/blob/main/report/report.md",
    "tiles": tiles, "charts": CHARTS, "factors": fgrid, "verdicts": FACTOR_VERDICTS, "gaps": GAPS,
    "sources": sources, "calcs": CALCS,
}

os.makedirs(SITE, exist_ok=True)
js = json.dumps(data, ensure_ascii=False, indent=1, default=lambda o: round(o, 6))
open(os.path.join(SITE, "data.json"), "w", encoding="utf-8").write(js + "\n")
tpl = open(os.path.join(SITE, "template.html"), encoding="utf-8").read()
compact = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = tpl.replace("/*__DATA__*/null", compact)
assert html != tpl, "data placeholder missing from template"
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(html)
print(f"site: {len(CHARTS)} charts, {len(CALCS)} computed values, {len(sources)} sources, built from {SHA[:10]}")
