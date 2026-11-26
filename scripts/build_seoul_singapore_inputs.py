#!/usr/bin/env python3
"""Write data/peers/seoul_metro.csv and data/peers/singapore_mrt.csv.

Both systems have thin public data (see docs/peers/asia.md). Reported values
are entered below with their locators; costs are ESTIMATES with methods
seoul_opex_excl_depreciation, seoul_car_km_from_train_km and
smrt_opex_from_revenue_ebit.
Run from the repository root, then scripts/build_peers.py and scripts/validate.py.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["obs_id", "system_id", "year", "year_basis", "metric_id", "value",
          "value_low", "value_high", "unit", "currency", "price_basis", "scope",
          "value_type", "verification", "source_id", "source_locator",
          "method_id", "inputs", "notes"]


def fmt(x):
    return str(int(round(x))) if abs(x) >= 1e5 else f"{x:.6g}"


def row(**k):
    r = {f: "" for f in FIELDS}
    r["verification"] = "unverified"
    r.update(k)
    return r


def write(sid, rows):
    rows.sort(key=lambda r: (int(r["year"]), r["metric_id"], r["obs_id"]))
    p = ROOT / "data" / "peers" / f"{sid}.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{p.relative_to(ROOT)}: {len(rows)} rows")


# ---------------- Seoul Metro ----------------
SEOUL_SRC = "seoul_metro_settlement_2019"
# year -> values (won, thousand trips, thousand train-km, km, count)
SEOUL = {
    2019: dict(opex=2537047141797, consign=74284435408, fare=1636749394102, trips=2671426,
               train_km=40073, route_km=300.3, stations=278, staff=16854, cars=3551, sets=405, col="당기 (2019)", ucol="2019"),
    2018: dict(opex=2518725548781, consign=63523181341, fare=1623423023974, trips=2642441,
               train_km=41070, route_km=300.1, stations=277, staff=16956, cars=3570, sets=423, col="전기 (2018)", ucol="2018"),
}
# Depreciation is not readable in the source for 2019; estimate range (won).
SEOUL_DEP = (370e9, 300e9, 450e9)
# Share of train-km run empty (회송) and so not revenue service.
SEOUL_DEADHEAD = (0.04, 0.02, 0.07)


def seoul():
    sid, scope, out = "seoul_metro", "whole_agency_less_contract_work", []
    for y, v in SEOUL.items():
        def rep(metric, value, unit, loc, tag="sm", cur="", note="", sc=scope):
            oid = f"{sid}_{y}_{metric}_{tag}"
            out.append(row(obs_id=oid, system_id=sid, year=y, year_basis="calendar", metric_id=metric,
                           value=fmt(value), unit=unit, currency=cur, price_basis="nominal" if cur else "",
                           scope=sc, value_type="reported", source_id=SEOUL_SRC, source_locator=loc, notes=note))
            return oid
        pl = "손익계산서 pp.28-32, {} column, row '{}' (원)"
        o1 = rep("opex_incl_depreciation", v["opex"], "KRW", "사업수익·사업비용 summary p.17, 영업비용, " + v["col"] + " (원); equals 매출원가 + 판매비와관리비 on pp.28-32", cur="KRW",
                 note="Whole corporation: includes depreciation, contract work for others (수탁사업원가) and ancillary businesses.", sc="whole_agency")
        o2 = rep("opex_other_business", v["consign"], "KRW", pl.format(v["col"], "매출원가 2. 수탁사업원가"), cur="KRW",
                 note="Construction and operation done under contract for others (for example Line 9 phase 2-3 and extensions); revenue equals cost.", sc="whole_agency")
        rep("fare_revenue", v["fare"], "KRW", pl.format(v["col"], "매출액 1. 운수사업수익"), cur="KRW",
            note="Transport revenue of the corporation (lines 1-8 fares after settlement with other operators).")
        tr = rep("unlinked_trips", v["trips"] * 1000, "trips", f"사업보고서 2.가 업무량, p.16, row 수송인원, column 계 ({v['ucol']}) (천명; multiplied by 1,000)",
                 note="Lines 1-8. Seoul Metro counts entries plus transfers in from other operators' lines (승차인원+환승인원, see seoul_city_subway_overview_2025), close to NTD boardings; transfers between its own lines are not counted again.")
        tk = rep("train_km", v["train_km"] * 1000, "km", f"사업보고서 2.가 업무량, p.16, row 열차주행키로, column 계 ({v['ucol']}) (천km; multiplied by 1,000)",
                 note="Includes empty running (회송포함), so it is slightly more than revenue train-km. Kept in its own scope so no ratio uses it directly.", tag="smgross", sc="lines_1_8_incl_empty_running")
        rep("route_km", v["route_km"], "km", f"사업보고서 2.가 업무량, p.16, row 영업연장, column 계 ({v['ucol']})")
        rep("stations", v["stations"], "count", f"사업보고서 2.가 업무량, p.16, row 역수, column 계 ({v['ucol']})")
        rep("employees_fte", v["staff"], "employees", f"사업보고서 2.마 직원 현황, p.14, 현원, {'당년도말' if y == 2019 else '전년도말'}",
            note="Head count at year end (현원) of the whole corporation, excluding non-standing board members. Includes staff on contract work and ancillary businesses (a few percent). Not FTE.")
        # estimated opex excluding depreciation and contract work
        dep, dlo, dhi = SEOUL_DEP
        base = v["opex"] - v["consign"] - dep
        out.append(row(obs_id=f"{sid}_{y}_opex_total_est", system_id=sid, year=y, year_basis="calendar",
                       metric_id="opex_total", value=fmt(base), value_low=fmt(v["opex"] - v["consign"] - dhi),
                       value_high=fmt(v["opex"] - v["consign"] - dlo), unit="KRW", currency="KRW", price_basis="nominal",
                       scope=scope, value_type="estimated", source_id=SEOUL_SRC,
                       source_locator="Computed from the input rows listed in inputs and the depreciation range in the method note",
                       method_id="seoul_opex_excl_depreciation", inputs=f"{o1};{o2}",
                       notes="ESTIMATE. 영업비용 minus contract work minus depreciation; depreciation is not in the readable part of the source and is assumed to be 300-450 billion won."))
        cpt = v["cars"] / v["sets"]
        d, dl, dh = SEOUL_DEADHEAD
        out.append(row(obs_id=f"{sid}_{y}_car_km_est", system_id=sid, year=y, year_basis="calendar",
                       metric_id="car_km", value=fmt(v["train_km"] * 1000 * cpt * (1 - d)),
                       value_low=fmt(v["train_km"] * 1000 * cpt * (1 - dh) * 0.97),
                       value_high=fmt(v["train_km"] * 1000 * cpt * (1 - dl) * 1.02),
                       unit="km", scope=scope, value_type="estimated", source_id=SEOUL_SRC,
                       source_locator=f"Train-km from the input row; cars per train from 사업보고서 2.가 업무량 p.16, row 전동차(편성), {v['cars']}({v['sets']})",
                       method_id="seoul_car_km_from_train_km", inputs=tk,
                       notes=f"ESTIMATE. Train-km x average cars per train set ({cpt:.2f}) x (1 - share of empty running, 2-7%)."))
    seoul_later(sid, out)
    write(sid, out)


# Later years from secondary sources (see docs/peers/asia.md).
# sankun_seoul_metro_financials: 재무정보 table (백만원), 매출액 and 영업이익.
SEOUL_LATER_FIN = {2022: (1768373, -934513), 2023: (1870727, -845201), 2024: (2068193, -945492)}
# Assumed ranges (won) for 2022-2024: contract work and depreciation; see method seoul_opex_from_revenue_operating_loss.
SEOUL_LATER_CONSIGN = (70e9, 40e9, 110e9)
SEOUL_LATER_DEP = (410e9, 340e9, 480e9)
# 2024 transport statistics, seoul_mediahub_2025_ridership_2024.
SEOUL_2024 = dict(trips=2417520000, train_km=42040917, stations=273)


def seoul_later(sid, out):
    scope = "whole_agency_less_contract_work"
    src = "sankun_seoul_metro_financials"
    for y, (rev, oi) in SEOUL_LATER_FIN.items():
        loc = "재무정보 table (단위: 백만원), column '{}년 12월', row '{}' (multiplied by 1,000,000)"
        r = f"{sid}_{y}_operating_revenue_sankun"
        e = f"{sid}_{y}_ebit_sankun"
        note = "Secondary (aggregator page citing public disclosures). Whole corporation, including contract work and ancillary businesses."
        out.append(row(obs_id=r, system_id=sid, year=y, year_basis="calendar", metric_id="operating_revenue",
                       value=fmt(rev * 1e6), unit="KRW", currency="KRW", price_basis="nominal", scope="whole_agency",
                       value_type="reported", source_id=src, source_locator=loc.format(y, "매출액"), notes=note))
        out.append(row(obs_id=e, system_id=sid, year=y, year_basis="calendar", metric_id="ebit",
                       value=fmt(oi * 1e6), unit="KRW", currency="KRW", price_basis="nominal", scope="whole_agency",
                       value_type="reported", source_id=src, source_locator=loc.format(y, "영업이익"),
                       notes=note + " Operating income (영업이익); negative is an operating loss."))
        gross = (rev - oi) * 1e6
        c, clo, chi = SEOUL_LATER_CONSIGN
        d, dlo, dhi = SEOUL_LATER_DEP
        out.append(row(obs_id=f"{sid}_{y}_opex_total_est", system_id=sid, year=y, year_basis="calendar",
                       metric_id="opex_total", value=fmt(gross - c - d), value_low=fmt(gross - chi - dhi),
                       value_high=fmt(gross - clo - dlo), unit="KRW", currency="KRW", price_basis="nominal",
                       scope=scope, value_type="estimated", source_id=src,
                       source_locator="Computed from the input rows listed in inputs and the ranges in the method note",
                       method_id="seoul_opex_from_revenue_operating_loss", inputs=f"{r};{e}",
                       notes="ESTIMATE. (매출액 - 영업이익) minus assumed contract work (40-110 billion won) minus assumed depreciation (340-480 billion won). Inputs are from a secondary source."))
    y, v, src = 2024, SEOUL_2024, "seoul_mediahub_2025_ridership_2024"
    out.append(row(obs_id=f"{sid}_{y}_unlinked_trips_mh", system_id=sid, year=y, year_basis="calendar",
                   metric_id="unlinked_trips", value=fmt(v["trips"]), unit="trips", scope=scope,
                   value_type="reported", source_id=src,
                   source_locator="Article body, sentence '수송 인원은 전년 대비 2.5% 늘어난 총 24억 1,752만 명' (24억 1,752만 = 2,417,520,000)",
                   notes="Lines 1-8, 2024 transport statistics of Seoul Metro as published by the city. Assumed to use the same counting rule (entries plus transfers in) as the 2018-2019 수송인원."))
    tk = f"{sid}_{y}_train_km_mh"
    out.append(row(obs_id=tk, system_id=sid, year=y, year_basis="calendar", metric_id="train_km",
                   value=fmt(v["train_km"]), unit="km", scope="lines_1_8_incl_empty_running", value_type="reported",
                   source_id=src, source_locator="Article body, sentence '총 160만 499회 운행하며 4,204만 917km를 달렸다' (4,204만 917km = 42,040,917 km)",
                   notes="Distance run by trains on lines 1-8. Assumed to include empty running, like 열차주행키로 in 2018-2019."))
    out.append(row(obs_id=f"{sid}_{y}_stations_mh", system_id=sid, year=y, year_basis="calendar", metric_id="stations",
                   value="273", unit="count", scope=scope, value_type="reported", source_id=src,
                   source_locator="Article body, sentence '서울 지하철 1~8호선 273개 역 중'"))
    # Car-km: 2019 cars per set, wider range because the 2024 fleet is not in the source.
    cpt = SEOUL[2019]["cars"] / SEOUL[2019]["sets"]
    d, dl, dh = SEOUL_DEADHEAD
    out.append(row(obs_id=f"{sid}_{y}_car_km_est", system_id=sid, year=y, year_basis="calendar",
                   metric_id="car_km", value=fmt(v["train_km"] * cpt * (1 - d)),
                   value_low=fmt(v["train_km"] * cpt * (1 - dh) * 0.95),
                   value_high=fmt(v["train_km"] * cpt * (1 - dl) * 1.03),
                   unit="km", scope=scope, value_type="estimated", source_id=SEOUL_SRC,
                   source_locator=f"Train-km from the input row; cars per train set from the 2019 사업보고서 2.가 업무량 p.16, row 전동차(편성), {SEOUL[2019]['cars']}({SEOUL[2019]['sets']})",
                   method_id="seoul_car_km_from_train_km", inputs=tk,
                   notes=f"ESTIMATE. 2024 train-km x 2019 average cars per train set ({cpt:.2f}) x (1 - share of empty running, 2-7%); range widened by -5%/+3% because the 2024 fleet mix is not in a source."))
    # Press figure: 2025 cost per passenger, Seoul Metro's own definition.
    out.append(row(obs_id=f"{sid}_2025_opex_per_trip_mt", system_id=sid, year=2025, year_basis="calendar",
                   metric_id="opex_per_trip", value="1817", unit="KRW/trip", currency="KRW", price_basis="nominal",
                   scope="seoul_metro_press_cost_per_passenger", value_type="reported", source_id="mt_2026_seoul_metro_loss",
                   source_locator="Article body: Seoul Metro's 2025 cost per passenger carried, 1,817원 (against an average fare of 1,036원)",
                   notes="Secondary (news report of Seoul Metro's own figure). The article does not say what the cost includes (it may include depreciation and interest), so it is not directly comparable with opex_total-based cost per trip. Kept in its own scope."))


# ---------------- Singapore SMRT Trains ----------------
# year = calendar year in which the April-March financial year starts.
SMRT = {
    2014: dict(src="smrt_ar_2016", page="pp.34-35", fy="FY2015", rev=644.2, ebit=13.4),
    2015: dict(src="smrt_ar_2016", page="pp.34-35", fy="FY2016", rev=670.2, ebit=12.0),
    2021: dict(src="smrt_group_review_2324", page="pp.35-36", fy="FY21/22", rev=645.5, ebit=16.0,
               car_km=142, trips=480, pkm=4914, route=137, lines="North-South, East-West and Circle lines"),
    2022: dict(src="smrt_group_review_2324", page="pp.35-36", fy="FY22/23", rev=813.2, ebit=6.1,
               car_km=143, trips=636, pkm=6625, route=137, lines="North-South, East-West and Circle lines"),
    2023: dict(src="smrt_group_review_2324", page="pp.35-36", fy="FY23/24", rev=886.7, ebit=6.2,
               car_km=158, trips=717, pkm=7772, route=167, lines="North-South, East-West, Circle and Thomson-East Coast lines"),
}


def singapore():
    sid, scope, out = "singapore_mrt", "smrt_trains_heavy_rail", []
    for y, v in SMRT.items():
        def rep(metric, value, unit, loc, cur="", note=""):
            oid = f"{sid}_{y}_{metric}_smrt"
            out.append(row(obs_id=oid, system_id=sid, year=y, year_basis="fiscal_apr_mar", metric_id=metric,
                           value=fmt(value), unit=unit, currency=cur, price_basis="nominal" if cur else "",
                           scope=scope, value_type="reported", source_id=v["src"], source_locator=loc, notes=note))
            return oid
        if "car_km" not in v:
            # Annual report FY2016: Train (MRT) segment, chart labels; revenue confirmed in text p.35.
            loc = f"Group Performance, Rail Business, Train revenue and EBIT chart labels, {v['page']}, {v['fy']} (S$ million; multiplied by 1,000,000)"
            r = rep("operating_revenue", v["rev"] * 1e6, "SGD", loc, "SGD",
                    "SMRT Train (MRT: North-South, East-West and Circle lines) revenue, excluding the Bukit Panjang LRT. Read from chart labels; FY2016 value also in text p.35 ('Revenue from Train operations increased by $26.0 million or 4.0% to $670.2 million').")
            e = rep("ebit", v["ebit"] * 1e6, "SGD", loc, "SGD",
                    "Train EBIT, read from chart labels. FY2016 includes a net property tax refund of S$16.4 million; text p.35 says Train operations would have lost S$4.4 million without it.")
            base = (v["rev"] - v["ebit"]) * 1e6
            out.append(row(obs_id=f"{sid}_{y}_opex_total_est", system_id=sid, year=y, year_basis="fiscal_apr_mar",
                           metric_id="opex_total", value=fmt(base), value_low=fmt(base * 0.80), value_high=fmt(base * 1.10),
                           unit="SGD", currency="SGD", price_basis="nominal", scope=scope, value_type="estimated",
                           source_id=v["src"], source_locator="Computed from the input rows listed in inputs",
                           method_id="smrt_opex_from_revenue_ebit", inputs=f"{r};{e}",
                           notes="ESTIMATE. Revenue minus EBIT. Before the 2016 transfer of rail assets to LTA, SMRT owned its trains, so depreciation is a larger share than in later years (covered by the low end)."))
            continue
        fin = f"SMRT Trains' Key Financial Data, {v['page']}, row {v['fy']}, column '{{}}' (S$ million; multiplied by 1,000,000)"
        opr = f"SMRT Trains Key Operating Data, {v['page']}, column {v['fy']}, row '{{}}'"
        r = rep("operating_revenue", v["rev"] * 1e6, "SGD", fin.format("Revenue ($M)"), "SGD",
                "SMRT Trains Ltd revenue: fares plus other income it books as revenue. Under the New Rail Financing Framework the government (LTA) owns the trains and network and the operator pays licence charges.")
        e = rep("ebit", v["ebit"] * 1e6, "SGD", fin.format("Earning Before Interest and Tax ($M)"), "SGD")
        ck = rep("car_km", v["car_km"] * 1e6, "km", opr.format("Total car-kilometres operated (to nearest million)") + " (million; multiplied by 1,000,000)",
                 note=f"{v['lines']}. Rounded to the nearest million in the source.")
        rep("unlinked_trips", v["trips"] * 1e6, "trips", opr.format("Total annual ridership (to nearest million)") + " (million; multiplied by 1,000,000)",
            note=f"{v['lines']}. Counting rule for transfers between lines and operators not stated.")
        rep("passenger_km", v["pkm"] * 1e6, "km", opr.format("Total passenger-kilometres (to nearest million)") + " (million; multiplied by 1,000,000)")
        rep("route_km", v["route"], "km", opr.format("Total route length (to nearest kilometres)"))
        base = (v["rev"] - v["ebit"]) * 1e6
        hi = 1.25 if y == 2023 else 1.10
        out.append(row(obs_id=f"{sid}_{y}_opex_total_est", system_id=sid, year=y, year_basis="fiscal_apr_mar",
                       metric_id="opex_total", value=fmt(base), value_low=fmt(base * 0.80), value_high=fmt(base * hi),
                       unit="SGD", currency="SGD", price_basis="nominal", scope=scope, value_type="estimated",
                       source_id=v["src"], source_locator="Computed from the input rows listed in inputs",
                       method_id="smrt_opex_from_revenue_ebit", inputs=f"{r};{e}",
                       notes="ESTIMATE. Revenue minus EBIT. Includes licence charges and depreciation of operator assets (removed in the low end) and nets off other operating income (added in the high end)."))
    write(sid, out)


if __name__ == "__main__":
    seoul()
    singapore()
