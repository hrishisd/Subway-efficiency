"""Build the research report from the dataset.

    python3 scripts/build_report.py

Reads data/observations.csv (through scripts/report_data.py), writes:
  report/figures/*.png      charts
  report/numbers.csv        every computed number used in the report text, with formula and input rows
  report/report.md          rendered from report/report_template.md

Template placeholders:
  {{v:system:year:metric:fmt}}   one dataset value; "(est.)" is appended when it is an estimate
  {{c:calc_id}}                  a computed number from CALCS below (also listed in numbers.csv)
  {{t:table_id}}                 a generated table
  {{fig:file:alt}}               a figure
Formats: usd2 ($1.23), usd0 ($123), pct (45%), x1 (1.2x), n0 (1,234), n1 (12.3), k (455k), m (1.2M)
"""
import csv, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_data import ROOT, OBS, REL, FACTORS, SYSTEMS, US, pick, obs, is_estimate  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

REPORT = os.path.join(ROOT, "report")
FIG = os.path.join(REPORT, "figures")
os.makedirs(FIG, exist_ok=True)

# ---------------------------------------------------------------- style (dataviz reference palette, light mode)
for f in font_manager.findSystemFonts():
    if "Inter" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 10,
    "axes.edgecolor": "#c9c9c9", "axes.labelcolor": "#666666", "xtick.color": "#666666", "ytick.color": "#191919",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#ececec",
    "grid.linewidth": 0.8, "axes.axisbelow": True, "figure.dpi": 100, "savefig.dpi": 200,
    "text.color": "#191919", "axes.titlecolor": "#191919",
})
NYC_C = "#257de0"     # categorical slot 1: NYC
PEER_C = "#8a8a8a"    # neutral for peers
US_C = "#b8b8b8"      # lighter neutral for US peers
SERIES = ["#257de0", "#f47230", "#00b894", "#f2a600"]  # slots 1-4, fixed order
TEXT2 = "#666666"

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


def fmt(x, f):
    if x is None:
        return "–"
    if f == "usd2":
        return f"${x:,.2f}"
    if f == "usd0":
        return f"${x:,.0f}"
    if f == "usdb":
        return f"${x / 1e9:,.2f}B"
    if f == "usdm":
        return f"${x / 1e6:,.0f}M"
    if f == "pct":
        return f"{x * 100:.0f}%"
    if f == "chg":
        return f"{(x - 1) * 100:+.0f}%"
    if f == "x1":
        return f"{x:.1f}×"
    if f == "x2":
        return f"{x:.2f}×"
    if f == "n0":
        return f"{x:,.0f}"
    if f == "n1":
        return f"{x:,.1f}"
    if f == "k":
        return f"{x / 1e3:,.0f}k"
    if f == "m":
        return f"{x / 1e6:,.2f}M"
    raise ValueError(f)


def vstr(v, f, bold_est=True):
    if v is None:
        return "–"
    s = fmt(v.value, f)
    if v.est:
        rng = ""
        if v.low is not None and v.high is not None and f.startswith("usd"):
            rng = f" ({fmt(v.low, f)}–{fmt(v.high, f)})"
        return f"**{s} EST**{rng}" if bold_est else f"{s} EST"
    return s


# ---------------------------------------------------------------- computed numbers (numbers.csv)
CALCS = {}


def calc(cid, value, formula, inputs, desc, fmt_="n1"):
    ins = [i for i in inputs if i]
    est = any(is_estimate(i) for i in ins if i in OBS)
    CALCS[cid] = dict(calc_id=cid, value=value, fmt=fmt_, estimate=est, formula=formula,
                      inputs=";".join(ins), description=desc)
    return value


def V(s, y, m, scope=None):
    return pick(s, y, m, scope)


def ratio(cid, a, b, desc, f="x1"):
    if "change" in cid:
        f = "chg"
    return calc(cid, a.value / b.value, f"{a.oid} / {b.oid}", [a.oid, b.oid], desc, f)


nyc19 = {m: V("nyc_subway", 2019, m) for m in ("opex_per_car_km", "opex_per_passenger_km", "opex_per_trip",
                                               "avg_car_load", "farebox_recovery", "fare_revenue", "unlinked_trips",
                                               "opex_total", "opex_excl_ga_per_car_km", "avg_trip_length_km")}
nyc23 = {m: V("nyc_subway", 2023, m) for m in ("opex_per_car_km", "opex_per_passenger_km", "opex_per_trip",
                                               "opex_per_train_km", "employees_per_million_car_km", "car_km",
                                               "passenger_km_per_employee", "trips_per_employee", "avg_car_load",
                                               "avg_cars_per_train")}

# Gap ratios, 2019 and 2023
for s in ("london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr", "seoul_metro", "madrid_metro"):
    for m, tag in (("opex_per_car_km", "carkm"), ("opex_per_passenger_km", "pkm"), ("opex_per_trip", "trip")):
        p = V(s, 2019, m)
        if p:
            ratio(f"nyc_over_{s}_{tag}_2019", nyc19[m], p, f"NYC 2019 {m} divided by {s} 2019")
    p = V(s, 2019, "avg_car_load")
    if p:
        ratio(f"{s}_over_nyc_load_2019", p, nyc19["avg_car_load"], f"{s} passengers per car divided by NYC's, 2019")
for s in ("london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr", "singapore_mrt"):
    for m, tag in (("opex_per_car_km", "carkm"), ("opex_per_passenger_km", "pkm"), ("opex_per_trip", "trip"),
                   ("employees_per_million_car_km", "staff")):
        p = V(s, 2023, m)
        if p and nyc23.get(m if m != "opex_per_train_km" else "opex_per_train_km"):
            key = m
            ratio(f"nyc_over_{s}_{tag}_2023", nyc23[key], p, f"NYC 2023 {m} divided by {s} 2023")
# train-km ratios
for s in ("london_underground", "tokyo_metro", "tokyo_toei"):
    p = V(s, 2023, "opex_per_train_km")
    ratio(f"nyc_over_{s}_trainkm_2023", nyc23["opex_per_train_km"], p, f"NYC 2023 cost per train-km over {s}")

# Seoul 2024 vs NYC 2024
nyc24 = {m: V("nyc_subway", 2024, m) for m in ("opex_per_car_km", "opex_per_trip", "opex_total",
                                               "opex_general_administration", "opex_facility_maintenance",
                                               "opex_vehicle_operations", "opex_vehicle_maintenance",
                                               "opex_type_casualty_and_liability", "employees_operating",
                                               "employees_facility_maintenance", "employees_vehicle_operations",
                                               "employees_vehicle_maintenance", "employees_general_administration",
                                               "car_km", "train_km", "opex_excl_ga_per_car_km")}
ratio("nyc_over_seoul_metro_carkm_2024", nyc24["opex_per_car_km"], V("seoul_metro", 2024, "opex_per_car_km"),
      "NYC 2024 cost per car-km over Seoul 2024 (Seoul estimated)")

# Log decomposition of the cost-per-passenger-km gap, 2019: share explained by load
for s in ("tokyo_metro", "tokyo_toei", "hong_kong_mtr"):
    a = V(s, 2019, "opex_per_car_km")
    ld = V(s, 2019, "avg_car_load")
    lc = math.log(nyc19["opex_per_car_km"].value / a.value)
    ll = math.log(ld.value / nyc19["avg_car_load"].value)
    calc(f"load_share_{s}_2019", ll / (lc + ll),
         f"ln({ld.oid}/{nyc19['avg_car_load'].oid}) / [ln({nyc19['opex_per_car_km'].oid}/{a.oid}) + same]",
         [ld.oid, nyc19["avg_car_load"].oid, nyc19["opex_per_car_km"].oid, a.oid],
         f"Share of the log gap in cost per passenger-km (NYC vs {s}, 2019) due to passengers per car", "pct")

# Fare revenue per trip, 2019 (farebox x cost per trip)
for s in ("nyc_subway", "tokyo_metro", "tokyo_toei", "london_underground"):
    fb, ct = V(s, 2019, "farebox_recovery"), V(s, 2019, "opex_per_trip")
    calc(f"fare_per_trip_{s}_2019", fb.value * ct.value, f"{fb.oid} * {ct.oid}", [fb.oid, ct.oid],
         f"Fare revenue per trip, {s}, 2019, 2024 USD (PPP for non-US)", "usd2")

# NYC cost structure 2024
tot = nyc24["opex_total"]
for k in ("opex_general_administration", "opex_facility_maintenance", "opex_vehicle_operations",
          "opex_vehicle_maintenance", "opex_type_casualty_and_liability"):
    r = V("nyc_subway", 2024, k)
    calc(f"nyc_share_{k}_2024", r.value / tot.value, f"{r.oid} / {tot.oid}", [r.oid, tot.oid],
         f"NYC 2024 {k} as share of operating expense", "pct")
for k in ("employees_facility_maintenance", "employees_vehicle_operations", "employees_vehicle_maintenance",
          "employees_general_administration"):
    r = V("nyc_subway", 2024, k)
    e = nyc24["employees_operating"]
    calc(f"nyc_share_{k}_2024", r.value / e.value, f"{r.oid} / {e.oid}", [r.oid, e.oid],
         f"NYC 2024 {k} as share of operating employees", "pct")

# US staff by function per million train-km, 2024
FUNCS = ["employees_vehicle_operations", "employees_vehicle_maintenance", "employees_facility_maintenance",
         "employees_general_administration"]
us_func = {}
for s in ["nyc_subway"] + USPEERS:
    tk = V(s, 2024, "train_km")
    us_func[s] = {}
    for k in FUNCS:
        r = V(s, 2024, k)
        us_func[s][k] = calc(f"{s}_{k}_per_m_train_km_2024", r.value / tk.value * 1e6, f"{r.oid} / {tk.oid} * 1e6",
                             [r.oid, tk.oid], f"{s} 2024 {k} per million train-km", "n0")
    dk = V(s, 2024, "directional_route_km")
    fm = V(s, 2024, "employees_facility_maintenance")
    calc(f"{s}_fm_per_dir_km_2024", fm.value / dk.value, f"{fm.oid} / {dk.oid}", [fm.oid, dk.oid],
         f"{s} 2024 facility-maintenance employees per directional route-km", "n1")
    calc(f"{s}_train_km_per_dir_km_2024", tk.value / dk.value, f"{tk.oid} / {dk.oid}", [tk.oid, dk.oid],
         f"{s} 2024 train-km per directional route-km (how hard each km of track is used)", "n0")
    fmc, ck = V(s, 2024, "opex_facility_maintenance"), V(s, 2024, "car_km")
    fmr = V(s, 2024, "opex_facility_maintenance")
    # nominal 2024 dollars = 2024 dollars
    calc(f"{s}_fm_cost_per_car_km_2024", fmc.value / ck.value, f"{fmc.oid} / {ck.oid}", [fmc.oid, ck.oid],
         f"{s} 2024 facility maintenance cost per car-km (USD)", "usd2")
    calc(f"{s}_fm_cost_share_2024", fmr.value / V(s, 2024, "opex_total").value,
         f"{fmr.oid} / {V(s, 2024, 'opex_total').oid}", [fmr.oid, V(s, 2024, "opex_total").oid],
         f"{s} 2024 facility maintenance share of opex", "pct")

# Crew-size illustration: CBC saving (secondary) as share of NYC opex and of the gap to peers
fact = [f for f in FACTORS if f["system_id"] == "nyc_subway" and f["factor_id"] == "unionization"
        and "442" in f["value"]][0]
CBC = 442e6
calc("cbc_crew_saving", CBC, f"factors.csv {fact['fact_id']} (text quotes $442 million a year)", [],
     "Citizens Budget Commission estimate of savings from one-person crews, via Reason (secondary)", "usdm")
calc("cbc_share_of_opex_2024", CBC / nyc24["opex_total"].value, f"442e6 / {nyc24['opex_total'].oid}",
     [nyc24["opex_total"].oid], "CBC crew saving as share of NYC 2024 subway operating expense", "pct")
for s in ("tokyo_metro", "london_underground", "hong_kong_mtr"):
    p = V(s, 2023, "opex_per_car_km")
    gap = (nyc23["opex_per_car_km"].value - p.value) * nyc23["car_km"].value
    calc(f"gap_dollars_vs_{s}_2023", gap, f"({nyc23['opex_per_car_km'].oid} - {p.oid}) * {nyc23['car_km'].oid}",
         [nyc23["opex_per_car_km"].oid, p.oid, nyc23["car_km"].oid],
         f"NYC 2023 cost above what {s}'s cost per car-km would give on NYC's car-km (2024 USD)", "usdb")
    calc(f"cbc_share_of_gap_{s}_2023", CBC / gap, f"442e6 / gap_dollars_vs_{s}_2023", [p.oid],
         f"CBC crew saving as share of the NYC-{s} cost gap, 2023", "pct")

# claims and admin
cas = nyc24["opex_type_casualty_and_liability"]
calc("nyc_casualty_per_car_km_2024", cas.value / nyc24["car_km"].value, f"{cas.oid} / {nyc24['car_km'].oid}",
     [cas.oid, nyc24["car_km"].oid], "NYC 2024 casualty and liability cost per car-km", "usd2")
ga19 = V("nyc_subway", 2019, "opex_general_administration")
calc("nyc_ga_share_2019", ga19.value / obs("nyc_subway_2019_opex_total_ntd").value,
     f"{ga19.oid} / nyc_subway_2019_opex_total_ntd", [ga19.oid, "nyc_subway_2019_opex_total_ntd"],
     "NYC 2019 general administration share of opex", "pct")

# NYC trend
r15, r24 = V("nyc_subway", 2015, "opex_per_car_km"), V("nyc_subway", 2024, "opex_per_car_km")
x15, x24 = V("nyc_subway", 2015, "opex_excl_ga_per_car_km"), V("nyc_subway", 2024, "opex_excl_ga_per_car_km")
ratio("nyc_real_carkm_change_2015_2024", r24, r15, "NYC real cost per car-km 2024 / 2015")
ratio("nyc_real_exga_carkm_change_2015_2024", x24, x15, "NYC real cost per car-km excl. admin 2024 / 2015")
x19 = V("nyc_subway", 2019, "opex_excl_ga_per_car_km")
ratio("nyc_real_exga_carkm_change_2019_2024", x24, x19, "NYC real cost per car-km excl. admin 2024 / 2019")
ratio("nyc_real_carkm_change_2019_2024", r24, V("nyc_subway", 2019, "opex_per_car_km"),
      "NYC real cost per car-km 2024 / 2019")

# Reliability ratios
def rel(system, metric, period, contains=None):
    rows = [r for r in REL if r["system_id"] == system and r["metric_id"] == metric and r["period"] == period]
    if contains:
        rows = [r for r in rows if contains in (r["notes"] + r["agency_metric_name"] + r["source_id"])]
    return rows


nyc_mdbf = rel("nyc_subway", "mdbf_car_km", "2025")[0]
hk_mdbf = sorted(rel("hong_kong_mtr", "mdbf_car_km", "2025"), key=lambda r: float(r["value"]))
sg_mdbf = rel("singapore_mrt", "mdbf_car_km", "2025")[0]
for nm, r in (("hk_low", hk_mdbf[0]), ("hk_high", hk_mdbf[1]), ("sg", sg_mdbf)):
    calc(f"mdbf_ratio_{nm}_2025", float(r["value"]) / float(nyc_mdbf["value"]),
         f"reliability.csv {r['rel_id']} / {nyc_mdbf['rel_id']}", [], f"MDBF {nm} over NYC, 2025", "n0")

# ---------------------------------------------------------------- tables
TABLES = {}


def table(rows, header, align=None):
    align = align or ["---"] + ["---:"] * (len(header) - 1)
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join(align) + " |"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def unit_table(year, systems, est_ok=True, cols=None):
    cols = cols or [("opex_per_passenger_km", "usd2", "Cost per passenger-km"), ("opex_per_trip", "usd2", "Cost per trip"),
                    ("opex_per_car_km", "usd2", "Cost per car-km"), ("opex_per_train_km", "usd0", "Cost per train-km"),
                    ("farebox_recovery", "pct", "Farebox recovery"), ("avg_car_load", "n0", "Passengers per car"),
                    ("avg_trip_length_km", "n1", "Avg trip (km)")]
    rows = []
    for s in systems:
        cells = []
        for m, f, _ in cols:
            v = V(s, year, m)
            if v is not None and not est_ok and v.est:
                cells.append("(est. left out)")
            else:
                c = vstr(v, f)
                if m == "farebox_recovery" and v is not None and v.row["scope"] == "hk_transport_operations_all":
                    c += " ¹"
                cells.append(c)
        if any(c not in ("–", "(est. left out)") for c in cells):
            rows.append([("**" + NAMES[s] + "**") if s == "nyc_subway" else NAMES[s]] + cells)
    keep = [i for i in range(len(cols)) if any(r[i + 1] != "–" for r in rows)]
    rows = [[r[0]] + [r[i + 1] for i in keep] for r in rows]
    return table(rows, ["System"] + [cols[i][2] for i in keep])


TABLES["unit_2019"] = unit_table(2019, ["nyc_subway"] + FOREIGN)
TABLES["unit_2019_us"] = unit_table(2019, ["nyc_subway"] + USPEERS)
TABLES["unit_2023"] = unit_table(2023, ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei",
                                        "hong_kong_mtr", "singapore_mrt"])
# Without estimates: use 2018 for Tokyo passenger-km (reported) and 2019 otherwise
noest_rows = []
for s, y in (("nyc_subway", 2019), ("nyc_subway", 2018), ("london_underground", 2019), ("london_underground", 2018),
             ("tokyo_metro", 2018), ("tokyo_metro", 2019), ("tokyo_toei", 2018), ("tokyo_toei", 2019)):
    cells = []
    for m, f in (("opex_per_passenger_km", "usd2"), ("opex_per_trip", "usd2"), ("opex_per_car_km", "usd2"),
                 ("opex_per_train_km", "usd0"), ("farebox_recovery", "pct")):
        v = V(s, y, m)
        cells.append("left out (est.)" if (v is not None and v.est) else vstr(v, f))
    noest_rows.append([f"{NAMES[s]} {y}"] + cells)
TABLES["unit_noest"] = table(noest_rows, ["System, year", "Cost per passenger-km", "Cost per trip", "Cost per car-km",
                                          "Cost per train-km", "Farebox recovery"])

# Decomposition table
dec = []
for s in ("tokyo_metro", "tokyo_toei", "hong_kong_mtr", "london_underground"):
    a, ld, pk = V(s, 2019, "opex_per_car_km"), V(s, 2019, "avg_car_load"), V(s, 2019, "opex_per_passenger_km")
    dec.append([NAMES[s], vstr(a, "usd2"), vstr(ld, "n0"), vstr(pk, "usd2"),
                fmt(nyc19["opex_per_car_km"].value / a.value, "x1") + (" EST" if a.est else ""),
                fmt(ld.value / nyc19["avg_car_load"].value, "x1") + (" EST" if ld.est else ""),
                fmt(nyc19["opex_per_passenger_km"].value / pk.value, "x1") + (" EST" if pk.est else ""),
                (fmt(CALCS[f"load_share_{s}_2019"]["value"], "pct") + (" EST" if CALCS[f"load_share_{s}_2019"]["estimate"] else ""))
                if f"load_share_{s}_2019" in CALCS else "n/a (London cars are emptier)"])
dec.insert(0, ["**New York**", vstr(nyc19["opex_per_car_km"], "usd2"), vstr(nyc19["avg_car_load"], "n0"),
               vstr(nyc19["opex_per_passenger_km"], "usd2"), "", "", "", ""])
TABLES["decomp_2019"] = table(dec, ["System (2019)", "Cost per car-km", "Passengers per car", "Cost per passenger-km",
                                    "NYC cost per car-km is … higher", "Peer carries … more per car",
                                    "NYC cost per passenger-km is … higher", "Share of gap from passengers per car"])

# Staff table, 2023
st = []
for s in ("nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr"):
    y = 2023
    st.append([("**New York**" if s == "nyc_subway" else NAMES[s]),
               vstr(V(s, y, "employees_per_million_car_km"), "n0"), vstr(V(s, y, "passenger_km_per_employee"), "k"),
               vstr(V(s, y, "trips_per_employee"), "k")])
st.append(["Seoul (2019)", vstr(V("seoul_metro", 2019, "employees_per_million_car_km"), "n0"), "–",
           vstr(V("seoul_metro", 2019, "trips_per_employee"), "k")])
st.append(["Madrid (2018)", vstr(V("madrid_metro", 2018, "employees_per_million_car_km"), "n0"), "–",
           vstr(V("madrid_metro", 2018, "trips_per_employee"), "k")])
for s in USPEERS:
    st.append([NAMES[s], vstr(V(s, 2023, "employees_per_million_car_km"), "n0"),
               vstr(V(s, 2023, "passenger_km_per_employee"), "k"), vstr(V(s, 2023, "trips_per_employee"), "k")])
TABLES["staff_2023"] = table(st, ["System (2023 unless shown)", "Staff per million car-km", "Passenger-km per staff",
                                  "Trips per staff"])

# ---- Staff cost per employee and pay-versus-headcount split, 2023
COMP_PEERS = ["tokyo_metro", "tokyo_toei", "hong_kong_mtr"]
nyc_comp = V("nyc_subway", 2023, "staff_cost_per_employee")
nyc_wage = V("nyc_subway", 2023, "staff_wages_per_employee")
nyc_ben = V("nyc_subway", 2023, "staff_benefits_per_employee")
nyc_share = V("nyc_subway", 2023, "staff_cost_share_of_opex")
nyc_ck = nyc23["opex_per_car_km"]
calc("nyc_share_staff_cost_2023", nyc_share.value, nyc_share.oid, [nyc_share.oid],
     "NYC staff cost as a share of operating cost, 2023", "pct")
calc("nyc_benefits_over_wages_2023", nyc_ben.value / nyc_wage.value, f"{nyc_ben.oid} / {nyc_wage.oid}",
     [nyc_ben.oid, nyc_wage.oid], "NYC fringe benefits as a share of wages, 2023", "pct")
nyc_lab_ck = calc("nyc_labor_per_car_km_2023", nyc_share.value * nyc_ck.value, f"{nyc_share.oid} * {nyc_ck.oid}",
                  [nyc_share.oid, nyc_ck.oid], "NYC staff cost per car-km, 2023 (2024 $)", "usd2")
nyc_nl_ck = calc("nyc_nonlabor_per_car_km_2023", (1 - nyc_share.value) * nyc_ck.value,
                 f"(1 - {nyc_share.oid}) * {nyc_ck.oid}", [nyc_share.oid, nyc_ck.oid],
                 "NYC non-staff operating cost per car-km, 2023 (2024 $)", "usd2")
SHARE = {}
for s in COMP_PEERS:
    comp = V(s, 2023, "staff_cost_per_employee")
    ratio(f"nyc_over_{s}_comp_2023", nyc_comp, comp, f"NYC 2023 staff cost per employee over {s} (PPP)", "x2")
    scope = "hk_transport_operations_all" if s == "hong_kong_mtr" else None
    sc, ot = V(s, 2023, "opex_staff_costs", scope), V(s, 2023, "opex_total", scope)
    sh = calc(f"staff_share_{s}_2023", sc.value / ot.value, f"{sc.oid} / {ot.oid}", [sc.oid, ot.oid],
              f"{s} staff cost as a share of operating cost, 2023", "pct")
    ck = V(s, 2023, "opex_per_car_km")
    lab = calc(f"labor_per_car_km_{s}_2023", sh * ck.value, f"staff_share_{s}_2023 * {ck.oid}",
               [sc.oid, ot.oid, ck.oid], f"{s} staff cost per car-km, 2023 (2024 $ PPP)", "usd2")
    calc(f"nonlabor_per_car_km_{s}_2023", (1 - sh) * ck.value, f"(1 - staff_share_{s}_2023) * {ck.oid}",
         [sc.oid, ot.oid, ck.oid], f"{s} non-staff cost per car-km, 2023 (2024 $ PPP)", "usd2")
    r_ = nyc_comp.value / comp.value
    cf = calc(f"nyc_carkm_at_{s}_pay_2023", nyc_lab_ck / r_ + nyc_nl_ck,
              f"nyc_labor_per_car_km_2023 / nyc_over_{s}_comp_2023 + nyc_nonlabor_per_car_km_2023",
              [nyc_share.oid, nyc_ck.oid, nyc_comp.oid, comp.oid],
              f"NYC 2023 cost per car-km if its own staff were paid {s}'s staff cost per employee (2024 $)", "usd2")
    calc(f"nyc_at_{s}_pay_over_{s}_2023", cf / ck.value, f"nyc_carkm_at_{s}_pay_2023 / {ck.oid}",
         [nyc_share.oid, nyc_ck.oid, nyc_comp.oid, comp.oid, ck.oid],
         f"NYC cost per car-km at {s} pay, divided by {s} cost per car-km", "x2")
    calc(f"pay_share_of_gap_{s}_2023", (nyc_ck.value - cf) / (nyc_ck.value - ck.value),
         f"({nyc_ck.oid} - nyc_carkm_at_{s}_pay_2023) / ({nyc_ck.oid} - {ck.oid})",
         [nyc_share.oid, nyc_ck.oid, nyc_comp.oid, comp.oid, ck.oid],
         f"Share of the NYC-{s} gap in cost per car-km that pay per employee accounts for, 2023", "pct")
    calc(f"nyc_over_{s}_labor_carkm_2023", nyc_lab_ck / lab, f"nyc_labor_per_car_km_2023 / labor_per_car_km_{s}_2023",
         [nyc_share.oid, nyc_ck.oid, sc.oid, ot.oid, ck.oid], f"NYC staff cost per car-km over {s}, 2023", "x1")
    calc(f"nyc_over_{s}_nonlabor_carkm_2023", nyc_nl_ck / ((1 - sh) * ck.value),
         f"nyc_nonlabor_per_car_km_2023 / nonlabor_per_car_km_{s}_2023",
         [nyc_share.oid, nyc_ck.oid, sc.oid, ot.oid, ck.oid], f"NYC non-staff cost per car-km over {s}, 2023", "x1")
    SHARE[s] = sh
tm_w, tm_b = V("tokyo_metro", 2023, "staff_wages_per_employee"), V("tokyo_metro", 2023, "staff_benefits_per_employee")
ratio("nyc_over_tokyo_metro_wages_2023", nyc_wage, tm_w, "NYC wages per employee over Tokyo Metro average salary, 2023")
ratio("nyc_over_tokyo_metro_benefits_2023", nyc_ben, tm_b, "NYC benefits per employee over Tokyo Metro (estimated), 2023")
calc("tokyo_metro_benefits_over_wages_2023", tm_b.value / tm_w.value, f"{tm_b.oid} / {tm_w.oid}", [tm_b.oid, tm_w.oid],
     "Tokyo Metro benefit cost as a share of average salary, 2023", "pct")
tm_c = V("tokyo_metro", 2023, "staff_cost_per_employee")
calc("benefit_share_of_comp_gap_tokyo_metro_2023", (nyc_ben.value - tm_b.value) / (nyc_comp.value - tm_c.value),
     f"({nyc_ben.oid} - {tm_b.oid}) / ({nyc_comp.oid} - {tm_c.oid})", [nyc_ben.oid, tm_b.oid, nyc_comp.oid, tm_c.oid],
     "Share of the NYC-Tokyo Metro gap in staff cost per employee that is benefits, 2023", "pct")

# ---- pay relative to each country's average wage (OECD), 2023, local currency
PPPF = {r["factor_id"]: float(r["value"]) for r in csv.DictReader(open(os.path.join(ROOT, "data/raw/ppp/ppp_deflator.csv"), encoding="utf-8"))}


def natwage(system, year):
    f = [x for x in FACTORS if x["system_id"] == system and x["factor_id"] == "national_avg_annual_wage" and x["as_of"] == str(year)][0]
    return float(f["value"]), f["fact_id"]


REL_PAY = {}
for s_, wid, cid in (("nyc_subway", "nyc_subway_2023_staff_wages_per_employee_ntd", "nyc_subway_2023_staff_cost_per_employee_ntd"),
                     ("tokyo_metro", "tokyo_metro_2023_staff_wages_per_employee_yuho", "tokyo_metro_2023_staff_cost_per_employee_mlit"),
                     ("tokyo_toei", None, "tokyo_toei_2023_staff_cost_per_employee_mlit")):
    nw, nfid = natwage(s_, 2023)
    if wid:
        calc(f"rel_wage_{s_}_2023", obs(wid).value / nw, f"{wid} / factors.csv {nfid}", [wid, nfid],
             f"{s_} wages per employee divided by the national average annual wage, 2023", "x2")
    REL_PAY[s_] = calc(f"rel_comp_{s_}_2023", obs(cid).value / nw, f"{cid} / factors.csv {nfid}", [cid, nfid],
                       f"{s_} wages plus benefits per employee divided by the national average annual wage, 2023", "x2")
for s_ in ("tokyo_metro", "tokyo_toei"):
    calc(f"rel_comp_nyc_over_{s_}_2023", REL_PAY["nyc_subway"] / REL_PAY[s_],
         f"rel_comp_nyc_subway_2023 / rel_comp_{s_}_2023",
         ["nyc_subway_2023_staff_cost_per_employee_ntd", obs(f"{s_}_2023_staff_cost_per_employee_mlit").oid],
         f"NYC pay relative to the US average wage, over {s_} pay relative to the Japanese average wage", "x2")
us_w, us_f = natwage("nyc_subway", 2023)
jp_w, jp_f = natwage("tokyo_metro", 2023)
us_real = us_w * PPPF["us_gdp_deflator_2024"] / PPPF["us_gdp_deflator_2023"]
jp_ppp = jp_w * PPPF["us_gdp_deflator_2024"] / PPPF["us_gdp_deflator_2023"] / PPPF["ppp_jpn_2023"]
calc("us_over_japan_avg_wage_ppp_2023", us_real / jp_ppp,
     f"{us_f} (2024 $) / ({jp_f} at ppp_jpn_2023, 2024 $)", [us_f, jp_f, "ppp_jpn_2023", "us_gdp_deflator_2023", "us_gdp_deflator_2024"],
     "US average annual wage over Japan's, at PPP, 2023", "x2")

sc_rows = [["**New York**", vstr(nyc_comp, "usd0"), vstr(nyc_wage, "usd0"), vstr(nyc_ben, "usd0"), "–",
            fmt(nyc_share.value, "pct"), fmt(nyc_lab_ck, "usd2"), fmt(nyc_nl_ck, "usd2"), "–"]]
for s in COMP_PEERS:
    comp = V(s, 2023, "staff_cost_per_employee")
    w_ = V(s, 2023, "staff_wages_per_employee")
    b_ = V(s, 2023, "staff_benefits_per_employee")
    e = " EST" if CALCS[f"labor_per_car_km_{s}_2023"]["estimate"] else ""
    lab_ = NAMES[s] + (" (all Hong Kong transport)" if s == "hong_kong_mtr" else "")
    sc_rows.append([lab_, vstr(comp, "usd0"), vstr(w_, "usd0"), vstr(b_, "usd0"),
                    fmt(CALCS[f"nyc_over_{s}_comp_2023"]["value"], "x2") + (" EST" if comp.est else ""),
                    fmt(SHARE[s], "pct"), fmt(CALCS[f"labor_per_car_km_{s}_2023"]["value"], "usd2") + e,
                    fmt(CALCS[f"nonlabor_per_car_km_{s}_2023"]["value"], "usd2") + e,
                    fmt(CALCS[f"nyc_carkm_at_{s}_pay_2023"]["value"], "usd2") + " (" +
                    fmt(CALCS[f"nyc_at_{s}_pay_over_{s}_2023"]["value"], "x2") + ")" +
                    (" EST" if CALCS[f"nyc_at_{s}_pay_over_{s}_2023"]["estimate"] else "")])
TABLES["staff_cost_2023"] = table(sc_rows, ["System (2023)", "Wages + benefits per employee", "of which wages",
                                            "of which benefits", "NYC ÷ system", "Staff cost share of operating cost",
                                            "Staff cost per car-km", "Other cost per car-km",
                                            "NYC cost per car-km at this system's pay"])

# US function table 2024
ft = []
for s in ["nyc_subway"] + USPEERS:
    ft.append([("**New York**" if s == "nyc_subway" else NAMES[s])] +
              [fmt(us_func[s][k], "n0") for k in FUNCS] +
              [fmt(CALCS[f"{s}_fm_per_dir_km_2024"]["value"], "n1"),
               fmt(CALCS[f"{s}_train_km_per_dir_km_2024"]["value"], "k"),
               fmt(CALCS[f"{s}_fm_cost_share_2024"]["value"], "pct")])
TABLES["us_functions_2024"] = table(ft, ["System (2024)", "Vehicle operations", "Vehicle maintenance",
                                         "Facility maintenance", "General admin",
                                         "Facility-maint. staff per directional route-km",
                                         "Train-km per directional route-km", "Facility maint. share of cost"])

# NYC trend table
tr = []
for y in range(2012, 2026):
    tr.append([str(y), vstr(V("nyc_subway", y, "opex_total"), "usdb"),
               vstr(V("nyc_subway", y, "opex_per_car_km"), "usd2"),
               vstr(V("nyc_subway", y, "opex_excl_ga_per_car_km"), "usd2"),
               vstr(V("nyc_subway", y, "opex_per_passenger_km"), "usd2"),
               vstr(V("nyc_subway", y, "farebox_recovery"), "pct")])
TABLES["nyc_trend"] = table(tr, ["Year", "Operating cost (2024 $)", "Cost per car-km", "Excl. admin",
                                 "Cost per passenger-km", "Farebox recovery"])

# Factors table
def fval(system, fid):
    rows = [f for f in FACTORS if f["system_id"] == system and f["factor_id"] == fid]
    rows.sort(key=lambda f: f["verification"] != "verified")
    return rows[0]["value"] if rows else "–"


fac = []
CREW = {"one_person": "one-person", "mostly_two_person": "**mostly two-person**",
        "mixed_two_and_one_person": "two-person on lines 1-4", "mixed_one_person_and_unattended": "one-person + driverless"}
NIGHT = {"24h_all_week": "**24/7**", "24h_weekends_some_lines": "weekend nights, some lines", "closes_nightly": "closes nightly"}
for s in ["nyc_subway", "london_underground", "paris_metro", "madrid_metro", "berlin_ubahn", "tokyo_metro", "tokyo_toei",
          "seoul_metro", "hong_kong_mtr", "singapore_mrt", "path"]:
    fac.append([("**New York**" if s == "nyc_subway" else NAMES[s]), fval(s, "opened_year"),
                CREW.get(fval(s, "crew_model"), fval(s, "crew_model") if fval(s, "crew_model") != "–" else "not recorded"),
                NIGHT.get(fval(s, "overnight_service"), "24/7 (unsourced note in systems.csv)" if s == "path" else "not recorded")])
TABLES["factors"] = table(fac, ["System", "Opened", "Crew on most trains", "Overnight service"])

# Reliability table
rl = []
def rel1(system, metric, period=None):
    rows = [r for r in REL if r["system_id"] == system and r["metric_id"] == metric and (period is None or r["period"] == period)]
    return rows
rl.append(["**New York**", fmt(float(nyc_mdbf["value"]), "n0") + " (2025)", "mechanical problem causing a delay",
           "94.2% (Dec 2024–Nov 2025, LTA compilation)"])
rl.append(["Hong Kong", f"{fmt(float(hk_mdbf[0]['value']), 'n0')} and {fmt(float(hk_mdbf[1]['value']), 'n0')} (2025, two line groups)",
           "train failure causing a delay of 5+ minutes", "99.9% (2025)"])
rl.append(["Singapore", fmt(float(sg_mdbf["value"]), "n0") + " (2025, LTA conversion from train-km)",
           "delay of more than 5 minutes", "99.8% (Dec 2025)"])
rl.append(["London", "not found", "–", "91.0% (2024/25, own series); 91.8% in the LTA compilation"])
rl.append(["Berlin", "not found", "–", "94.3% (2025, own figure)"])
TABLES["reliability"] = table(rl, ["System", "Car-km per failure", "What counts as a failure", "Scheduled service actually run"])

# ---------------------------------------------------------------- figures
def save(fig, name):
    fig.savefig(os.path.join(FIG, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def hbar(name, title, subtitle, items, f, xlabel, note=None):
    """items: list of (label, V or None, is_nyc, is_us)"""
    items = [i for i in items if i[1] is not None]
    items.sort(key=lambda i: i[1].value)
    fig, ax = plt.subplots(figsize=(7.2, 0.36 * len(items) + 1.5))
    ys = range(len(items))
    vmax = max((i[1].high or i[1].value) for i in items)
    for y, (lab, v, nyc, us) in zip(ys, items):
        col = NYC_C if nyc else (US_C if us else PEER_C)
        if v.est:
            ax.barh(y, v.value, height=0.62, color="white", edgecolor=col, hatch="////", linewidth=1.2)
            if v.low is not None and v.high is not None:
                ax.plot([v.low, v.high], [y, y], color="#191919", lw=1.2)
                ax.plot([v.low, v.low], [y - 0.15, y + 0.15], color="#191919", lw=1.2)
                ax.plot([v.high, v.high], [y - 0.15, y + 0.15], color="#191919", lw=1.2)
        else:
            ax.barh(y, v.value, height=0.62, color=col)
        txt = fmt(v.value, f) + ("  ESTIMATE" if v.est else "")
        xt = max(v.value, v.high or 0) + vmax * 0.015
        ax.text(xt, y, txt, va="center", fontsize=9, color="#191919",
                fontweight="bold" if (nyc or v.est) else "normal")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([i[0] for i in items])
    for t, i in zip(ax.get_yticklabels(), items):
        if i[2]:
            t.set_fontweight("bold")
    ax.set_xlim(0, vmax * 1.32)
    if f == "pct":
        from matplotlib.ticker import PercentFormatter
        ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(xlabel)
    fig.suptitle(title, x=0.02, ha="left", fontsize=12.5, fontweight="bold", y=0.995)
    ax.set_title(subtitle, loc="left", fontsize=9, color=TEXT2, pad=8)
    foot = "Hatched bar = ESTIMATE (rests on an assumption not in any source; whisker = low–high range). "
    foot += "Dark gray = foreign peers, light gray = US peers. "
    if note:
        foot += note
    fig.text(0.02, -0.01, foot, fontsize=7.5, color=TEXT2, ha="left", va="top", wrap=True)
    save(fig, name)


def items_for(year, metric, systems, label_year=False):
    out = []
    for s in systems:
        v = V(s, year, metric)
        if v is not None:
            out.append((NAMES[s] + (f" ({year})" if label_year else ""), v, s == "nyc_subway", s in US))
    return out


ALL = ["nyc_subway"] + FOREIGN + USPEERS
hbar("cost_per_passenger_km_2019.png", "Cost per passenger-km, 2019",
     "Operating cost per passenger-kilometre, 2024 US dollars (PPP for non-US systems)",
     items_for(2019, "opex_per_passenger_km", ALL), "usd2", "2024 US$ per passenger-km",
     "Tokyo 2019 passenger-km are estimated from the 2015-18 average trip length. No figure: Madrid, Seoul, Paris, Beijing, Berlin.")
hbar("cost_per_trip_2019.png", "Cost per trip, 2019",
     "Operating cost per trip (boarding or entry, as each system counts it), 2024 US dollars (PPP for non-US)",
     items_for(2019, "opex_per_trip", ALL), "usd2", "2024 US$ per trip",
     "Beijing is a secondary news figure with unstated definitions. Trip-counting rules differ: London, Madrid and Tokyo do not count line changes; NTD counts boardings.")
hbar("cost_per_car_km_2019.png", "Cost per car-km, 2019",
     "Operating cost per car-kilometre of service, 2024 US dollars (PPP for non-US systems)",
     items_for(2019, "opex_per_car_km", ALL), "usd2",
     "2024 US$ per car-km",
     "Cars differ in size (London's deep-tube cars are small), so read this with cost per train-km.")
hbar("cost_per_train_km_2023.png", "Cost per train-km, 2023",
     "Operating cost per train-kilometre, 2024 US dollars (PPP for non-US). Only systems that report train-km.",
     items_for(2023, "opex_per_train_km", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei"] + USPEERS),
     "usd0", "2024 US$ per train-km",
     "NYC trains average about 9 cars, Tokyo about 8, London about 7. Washington, Boston and PATH figures move a lot between years.")

# Scatter: cost per car-km vs passengers per car, 2019, with iso cost per passenger-km lines
fig, ax = plt.subplots(figsize=(7.2, 5.0))
pts = []
for s in ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei", "hong_kong_mtr"] + USPEERS:
    c, l = V(s, 2019, "opex_per_car_km"), V(s, 2019, "avg_car_load")
    if c and l:
        pts.append((s, l, c))
import numpy as np  # noqa: E402
xs = np.linspace(5, 85, 200)
ISO_POS = {0.80: (34.0, "left"), 0.40: (68.0, "left"), 0.20: (83.0, "right"), 0.10: (83.0, "right")}
for iso in (0.10, 0.20, 0.40, 0.80):
    ax.plot(xs, iso * xs, color="#d6d6d6", lw=1, zorder=1)
    xl, ha = ISO_POS[iso]
    ax.text(xl + (0.8 if ha == "left" else 0), iso * xl - (0.0 if ha == "left" else 1.4), f"${iso:.2f} per passenger-km",
            fontsize=7.5, color=TEXT2, ha=ha, va="center")
OFF = {"wmata_metrorail": (-8, 6, "right"), "mbta_subway": (6, 4, "left"), "chicago_l": (-8, -10, "right"),
       "bart": (6, -10, "left"), "septa_subway": (6, -4, "left"), "london_underground": (-8, 6, "right"),
       "tokyo_toei": (-8, 6, "right"), "hong_kong_mtr": (6, -10, "left"), "tokyo_metro": (-8, 8, "right"),
       "nyc_subway": (7, 5, "left"), "path": (7, 0, "left")}
for s, l, c in pts:
    nyc = s == "nyc_subway"
    col = NYC_C if nyc else (US_C if s in US else PEER_C)
    est = l.est or c.est
    ax.scatter(l.value, c.value, s=70 if nyc else 46, color="white" if est else col, edgecolor=col if est else "white",
               linewidth=1.6 if est else 1.5, zorder=3)
    lab = NAMES[s] + (" (EST)" if est else "")
    dx, dy, ha = OFF.get(s, (6, 4, "left"))
    ax.annotate(lab, (l.value, c.value), xytext=(dx, dy), textcoords="offset points", fontsize=8.5, ha=ha,
                fontweight="bold" if nyc else "normal", color="#191919")
ax.set_xlim(0, 85)
ax.set_ylim(0, 28)
ax.set_xlabel("Average passengers on board per car (passenger-km ÷ car-km)")
ax.set_ylabel("Cost per car-km, 2024 US$")
fig.suptitle("Asian metros are cheap per passenger mainly because their cars are full",
             x=0.02, ha="left", fontsize=12, fontweight="bold", y=1.0)
ax.set_title("2019. Gray lines join points of equal cost per passenger-km. NYC costs more per car-km than any foreign peer.",
             loc="left", fontsize=9, color=TEXT2)
fig.text(0.02, -0.01, "Hollow marker = depends on an ESTIMATE (London car-km, Hong Kong cost, Tokyo 2019 passenger-km). "
         "Dark gray = foreign peers, light gray = US peers.", fontsize=7.5, color=TEXT2, ha="left", va="top")
save(fig, "cost_vs_load_2019.png")

# Staff per million car-km
hbar("staff_per_car_km_2023.png", "Staff per million car-km, 2023",
     "Operating employees per million car-km (head counts; London is FTE)",
     items_for(2023, "employees_per_million_car_km", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei",
                                                      "hong_kong_mtr"] + USPEERS)
     + [("Seoul (2019)", V("seoul_metro", 2019, "employees_per_million_car_km"), False, False),
        ("Madrid (2018)", V("madrid_metro", 2018, "employees_per_million_car_km"), False, False)],
     "n1", "Employees per million car-km",
     "Seoul counts every employee of the corporation. Madrid is a company head count.")

hbar("passenger_km_per_staff_2023.png", "Passenger-km per employee, 2023",
     "Passenger-kilometres carried per operating employee (thousands)",
     items_for(2023, "passenger_km_per_employee", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei",
                                                   "hong_kong_mtr"] + USPEERS), "k", "Passenger-km per employee")

# Staff cost per employee, wages and benefits stacked
fig, ax = plt.subplots(figsize=(7.2, 2.9))
rows_ = [("New York", nyc_wage, nyc_ben, nyc_comp, True),
         ("Tokyo Metro", V("tokyo_metro", 2023, "staff_wages_per_employee"),
          V("tokyo_metro", 2023, "staff_benefits_per_employee"), V("tokyo_metro", 2023, "staff_cost_per_employee"), False),
         ("Toei (Tokyo)", None, None, V("tokyo_toei", 2023, "staff_cost_per_employee"), False),
         ("Hong Kong (all transport)", None, None, V("hong_kong_mtr", 2023, "staff_cost_per_employee"), False)]
rows_ = rows_[::-1]
LIGHT = {True: "#9cc4f0", False: "#c9c9c9"}
for y, (lab, w_, b_, tot, nyc) in enumerate(rows_):
    col = NYC_C if nyc else PEER_C
    if w_ is not None:
        ax.barh(y, w_.value, height=0.62, color=col)
        if b_.est:
            ax.barh(y, b_.value, left=w_.value, height=0.62, color="white", edgecolor=col, hatch="////", lw=1.2)
        else:
            ax.barh(y, b_.value, left=w_.value, height=0.62, color=LIGHT[nyc])
        ax.text(w_.value / 2, y, "wages", ha="center", va="center", fontsize=8, color="white")
        if not b_.est:
            ax.text(w_.value + b_.value / 2, y, "benefits", ha="center", va="center", fontsize=8, color="#191919")
    elif tot.est:
        ax.barh(y, tot.value, height=0.62, color="white", edgecolor=col, hatch="////", lw=1.2)
        ax.plot([tot.low, tot.high], [y, y], color="#191919", lw=1.2)
        for xx in (tot.low, tot.high):
            ax.plot([xx, xx], [y - 0.15, y + 0.15], color="#191919", lw=1.2)
    else:
        ax.barh(y, tot.value, height=0.62, color=col)
    extra = "  ESTIMATE" if tot.est else ("  (hatched benefits = ESTIMATE)" if b_ is not None and b_.est else "")
    ax.text(tot.value + 3000, y, f"${tot.value / 1000:,.0f}k" + extra, va="center",
            fontsize=9, fontweight="bold" if (nyc or tot.est) else "normal")
ax.set_yticks(range(len(rows_)))
ax.set_yticklabels([r[0] for r in rows_])
ax.get_yticklabels()[-1].set_fontweight("bold")
ax.set_xlim(0, nyc_comp.value * 1.35)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"${x / 1000:,.0f}k"))
ax.grid(axis="y", visible=False)
ax.set_xlabel("Wages and benefits per employee, 2024 US dollars at PPP")
fig.suptitle("Each NYC subway worker costs about 1.65 times as much", x=0.02, ha="left", fontsize=12.5,
             fontweight="bold", y=1.04)
ax.set_title("2023. Own staff only; contracted-out work is not included. Toei and Hong Kong do not split wages and benefits.",
             loc="left", fontsize=9, color=TEXT2)
fig.text(0.02, -0.12, "Hatched = ESTIMATE (whisker = low–high range). Hong Kong covers MTR's whole Hong Kong transport "
         "business, and its staff cost may include staff its head count leaves out. NYC benefits include pensions and "
         "retiree health care as booked (accrual).", fontsize=7.5, color=TEXT2, ha="left", va="top", wrap=True)
save(fig, "staff_cost_per_employee_2023.png")

# Farebox
fb_items = items_for(2019, "farebox_recovery", ["nyc_subway", "london_underground", "tokyo_metro", "tokyo_toei",
                                                "seoul_metro"] + USPEERS)
hk = V("hong_kong_mtr", 2019, "farebox_recovery")
fb_items.append(("Hong Kong (all transport)", hk, False, False))
hbar("farebox_recovery_2019.png", "Farebox recovery, 2019",
     "Fare revenue as a share of operating cost (above 100% = fares cover all operating cost)",
     fb_items, "pct", "Fare revenue ÷ operating cost",
     "Hong Kong covers MTR's whole Hong Kong transport business, not heavy rail alone. Tokyo excludes depreciation, like NTD.")

# US staff by function per million train-km, stacked
fig, ax = plt.subplots(figsize=(7.2, 3.9))
order = sorted(["nyc_subway"] + USPEERS, key=lambda s: sum(us_func[s].values()))
labels_f = ["Vehicle operations", "Vehicle maintenance", "Facility maintenance", "General administration"]
for i, s in enumerate(order):
    left = 0
    for k, col in zip(FUNCS, SERIES):
        w = us_func[s][k]
        ax.barh(i, w, left=left, color=col, height=0.62, edgecolor="white", linewidth=2)
        left += w
    ax.text(left + 6, i, fmt(left, "n0"), va="center", fontsize=9, fontweight="bold" if s == "nyc_subway" else "normal")
ax.set_yticks(range(len(order)))
ax.set_yticklabels([NAMES[s] for s in order])
for t, s in zip(ax.get_yticklabels(), order):
    if s == "nyc_subway":
        t.set_fontweight("bold")
ax.grid(axis="y", visible=False)
ax.set_xlabel("Operating employees per million train-km")
ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in SERIES], labels_f, ncol=4, fontsize=8, frameon=False,
          loc="upper left", bbox_to_anchor=(0, -0.18))
fig.suptitle("NYC's extra staff are in facility maintenance, not on the trains", x=0.02, ha="left",
             fontsize=12, fontweight="bold", y=1.03)
ax.set_title("US heavy-rail systems, 2024, NTD. Facility maintenance = track, structures, stations, signals and power.",
             loc="left", fontsize=9, color=TEXT2)
save(fig, "us_staff_by_function_2024.png")

# NYC trend
fig, ax = plt.subplots(figsize=(7.2, 3.8))
yrs = list(range(2012, 2026))
a = [V("nyc_subway", y, "opex_per_car_km") for y in yrs]
b = [V("nyc_subway", y, "opex_excl_ga_per_car_km") for y in yrs]
ax.plot(yrs, [v.value for v in a], color=SERIES[0], lw=2, marker="o", ms=4)
yb = [y for y, v in zip(yrs, b) if v]
ax.plot(yb, [v.value for v in b if v], color=SERIES[1], lw=2, marker="o", ms=4)
ax.text(2025.2, a[-1].value, "All costs", va="center", fontsize=9)
ax.text(2025.2, b[-1].value, "Excluding general\nadministration", va="center", fontsize=9)
ax.axvspan(2019.5, 2022.5, color="#f4f4f4", zorder=0)
ax.text(2021, 6.6, "pandemic years", ha="center", fontsize=8, color=TEXT2)
ax.set_ylim(6, 14)
ax.set_xlim(2011.5, 2027.3)
ax.set_ylabel("Cost per car-km, 2024 US$")
ax.legend(["All costs", "Excluding general administration"], frameon=False, fontsize=8, loc="upper left", ncol=2)
fig.suptitle("NYC's real cost per car-km has been flat for a decade", x=0.02, ha="left", fontsize=12, fontweight="bold", y=1.03)
ax.set_xticks(range(2012, 2026, 2))
ax.set_title("NYC subway, NTD, 2024 dollars (US GDP deflator). 2012 is a possible series break. Admin rose sharply in 2023-24.",
             loc="left", fontsize=9, color=TEXT2)
save(fig, "nyc_cost_per_car_km_trend.png")

# Reliability (log scale)
fig, ax = plt.subplots(figsize=(7.2, 2.6))
rel_items = [("New York (2025)", float(nyc_mdbf["value"]), NYC_C),
             ("Hong Kong, line group A (2025)", float(hk_mdbf[0]["value"]), PEER_C),
             ("Singapore (2025)", float(sg_mdbf["value"]), PEER_C),
             ("Hong Kong, line group B (2025)", float(hk_mdbf[1]["value"]), PEER_C)]
for i, (lab, v, c) in enumerate(rel_items):
    ax.barh(i, v, color=c, height=0.6)
    ax.text(v * 1.12, i, f"{v / 1e6:.2f} million" if v > 1e6 else f"{v / 1e3:.0f} thousand", va="center", fontsize=9)
ax.set_xscale("log")
ax.set_xlim(5e4, 6e7)
ax.set_xticks([1e5, 1e6, 1e7])
ax.set_xticklabels(["100 thousand", "1 million", "10 million"])
ax.minorticks_off()
ax.set_yticks(range(len(rel_items)))
ax.set_yticklabels([r[0] for r in rel_items])
ax.get_yticklabels()[0].set_fontweight("bold")
ax.grid(axis="y", visible=False)
ax.set_xlabel("Car-km between delay-causing failures (log scale)")
fig.suptitle("NYC trains break down 25 to 40 times as often", x=0.02, ha="left", fontsize=12, fontweight="bold", y=1.04)
ax.set_title("Each agency's own definition of a failure; Hong Kong and Singapore count delays of 5+ minutes.",
             loc="left", fontsize=9, color=TEXT2)
save(fig, "mdbf_2025.png")

# ---------------------------------------------------------------- numbers.csv
with open(os.path.join(REPORT, "numbers.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["calc_id", "value", "formatted", "estimate", "formula", "inputs", "description"],
                       lineterminator="\n")
    w.writeheader()
    for c in sorted(CALCS.values(), key=lambda c: c["calc_id"]):
        w.writerow(dict(calc_id=c["calc_id"], value=f"{c['value']:.6g}", formatted=fmt(c["value"], c["fmt"]),
                        estimate="yes" if c["estimate"] else "no", formula=c["formula"], inputs=c["inputs"],
                        description=c["description"]))

# ---------------------------------------------------------------- render template
tpl_path = os.path.join(REPORT, "report_template.md")
if os.path.exists(tpl_path):
    tpl = open(tpl_path, encoding="utf-8").read()
    used = []

    def sub(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "v":
            s, y, metric, f = arg.split(":")
            v = V(s, int(y), metric)
            if v is None:
                raise KeyError(arg)
            used.append(v.oid)
            return vstr(v, f, bold_est=False)
        if kind == "c":
            c = CALCS[arg]
            return fmt(c["value"], c["fmt"]) + (" EST" if c["estimate"] else "")
        if kind == "t":
            return TABLES[arg]
        if kind == "fig":
            file, alt = arg.split(":", 1)
            assert os.path.exists(os.path.join(FIG, file)), file
            return f"![{alt}](figures/{file})"
        raise ValueError(kind)

    out = re.sub(r"\{\{(v|c|t|fig):([^}]+)\}\}", sub, tpl)
    open(os.path.join(REPORT, "report.md"), "w", encoding="utf-8").write(
        "<!-- Generated by scripts/build_report.py from report/report_template.md. Edit the template, not this file. -->\n" + out)
    print(f"rendered report.md ({len(used)} dataset values)")
print(f"{len(CALCS)} computed numbers, {len(TABLES)} tables, figures in report/figures")
