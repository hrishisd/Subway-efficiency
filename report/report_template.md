# How efficient is the New York City subway? Operating cost, productivity and reliability compared with peer metros

*Research report, 26 November 2026. Built from the dataset in this repository. Scope: operating cost, staff productivity and reliability. Capital and expansion costs are out of scope.*

> **How to read the numbers.** Money is in **2024 US dollars**. US systems are converted with the US GDP deflator. Foreign systems are converted at **purchasing power parity (PPP)** for their year, then to 2024 dollars. Values marked **EST** are **estimates**: they rest on at least one assumption that is not in any published source. Each estimate has a written method in [`methods/`](../methods/) and a low–high range, shown in brackets in the tables and as a whisker on the charts. In the charts, estimates are hatched bars or hollow markers. Section 6 repeats the main results with every estimate left out.

---

## Executive summary

**The short answer.** Per unit of service, the NYC subway is the most expensive large metro in this study. Per rider, it is about as expensive as London, cheaper than most US systems, and three to four times as expensive as Tokyo and Hong Kong. Most of the per-rider gap with Asia comes from how full the trains are, not from how much a train costs to run. But NYC also has a real production-cost gap: it spent about 10% (Madrid) to 70% (Hong Kong) more per car-km than its foreign peers in 2019, and 35% to 75% more in 2023, and its staffing is concentrated in maintenance of track, stations and other facilities.

1. **Cost per passenger-km (2019, before the pandemic):** NYC {{v:nyc_subway:2019:opex_per_passenger_km:usd2}}. London {{v:london_underground:2019:opex_per_passenger_km:usd2}}. Tokyo Metro {{v:tokyo_metro:2018:opex_per_passenger_km:usd2}} (2018, the last year with reported passenger-km). Toei {{v:tokyo_toei:2018:opex_per_passenger_km:usd2}} (2018). Hong Kong {{v:hong_kong_mtr:2019:opex_per_passenger_km:usd2}}. US heavy-rail peers ranged from {{v:bart:2019:opex_per_passenger_km:usd2}} (BART) to {{v:path:2019:opex_per_passenger_km:usd2}} (PATH).
2. **Cost per trip (2019):** NYC {{v:nyc_subway:2019:opex_per_trip:usd2}}, London {{v:london_underground:2019:opex_per_trip:usd2}}, Madrid {{v:madrid_metro:2019:opex_per_trip:usd2}}, Tokyo Metro {{v:tokyo_metro:2019:opex_per_trip:usd2}}, Toei {{v:tokyo_toei:2019:opex_per_trip:usd2}}, Hong Kong {{v:hong_kong_mtr:2019:opex_per_trip:usd2}}, Seoul {{v:seoul_metro:2019:opex_per_trip:usd2}}. NYC trips are short, which helps it on this measure.
3. **Cost per car-km (2019):** NYC {{v:nyc_subway:2019:opex_per_car_km:usd2}}, higher than every foreign peer with data: Madrid {{v:madrid_metro:2019:opex_per_car_km:usd2}}, Tokyo Metro {{v:tokyo_metro:2019:opex_per_car_km:usd2}}, Seoul {{v:seoul_metro:2019:opex_per_car_km:usd2}}, Toei {{v:tokyo_toei:2019:opex_per_car_km:usd2}}, London {{v:london_underground:2019:opex_per_car_km:usd2}}, Hong Kong {{v:hong_kong_mtr:2019:opex_per_car_km:usd2}}. Per train-km (2023), NYC is {{c:nyc_over_tokyo_metro_trainkm_2023}} Tokyo Metro and {{c:nyc_over_london_underground_trainkm_2023}} London.
4. **The key tension.** NYC is cheap per rider among US systems because its cars are fuller ({{v:nyc_subway:2019:avg_car_load:n0}} people on board per car on average in 2019, against 15 to 25 for US peers other than PATH). But Tokyo and Hong Kong cars carried two to two and a half times as many people. Against Tokyo Metro, about {{c:load_share_tokyo_metro_2019}} of NYC's higher cost per passenger-km is explained by fuller cars and the rest by higher cost per car-km.
5. **Staffing.** NYC had {{v:nyc_subway:2023:employees_per_million_car_km:n0}} operating staff per million car-km in 2023, against {{v:tokyo_metro:2023:employees_per_million_car_km:n0}} at Tokyo Metro, {{v:tokyo_toei:2023:employees_per_million_car_km:n0}} at Toei, {{v:london_underground:2023:employees_per_million_car_km:n0}} in London and {{v:hong_kong_mtr:2023:employees_per_million_car_km:n0}} in Hong Kong. Among US systems, NYC's extra staff are in **facility maintenance** (track, structures, stations, signals, power): {{c:nyc_share_employees_facility_maintenance_2024}} of its operating staff in 2024, and {{c:nyc_subway_fm_per_dir_km_2024}} facility-maintenance workers per directional route-km against {{c:bart_fm_per_dir_km_2024}} to {{c:path_fm_per_dir_km_2024}} for US peers.
6. **Farebox recovery.** NYC fares covered {{v:nyc_subway:2019:farebox_recovery:pct}} of operating cost in 2019 and {{v:nyc_subway:2024:farebox_recovery:pct}} in 2024. Tokyo Metro covered {{v:tokyo_metro:2019:farebox_recovery:pct}} and London {{v:london_underground:2019:farebox_recovery:pct}} in 2019. NYC's fare revenue per trip ({{c:fare_per_trip_nyc_subway_2019}}) was about the same as Tokyo's ({{c:fare_per_trip_tokyo_metro_2019}} to {{c:fare_per_trip_tokyo_toei_2019}}). The difference in cost recovery is a cost-per-trip difference, not a fare difference.
7. **Reliability.** NYC trains run about 198,000 car-km between delay-causing failures (2025). Hong Kong and Singapore run 4.8 to 8.1 million. Definitions differ, but a gap of {{c:mdbf_ratio_hk_low_2025}} to {{c:mdbf_ratio_hk_high_2025}} times is too large to be a definition artifact. On the share of scheduled service actually run, NYC (94%) is close to London and Berlin and well behind Hong Kong and Singapore.
8. **Trend.** In real terms NYC's cost per car-km has been roughly flat for a decade ({{c:nyc_real_carkm_change_2015_2024}} from 2015 to 2024). Without general administration the change was {{c:nyc_real_exga_carkm_change_2015_2024}}. General administration more than doubled after 2022: the 2024 step is mostly injury-claim reserves; the 2023 step is still unexplained.
9. **What explains the gap.** The evidence is strongest for (a) maintenance-heavy staffing, which fits the 24/7 service pattern, old fixed-block signals and a large, old network, and (b) high overhead and claims costs. Two-person crews matter but explain at most about a quarter of the gap. System age and funding mix are weak explanations on their own. None of these links is proven causal: the sample is small and the systems differ in many ways at once.

---

## 1. Question and approach

The question is how much more the NYC subway costs to run than comparable metros, and why. This report compares NYC with eleven foreign metros and six US heavy-rail systems. It uses **operating cost**: the day-to-day cost of running trains, maintaining them and the infrastructure, and administration. Depreciation, debt service and capital projects are excluded for every system.

Three kinds of measure answer different questions, and the report keeps them apart:

- **Cost per passenger-km and per trip** measure cost per unit of what riders consume. They depend on production cost *and* on how many people use the service.
- **Cost per car-km and per train-km** measure cost per unit of service produced. They are closer to a measure of production efficiency. A car-km is one rail car moving one kilometre; a train-km is one whole train moving one kilometre.
- **Staff per million car-km and passenger-km per employee** measure labor productivity.

An economist would say the first group mixes the supply side (unit cost) with the demand side (load factor). A system can be cheap per rider because it is efficient, or because it is crowded. Both matter to a rider, and the report shows both.

**Main year.** 2019, the last year before the pandemic. Ridership fell sharply in 2020 to 2022, which distorts every per-rider figure. Later years are shown where they add something.

**Currency.** The main comparison uses PPP, which converts local currency by what it buys at home. For countries with low price levels (Spain, Korea, and Japan in recent years), PPP makes local costs look *higher* in dollars than market exchange rates would. PPP is the right choice for asking "how many real resources does this system use", but it is a choice; at market exchange rates most foreign systems would look cheaper than shown here.

### Data coverage

| System | Cost | Quality of cost figure | Years used |
| --- | --- | --- | --- |
| **New York** (MTA NYC Transit) | NTD heavy-rail mode | Reported, uniform US definitions | 2012–2025 |
| US peers (PATH, Washington, Boston, Philadelphia, Chicago, BART) | NTD heavy-rail mode | Reported | 2015–2025 |
| London Underground | TfL quarterly reports | Reported; **car-km estimated** from train-km | 2017–2024 |
| Tokyo Metro, Toei | Japanese government railway statistics | Reported; **passenger-km estimated after 2018** | 2015–2023 |
| Hong Kong MTR | MTR annual reports | **Estimated** heavy-rail share of rail cost | 2016–2025 |
| Seoul Metro (lines 1–8) | Settlement report 2018–19; aggregator site 2022–24 | **Estimated**; 2022–24 rests on a secondary site that names no source | 2018, 2019, 2024 |
| Madrid | Regional press releases | **Estimated** | 2018, 2019, 2024 |
| Singapore (SMRT lines only) | Revenue minus operating profit | **Estimated**; no staff data | 2021–2023 |
| Beijing | One news report | Secondary, definitions unknown | 2019 |
| Berlin | One parliamentary answer | Reported cost per trip only | 2017 |
| Paris | None | No metro-only cost exists in published sources | – |
| Istanbul | Company-wide audit | No ridership or service data, so no unit costs | – |
| Shanghai | None | Not found | – |

Sources: per-system notes in [`docs/peers/`](../docs/peers/) and [`docs/ntd_baseline.md`](../docs/ntd_baseline.md); fact-check results in [`docs/verification.md`](../docs/verification.md).

---

## 2. Per rider: NYC is cheap among US systems, equal to London, far behind Asia

{{fig:cost_per_passenger_km_2019.png:Bar chart of operating cost per passenger-km in 2019}}

{{fig:cost_per_trip_2019.png:Bar chart of operating cost per trip in 2019}}

{{t:unit_2019}}

¹ Hong Kong farebox recovery covers MTR's whole Hong Kong transport business (heavy rail, light rail, buses, Airport Express, high-speed rail), not heavy rail alone.

Three things stand out.

**NYC and London cost almost the same per passenger-km** ({{v:nyc_subway:2019:opex_per_passenger_km:usd2}} and {{v:london_underground:2019:opex_per_passenger_km:usd2}}). London is *more* expensive per trip ({{v:london_underground:2019:opex_per_trip:usd2}} against {{v:nyc_subway:2019:opex_per_trip:usd2}}), for two reasons. London trips are longer ({{v:london_underground:2019:avg_trip_length_km:n1}} km against {{v:nyc_subway:2019:avg_trip_length_km:n1}} km). And the two count trips differently: TfL counts one trip per entry through the gates, while the US National Transit Database (NTD) counts every boarding, so a NYC rider who changes trains counts twice. Cost per passenger-km avoids this problem and is the better measure.

**NYC costs three to four times as much per passenger-km as Tokyo, Hong Kong and Singapore.** In 2019 NYC was {{c:nyc_over_tokyo_metro_pkm_2019}} Tokyo Metro, {{c:nyc_over_tokyo_toei_pkm_2019}} Toei and {{c:nyc_over_hong_kong_mtr_pkm_2019}} Hong Kong. In 2023 NYC was {{c:nyc_over_singapore_mrt_pkm_2023}} Singapore's SMRT lines. Per trip, Tokyo, Hong Kong and Seoul cost about $1.00 to $1.20, against NYC's {{v:nyc_subway:2019:opex_per_trip:usd2}}.

**Among US systems, NYC is cheap per rider.** Only Chicago and BART were cheaper per passenger-km in 2019, and only Boston was as cheap per trip. This is the basis for the common claim that "the NYC subway is efficient". It is true within the US and only per rider.

Two further data points sit outside the chart because their definitions are uncertain. Beijing's operators reported about {{v:beijing_subway:2019:opex_per_trip:usd2}} per trip in 2019, close to NYC, but this comes from a news report that does not define cost or trips. Berlin's U-Bahn cost {{v:berlin_ubahn:2017:opex_per_trip:usd2}} per trip in 2017 including attributable infrastructure, against NYC's {{v:nyc_subway:2017:opex_per_trip:usd2}} that year.

*Sources for this section:* rows `<system>_2019_opex_per_passenger_km*`, `*_opex_per_trip*`, `*_avg_trip_length_km*`, `*_farebox_recovery*` in [`data/observations.csv`](../data/observations.csv). NYC and US peers: NTD TS2.1 (`ntd_ts21_by_mode`), restated with `fred_gdp_deflator`. London: `tfl_qpr_q4_2019_20`, `tfl_til_2024_demand_performance`. Tokyo: `mlit_yardstick_fy2018`, `mlit_yardstick_fy2019`. Hong Kong: `mtr_ar2025_ten_year_stats`. Seoul: `seoul_metro_settlement_2019`. Madrid: CRTM reports and Comunidad de Madrid press releases. Beijing: `jiemian_2023_beijing_cost_per_trip` (secondary). Berlin: `abghs_s18_15985`. PPP: method [`ppp_usd_2024`](../methods/ppp_usd_2024.md). Ratios: [`report/numbers.csv`](numbers.csv), ids `nyc_over_*`.

---

## 3. Per unit of service: NYC is the most expensive large metro

{{fig:cost_per_car_km_2019.png:Bar chart of operating cost per car-km in 2019}}

{{fig:cost_per_train_km_2023.png:Bar chart of operating cost per train-km in 2023}}

Per car-km, NYC ({{v:nyc_subway:2019:opex_per_car_km:usd2}} in 2019) costs more than every foreign system with data. The gaps are moderate, not several-fold:

- {{c:nyc_over_tokyo_metro_carkm_2019}} Tokyo Metro and {{c:nyc_over_tokyo_toei_carkm_2019}} Toei (both reported, not estimated);
- {{c:nyc_over_london_underground_carkm_2019}} London and {{c:nyc_over_hong_kong_mtr_carkm_2019}} Hong Kong;
- {{c:nyc_over_seoul_metro_carkm_2019}} Seoul and {{c:nyc_over_madrid_metro_carkm_2019}} Madrid.

The gap widened after the pandemic. In 2023 NYC was {{c:nyc_over_tokyo_metro_carkm_2023}} Tokyo Metro, {{c:nyc_over_tokyo_toei_carkm_2023}} Toei, {{c:nyc_over_london_underground_carkm_2023}} London, {{c:nyc_over_hong_kong_mtr_carkm_2023}} Hong Kong and {{c:nyc_over_singapore_mrt_carkm_2023}} Singapore per car-km. In 2024 NYC was {{c:nyc_over_seoul_metro_carkm_2024}} Seoul, but Seoul's 2024 cost is a weak estimate (see section 11).

**Per train-km the gap is larger,** because NYC runs long trains: about {{v:nyc_subway:2023:avg_cars_per_train:n1}} cars on average in 2023, against about {{v:tokyo_metro:2023:avg_cars_per_train:n1}} at Tokyo Metro and an estimated {{v:london_underground:2023:avg_cars_per_train:n1}} in London. NYC spent {{v:nyc_subway:2023:opex_per_train_km:usd0}} per train-km in 2023, against {{v:tokyo_metro:2023:opex_per_train_km:usd0}} at Tokyo Metro, {{v:tokyo_toei:2023:opex_per_train_km:usd0}} at Toei and {{v:london_underground:2023:opex_per_train_km:usd0}} in London. Some costs scale with trains (crews, signals, dispatching), some with cars (maintenance of each car, energy), and some with neither (stations, track). The truth lies between the car-km and train-km comparisons.

**Car size cuts the other way for London.** London's deep-tube cars are small, so a London car-km delivers less capacity than a NYC car-km. That makes the per-car-km gap with London look larger than a per-seat comparison would. The dataset has no seat-km or place-km figures, so this cannot be corrected yet.

Among US systems, NYC is in the upper middle per car-km. PATH, in the same city and labor market, costs more than twice as much ({{v:path:2019:opex_per_car_km:usd2}}).

*Sources:* rows `*_opex_per_car_km*`, `*_opex_per_train_km*`, `*_avg_cars_per_train*` (NYC and US train-km: NTD breakdowns table, `ntd_breakdowns`, 2022 onward; London car-km: method [`london_car_km`](../methods/london_car_km.md); Hong Kong cost: [`hk_metro_cost_from_car_km`](../methods/hk_metro_cost_from_car_km.md); Seoul: [`seoul_opex_excl_depreciation`](../methods/seoul_opex_excl_depreciation.md), [`seoul_car_km_from_train_km`](../methods/seoul_car_km_from_train_km.md); Madrid: [`madrid_opex_from_press`](../methods/madrid_opex_from_press.md); Singapore: [`smrt_opex_from_revenue_ebit`](../methods/smrt_opex_from_revenue_ebit.md)). Ratios: `report/numbers.csv`.

---

## 4. The key tension: expensive service, fuller cars than the US, emptier cars than Asia

Cost per passenger-km is cost per car-km divided by the average number of people on board each car:

> cost per passenger-km = cost per car-km ÷ passengers per car

So a system can have a low cost per rider either by producing service cheaply or by filling it. The chart below plots both.

{{fig:cost_vs_load_2019.png:Scatter of cost per car-km against passengers per car, 2019}}

- **Against US peers,** NYC produces service at a similar or higher cost but fills its cars better. That is why it looks efficient in US rankings.
- **Against London,** NYC costs about half as much again per car-km but carries about 40% more people per car. The two effects cancel, so cost per passenger-km is the same.
- **Against Tokyo and Hong Kong,** NYC is both more expensive per car-km and much emptier. Fuller cars are the bigger part of the gap.

The table splits the 2019 gap in cost per passenger-km into its two parts. The split uses logarithms, so the two parts add up: the last column is the share of the gap that comes from passengers per car.

{{t:decomp_2019}}

**Is low occupancy a form of inefficiency?** Partly, but mostly not in the sense that matters for management. How full cars are depends on demand (density, the share of trips made by transit, trip patterns) and on how much service the agency chooses to run. NYC runs all night (section 11.2), and service at quiet times carries fewer people per car. That raises cost per rider, but it is a service riders value. So the cleanest measure of whether NYC *produces* service efficiently is cost per car-km and per train-km, where NYC was 10% to 70% more expensive than its foreign peers in 2019 and 35% to 75% more in 2023. The 3× to 4× gap per rider against Asia is mostly a difference in how crowded the systems are, not in how well they are run.

*Sources:* rows `*_2019_avg_car_load*`, `*_2019_opex_per_car_km*`, `*_2019_opex_per_passenger_km*`; decomposition `load_share_*_2019` in `report/numbers.csv`. Tokyo's 2019 passengers per car rests on estimated passenger-km ([`tokyo_passenger_km_from_trip_length`](../methods/tokyo_passenger_km_from_trip_length.md)); the 2018 values, which are fully reported, give the same picture (section 6).

---

## 5. Labor productivity

{{fig:staff_per_car_km_2023.png:Bar chart of staff per million car-km, 2023}}

{{fig:passenger_km_per_staff_2023.png:Bar chart of passenger-km per employee, 2023}}

{{t:staff_2023}}

NYC used {{c:nyc_over_tokyo_metro_staff_2023}} as many staff per car-km as Tokyo Metro in 2023, {{c:nyc_over_tokyo_toei_staff_2023}} as many as Toei, {{c:nyc_over_london_underground_staff_2023}} as many as London and {{c:nyc_over_hong_kong_mtr_staff_2023}} as many as Hong Kong. Seoul (about {{v:seoul_metro:2019:employees_per_million_car_km:n0}} in 2019, counting every employee of the corporation) is the one foreign peer that staffs like NYC. Seoul is also the one foreign peer that still has two-person crews on some lines.

Per passenger-km, each NYC employee carried about a quarter of what an employee in Tokyo or Hong Kong carried. That is the staff-side version of section 4: fewer staff per unit of service *and* fuller cars.

The staff gap per car-km (about 30% to 70%) is similar in size to the cost gap per car-km. This is consistent with the working hypothesis in the scoping notes: **NYC's cost problem is mainly about how many people it takes to run the system, not about how much each is paid.** But the dataset has no wage figures for foreign peers, so this is a consistency check, not a test. One US figure points the same way: NYC's fringe benefits were 40.6% of labor cost in 2024, high but below PATH's 48.8% (NTD; `nyc_subway_pension_benefit_share_ntd`, `path_pension_benefit_share_ntd` in `data/factors.csv`).

*Caveats.* Head counts and full-time equivalents are mixed: NYC and US peers are NTD head counts in operating functions (capital staff excluded); London is FTE at year end including agency staff; Tokyo and Toei are year-end head counts excluding contractors; Hong Kong's split of staff between heavy rail and other businesses is an estimate ([`hk_metro_staff_share`](../methods/hk_metro_staff_share.md)). Systems that contract out more work look more productive per employee than they are. Contracting models are not yet recorded in the dataset.

*Sources:* rows `*_employees_per_million_car_km*`, `*_passenger_km_per_employee*`, `*_trips_per_employee*`. NYC and US: `ntd_employees_by_mode`. London: TfL quarterly reports (headcount tables). Tokyo: `tokyometro_yuho_*`, `tokyo_audit_toei_subway_*`. Hong Kong: `mtr_ar2025_ten_year_stats`. Seoul: `seoul_metro_settlement_2019`. Madrid: `cam_press_*`.

---

## 6. The main results with every estimate left out

Several peer figures are estimates. The table below keeps only reported values and values computed from reported values by plain arithmetic. It uses 2018 for Tokyo passenger-km, the last year Japan published it.

{{t:unit_noest}}

What survives without estimates:

- **Per passenger-km:** NYC ({{v:nyc_subway:2018:opex_per_passenger_km:usd2}} in 2018) is about the same as London ({{v:london_underground:2018:opex_per_passenger_km:usd2}}) and about three times Tokyo Metro ({{v:tokyo_metro:2018:opex_per_passenger_km:usd2}}) and Toei ({{v:tokyo_toei:2018:opex_per_passenger_km:usd2}}).
- **Per trip:** NYC is cheaper than London and more than twice Tokyo.
- **Per car-km:** NYC is {{c:nyc_over_tokyo_metro_carkm_2019}} Tokyo Metro and {{c:nyc_over_tokyo_toei_carkm_2019}} Toei (2019).
- **Per train-km:** NYC is {{c:nyc_over_tokyo_metro_trainkm_2023}} Tokyo Metro, {{c:nyc_over_tokyo_toei_trainkm_2023}} Toei and {{c:nyc_over_london_underground_trainkm_2023}} London (2023).

**Every headline finding holds without the estimated cities.** Hong Kong, Seoul, Singapore and Madrid add breadth but do not change the direction of any conclusion.

---

## 7. Where NYC's money and staff go

The NTD splits NYC's cost and staff into four functions. In 2024:

| Function | Share of operating cost | Share of operating staff |
| --- | ---: | ---: |
| Vehicle operations (train crews, dispatch, and related) | {{c:nyc_share_opex_vehicle_operations_2024}} | {{c:nyc_share_employees_vehicle_operations_2024}} |
| Vehicle maintenance | {{c:nyc_share_opex_vehicle_maintenance_2024}} | {{c:nyc_share_employees_vehicle_maintenance_2024}} |
| Facility maintenance (track, structures, stations, signals, power) | {{c:nyc_share_opex_facility_maintenance_2024}} | {{c:nyc_share_employees_facility_maintenance_2024}} |
| General administration | {{c:nyc_share_opex_general_administration_2024}} | {{c:nyc_share_employees_general_administration_2024}} |

No foreign peer publishes a comparable split, so the comparison is with US systems, which report under the same NTD rules.

{{fig:us_staff_by_function_2024.png:Stacked bar chart of US heavy-rail staff by function per million train-km, 2024}}

{{t:us_functions_2024}}

**Facility maintenance is where NYC stands out.** Per million train-km, NYC's vehicle-operations staff ({{c:nyc_subway_employees_vehicle_operations_per_m_train_km_2024}}) are *within* the US range ({{c:bart_employees_vehicle_operations_per_m_train_km_2024}} at BART to {{c:chicago_l_employees_vehicle_operations_per_m_train_km_2024}} at Chicago, excluding PATH). Its facility-maintenance staff ({{c:nyc_subway_employees_facility_maintenance_per_m_train_km_2024}}) are about one and a half times PATH's ({{c:path_employees_facility_maintenance_per_m_train_km_2024}}) and two to five times those of the other US systems ({{c:bart_employees_facility_maintenance_per_m_train_km_2024}} to {{c:wmata_metrorail_employees_facility_maintenance_per_m_train_km_2024}}). Per directional route-km, NYC has {{c:nyc_subway_fm_per_dir_km_2024}} facility-maintenance workers, against {{c:wmata_metrorail_fm_per_dir_km_2024}} in Washington and {{c:path_fm_per_dir_km_2024}} at PATH.

Part of this is intensity of use: each kilometre of NYC track carries far more trains than in other US systems ({{c:nyc_subway_train_km_per_dir_km_2024}} train-km per directional route-km a year, against {{c:wmata_metrorail_train_km_per_dir_km_2024}} in Washington and {{c:chicago_l_train_km_per_dir_km_2024}} in Chicago). NYC also has many stations for its length. But even per train-km, which adjusts for intensity, NYC's facility-maintenance staffing is the highest in the US set.

*Sources:* rows `nyc_subway_2024_opex_<function>_ntd`, `<system>_2024_employees_<function>_ntd`, `<system>_2024_train_km_ntd`, `<system>_2024_directional_route_km_ntd` (NTD TS2.1, employees and breakdowns tables). Ratios: `report/numbers.csv`, ids `*_per_m_train_km_2024`, `*_fm_per_dir_km_2024`, `nyc_share_*`.

---

## 8. NYC over time

{{fig:nyc_cost_per_car_km_trend.png:Line chart of NYC cost per car-km in 2024 dollars, 2012 to 2025}}

{{t:nyc_trend}}

- **Flat in real terms.** Real cost per car-km was {{v:nyc_subway:2015:opex_per_car_km:usd2}} in 2015 and {{v:nyc_subway:2024:opex_per_car_km:usd2}} in 2024. The change from 2019 to 2024 was {{c:nyc_real_carkm_change_2019_2024}}.
- **Excluding general administration it fell:** the change was {{c:nyc_real_exga_carkm_change_2015_2024}} from 2015 to 2024 and {{c:nyc_real_exga_carkm_change_2019_2024}} from 2019 to 2024. The core cost of running and maintaining the system has not been running away.
- **General administration more than doubled** from {{v:nyc_subway:2022:opex_general_administration:usdm}} (nominal) in 2022 to {{v:nyc_subway:2024:opex_general_administration:usdm}} in 2024, from {{c:nyc_ga_share_2019}} of cost in 2019 to {{c:nyc_share_opex_general_administration_2024}} in 2024. The 2024 step is mostly casualty and liability cost, which rose from {{v:nyc_subway:2023:opex_type_casualty_and_liability:usdm}} to {{v:nyc_subway:2024:opex_type_casualty_and_liability:usdm}}. MTA's audited statements attribute this to higher claims reserves for selected injury cases. The 2023 step is different: it is labor booked to administration, and the number of subway staff reported under administration nearly doubled in one year (1,127 to 2,192 full-time). **Whether that was real hiring or a reclassification of existing staff is not known.** See [`docs/nyc_admin_cost_jump.md`](../docs/nyc_admin_cost_jump.md).
- **Per rider, the pandemic still shows.** Cost per passenger-km rose from {{v:nyc_subway:2019:opex_per_passenger_km:usd2}} (2019) to {{v:nyc_subway:2024:opex_per_passenger_km:usd2}} (2024) because ridership has not recovered while service has.
- **Series breaks.** The 2012 value is low against 2013 with almost the same service, and cost fell from 2016 to 2017 without an obvious cause. Treat single-year moves in 2012 to 2017 with care.
- **2000 to 2011 are missing.** The NTD archive workbook for those years could not be read from the research environment. A long-run trend for NYC is therefore not yet possible.

*Sources:* rows `nyc_subway_<year>_*_real2024_ntd` (method [`ntd_gdp_deflator_real_2024`](../methods/ntd_gdp_deflator_real_2024.md)), `nyc_subway_<year>_opex_general_administration_ntd`, `nyc_subway_<year>_opex_type_casualty_and_liability_ntd` (`ntd_opex_by_type`), `nyc_subway_<year>_employee_count_general_administration_ft_ntd` (`ntd_employees_by_mode`); MTA statements `nycta_fs_2025`.

---

## 9. Funding: who pays

{{fig:farebox_recovery_2019.png:Bar chart of farebox recovery in 2019}}

Tokyo Metro and Toei recovered {{v:tokyo_metro:2019:farebox_recovery:pct}} and {{v:tokyo_toei:2019:farebox_recovery:pct}} of operating cost from fares in 2019; London {{v:london_underground:2019:farebox_recovery:pct}}; MTR's whole Hong Kong transport business {{v:hong_kong_mtr:2019:farebox_recovery:pct}}. NYC recovered {{v:nyc_subway:2019:farebox_recovery:pct}}, near the top of the US range, and Seoul an estimated {{v:seoul_metro:2019:farebox_recovery:pct}}. After the pandemic NYC fell to {{v:nyc_subway:2024:farebox_recovery:pct}} (2024) and London to {{v:london_underground:2024:farebox_recovery:pct}}.

A useful identity: fare revenue per trip = farebox recovery × cost per trip. In 2019 that gives NYC {{c:fare_per_trip_nyc_subway_2019}}, Tokyo Metro {{c:fare_per_trip_tokyo_metro_2019}}, Toei {{c:fare_per_trip_tokyo_toei_2019}} and London {{c:fare_per_trip_london_underground_2019}} (2024 dollars at PPP). **NYC riders paid about what Tokyo riders paid per trip.** Tokyo covers its costs because each trip costs less to provide, not because its fares are higher. London covers its costs mainly through high fares.

Seoul shows the other side: about 15% of its riders travelled free in 2018, mostly seniors, and Seoul Metro says it is not compensated for this (secondary sources `newdaily_2019_seoul_metro`, `mt_2026_seoul_metro_loss`).

*Sources:* rows `*_2019_farebox_recovery*`, `*_2019_opex_per_trip*`; `fare_per_trip_*` in `report/numbers.csv`.

---

## 10. Reliability

Reliability measures are the least comparable part of the dataset, because each agency defines failures, delays and on-time running its own way. The most comparable measure is **mean distance between failures**: car-km run per failure that delays service.

{{fig:mdbf_2025.png:Bar chart of car-km between failures, log scale}}

{{t:reliability}}

- **Train failures.** NYC's pooled mean distance between failures was about 198,000 car-km in 2025 (MTA data; the LTA compilation gives the same). Hong Kong's two line groups ran 4.8 and 8.1 million, and Singapore 7.7 million. Hong Kong and Singapore count only failures that delay service by 5 minutes or more, so they count fewer failures than NYC does. But a gap of {{c:mdbf_ratio_hk_low_2025}} to {{c:mdbf_ratio_hk_high_2025}} times is far too large to come from the definition alone.
- **Getting worse.** NYC's figure fell from about 243,000 car-km in 2021 to 198,000 in 2025 (`nyc_subway_<year>_mdbf_car_km` in `data/reliability.csv`).
- **Within the US**, using NTD's uniform "major mechanical failure" count, NYC ran {{v:nyc_subway:2024:mdbf:k}} car-km per major failure in 2024: better than Boston ({{v:mbta_subway:2024:mdbf:k}}) and Chicago ({{v:chicago_l:2024:mdbf:k}}), worse than BART ({{v:bart:2024:mdbf:k}}).
- **Service actually run.** NYC ran 94.2% of scheduled service (December 2024 to November 2025, as compiled by Singapore's Land Transport Authority). London ran 91.0% of scheduled train-km in 2024/25, down from 96.6–97.6% before 2019; TfL blames staff availability, rolling stock and asset condition. Berlin ran 94.3% (2025). Hong Kong and Singapore ran 99.8–99.9%.
- **Long delays.** Tokyo Metro had 0.26 and Toei 0.06 delays of 30 minutes or more per million train-km in 2024; Singapore 0.18 (LTA compilation). No NYC figure on the same basis was found.
- **On-time performance** is not comparable across systems. NYC's own terminal on-time rate jumped from 66% (2018) to 81% (2019), which is probably a change in MTA's standard, not a real improvement.

**Reliability and cost.** The systems that cost least per car-km (Hong Kong, Singapore) are also the most reliable, and the most expensive (NYC) is among the least reliable. This is a correlation across a handful of systems. It is consistent with the view that old assets and fixed-block signals raise both maintenance cost and failure rates, but it does not prove it.

*Sources:* `data/reliability.csv`: `nyc_subway_<year>_mdbf_car_km` (MTA via data.ny.gov), `hong_kong_mtr_2025_mdbf_car_km_*` (`mtr_annual_report_2025_ops`), `singapore_mrt_*` (LTA), `london_underground_<year>_service_delivered_km` (`tfl_travel_in_london_2024`, `tfl_travel_in_london_2025`), `*_delays_30min_per_million_train_km` and `*_service_delivered_lta` (LTA compilation, secondary), `nyc_subway_<year>_terminal_otp`. NTD rows `*_2024_mdbf_ntd` (method [`ntd_mdbf_major`](../methods/ntd_mdbf_major.md)).

---

## 11. What explains NYC's higher cost? The factors one by one

{{t:factors}}

The dataset supports a structured comparison, not a regression: there are about a dozen systems and they differ in many ways at once. For each factor below the report gives the evidence for, the evidence against, and a verdict on how much weight it can bear.

### 11.1 Two-person crews and work rules

**For.** NYC is, in the words of the Transit Costs Project's 2025 survey of over 400 lines in 36 cities, "almost globally unique" in keeping two-person crews (train operator plus conductor) on most lines; fewer than 6.25% of lines surveyed use them (`tcp_2025_train_operations`). Every foreign peer in this report runs one-person or driverless trains on all or almost all lines, except Seoul's lines 1–4. The crews come from the labor contract with TWU Local 100, not from state law; a bill to put them into law was vetoed in December 2025 (`streetsblog_2025_12_19_opto_veto`). The Citizens Budget Commission, as quoted by Reason, puts the saving from one-person crews at {{c:cbc_crew_saving}} a year (secondary, `reason_2026_two_person_crews`; the CBC report itself is not yet checked). That is {{c:cbc_share_of_opex_2024}} of NYC's 2024 subway operating cost.

**Against, or limits.** Set against the size of the gap, the saving is modest. Had NYC run at Tokyo Metro's 2023 cost per car-km, it would have spent about {{c:gap_dollars_vs_tokyo_metro_2023}} less that year; the crew saving is {{c:cbc_share_of_gap_tokyo_metro_2023}} of that. Against London the share is {{c:cbc_share_of_gap_london_underground_2023}}. Within the US, NYC's vehicle-operations staff per train-km are not out of line (section 7). This is partly because NYC's long trains spread a crew over more cars. (The crew model of the US peers is not yet recorded in the dataset, so this comparison cannot isolate the crew rule.) Seoul, which still has two-person crews on four lines, staffs at NYC's level per car-km but costs less per car-km.

**Verdict.** A real and identifiable cost, worth roughly 7% of NYC's operating budget and perhaps a quarter of the gap with the best peers. It is not the main story. Wider work rules (overtime, track-access rules, job demarcation) could matter more, but the dataset has no direct measure of them.

### 11.2 24/7 service

**For.** NYC runs every line 24 hours a day, every day. Paris closes for about 4.5 hours a night, Madrid about 4 hours and Berlin about 3.5 hours on weeknights; London runs all night only on some lines on weekend nights (`data/factors.csv`, `overnight_service`, `nightly_closure_hours`; several of these rows are from secondary sources). Without a nightly closure, track and signal work must be done around running trains, with flagging, slow orders and diversions, or by taking lines out of service. Alon Levy argues that this is a main reason NYC maintenance is so expensive (`levy_2019_overnight_transit`, a secondary argument). The NTD data fits: NYC's facility-maintenance staff per train-km are the highest in the US set, about one and a half times PATH's and two to five times the others' (section 7). Night service also carries few riders, which lowers passengers per car and raises cost per rider (section 4). The dataset has no NYC ridership by hour to size this.

**Against.** PATH is noted in `data/systems.csv` as also running 24/7 (not yet a sourced factor row), and it is far more expensive per car-km than NYC, so 24/7 service alone does not tell the two apart. Copenhagen runs 24/7, but it is driverless and new, and the dataset has no cost for it. NYC's maintenance staffing may also reflect the size and age of its stations and structures (section 11.4), not only its hours. The dataset has no measure of how much track work is done under traffic.

**Verdict.** Plausible and consistent with the strongest pattern in the data (maintenance-heavy staffing). Not separately testable with this dataset. The best test would be cost by function for a 24/7 system against a peer that closes at night, which needs data not yet available outside the US.

### 11.3 Signaling and automation

**For.** About 85% of NYC's network still uses fixed-block signals, with communications-based train control (CBTC) only on the L, the 7 and parts of Queens Boulevard, and three further projects delayed to 2027–2028 (`nyc_subway_cbtc_share_lines_mta`; the 85% is from a secondary source). Most peers run automatic train operation on most lines, and Paris, Singapore, Hong Kong and others have driverless lines. Old signals need more maintenance staff, cause failures and delays, and block one-person or driverless operation.

**Against.** Tokyo Metro is also mostly fixed-block (with automatic train control; its first CBTC line opened in December 2024, `tokyo_metro_safety_report_2025`) and is cheaper per car-km and much more reliable. Signaling type alone does not make a system expensive; condition and maintenance practice matter too.

**Verdict.** Important for reliability and as an enabler of crew and maintenance savings. Its direct effect on operating cost cannot be separated in this data.

### 11.4 System age

**For.** NYC opened in 1904. The cheapest systems per car-km (Hong Kong, 1979; Singapore, 1987) are the youngest.

**Against.** London (1890) is older than NYC and cheaper per car-km. Tokyo Metro (1927), Madrid (1919), Paris (1900) and Berlin (1902) are all old. In the US, Chicago (1892) is among the cheapest systems per car-km and BART (1972) and Washington (1976) are not cheaper than it. Opening year says little about the condition of assets today.

**Verdict.** Weak on its own. Age probably matters through specific channels (signals, station structures, state of repair) rather than directly.

### 11.5 Staffing levels

**For.** This is the factor with the most direct evidence. NYC uses 30% to 70% more staff per car-km than Tokyo, London and Hong Kong (section 5), and the extra staff are concentrated in facility maintenance (section 7). The staff gap is about the size of the cost gap.

**Against.** Staff counts are not fully comparable (head counts against FTE; contracting differs). Without wage data for the peers, a part of the cost gap could still be wages and benefits.

**Verdict.** The most likely proximate explanation of the production-cost gap. It is a description, though, not a cause: the question is *why* NYC needs more maintenance staff, which points back to 11.2–11.4 and to work rules.

### 11.6 Administration and injury claims

**For.** General administration rose from {{c:nyc_ga_share_2019}} of NYC subway cost in 2019 to {{c:nyc_share_opex_general_administration_2024}} in 2024. Casualty and liability cost alone was {{c:nyc_share_opex_type_casualty_and_liability_2024}} of 2024 cost, or {{c:nyc_casualty_per_car_km_2024}} per car-km. US tort law and New York's liability rules may make this cost structurally higher than abroad; that is a hypothesis, not tested here.

**Against.** Excluding administration, NYC's real cost per car-km ({{v:nyc_subway:2024:opex_excl_ga_per_car_km:usd2}} in 2024) is lower than in 2019 and closer to Tokyo Metro's *full* cost. But the peers' figures include their own overhead, so removing NYC's overhead alone is not a fair comparison. Claims reserves are lumpy: the 2024 jump partly reversed in 2025. No foreign claims data was found.

**Verdict.** A real and growing part of the gap since 2022, and the part that has changed most recently. The 2023 rise in administration staff needs explaining before it can be called waste or reclassification.

### 11.7 Funding mix

**For.** The two systems run as companies expected to pay their way (Tokyo Metro, which receives no operating subsidy, and MTR in Hong Kong) are among the cheapest per car-km. A hard budget constraint plausibly disciplines cost.

**Against.** Toei, a city-owned bureau, is as cheap as Tokyo Metro. London is publicly owned and cheaper per car-km than NYC. Causation probably runs largely the other way: dense, crowded systems *can* cover costs from fares, and that is what lets them run as companies. Section 9 shows NYC's fare per trip is similar to Tokyo's; the farebox gap is a cost-per-trip gap.

**Verdict.** Weak as an explanation of cost. Farebox recovery is better read as an outcome of cost and crowding than as a cause.

### 11.8 Factors that are not inefficiency

Some differences in cost per rider are not management failures:

- **Crowding and density.** Tokyo and Hong Kong carry two to two and a half times as many people per car. This is a feature of the cities.
- **Trip length and trip counting.** NYC's short average trip and boarding-based counting make it look cheaper per trip; they do not affect cost per passenger-km.
- **Price levels.** PPP conversion matters a lot for Madrid and Seoul (section 1).
- **Policing.** London's cost includes British Transport Police; NYC subway policing is paid by the NYPD and is outside NTD cost. This flatters NYC.

---

## 12. What we can and cannot say about causation

What the data shows with reasonable confidence:

1. NYC's cost per unit of service is higher than every foreign peer with data, by roughly 10% to 70% per car-km in 2019 and 35% to 75% in 2023, and by more per train-km. This holds with estimates left out.
2. NYC's cost per rider is equal to London's and three to four times Tokyo's and Hong Kong's; most of the Asian gap is crowding.
3. NYC uses more staff per unit of service, and among US systems its extra staff are in facility maintenance.
4. NYC's trains fail far more often than Hong Kong's or Singapore's.

What it does not show:

- **Which factor causes the gap.** With about a dozen systems that differ at once in hours, crews, signals, age, density, wages and accounting, no statistical method can separate the factors. The verdicts in section 11 are judgments from patterns, not estimates of effects.
- **Wages.** No wage or benefit data for foreign systems is in the dataset, so "too many people" and "people paid too much" cannot be fully separated.
- **Long-run trend.** NYC data before 2012 is missing.

The most convincing future test would be within-system: what happened to cost and reliability on NYC lines that moved to CBTC (the L, the 7) or to one-person operation, against lines that did not.

---

## 13. Data gaps and caveats

- **Paris:** no metro-only cost exists. RATP reports metro, RER, tram and bus together, and France's national audit office has asked RATP to start tracking cost by line.
- **Shanghai and Beijing:** no primary operator cost data. Beijing has only one news-report figure.
- **Istanbul:** company-wide cost only, no ridership or service data.
- **Singapore:** SMRT lines only, cost estimated from revenue minus operating profit, three years, no staff. FY2014–2016 figures stay unverified.
- **Seoul:** 2018–2019 cost is an estimate (depreciation not in the readable source). **2022–2024 cost is weak**: it rests on an aggregator website that names no underlying document, plus an assumed depreciation of 340–480 billion won.
- **Madrid:** cost estimated from press releases; no passenger-km.
- **Hong Kong:** heavy-rail cost and staff are estimated shares of MTR's rail business.
- **London:** car-km estimated from train-km; no cost split by function.
- **Tokyo:** passenger-km after 2018 estimated from trip length.
- **NYC:** no data before 2012; possible series breaks in 2012 and 2016–2017; the 2023 doubling of administration staff is unexplained.
- **All systems:** wages, contracting models, crew models of US peers, car dimensions and seat-km are not yet in the dataset.

Verification status: an independent fact-check re-read about 3,900 values against their sources and found no wrong numbers; about 2% of hand-collected rows needed locator or wording fixes ([`docs/verification.md`](../docs/verification.md)). Estimated rows stay `unverified` by design, because their assumptions are not facts a source can confirm. Secondary-source rows (Wikipedia, blogs, news) also stay `unverified`.

## 14. What would most improve this report

1. NYC 2000–2011 from the NTD archive workbook (needs a normal internet connection).
2. Cost by function for at least one foreign peer (London's or Tokyo's maintenance split) to test the facility-maintenance finding outside the US.
3. Seoul Metro's own 2020–2025 financial statements, and Paris and Berlin mode-level costs if they ever exist.
4. Line-level NYC data before and after CBTC and one-person operation.
5. Wage and benefit levels for the peers, relative to local wages.

---

## Appendix A. 2023 comparison (latest year with most peers)

{{t:unit_2023}}

## Appendix B. US heavy-rail systems, 2019

{{t:unit_2019_us}}

## Appendix C. How to check any number

- Every value in a table or chart is a row in [`data/observations.csv`](../data/observations.csv), [`data/reliability.csv`](../data/reliability.csv) or [`data/factors.csv`](../data/factors.csv), each with a `source_id` in [`sources/sources.csv`](../sources/sources.csv) and a locator.
- Every number computed for this report (ratios, shares, gaps) is in [`report/numbers.csv`](numbers.csv) with its formula and input rows.
- `python3 scripts/build_report.py` rebuilds all charts, tables and this file from the data. The choice of which row to use is in [`scripts/report_data.py`](../scripts/report_data.py): 2024 dollars (US GDP deflator for US systems, PPP for others), metro-only scope where it exists. A value is marked EST if its row or any row it was computed from is an estimate.
