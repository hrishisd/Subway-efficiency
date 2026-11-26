# London Underground: sources and comparability

Rows: `data/peers/london_underground.csv` (built into `data/observations.csv` by `scripts/build_peers.py`). Years are TfL financial years (April to March), labelled by the calendar year in which they start: `2019` means 2019/20.

## What the data is

| Item | Source | Years | Notes |
| --- | --- | --- | --- |
| Operating cost | TfL Quarterly Performance Reports, Q4 of each year, table "Underground (£m)" | 2017-2024 | Direct operating cost plus allocated indirect operating cost. For 2018 and 2019 the total is also in the audited segment note, and it matches. |
| Fare revenue | Same table, "Passenger income" | 2017-2024 | Underground only. |
| Trips | Travel in London 2024, Table 1 ("journey stages"); 2024 from the Q4 2024/25 report | 2015-2024 | |
| Passenger-km | Travel in London 2024, Table 2 | 2015-2023 | |
| Train-km | Travel in London 2024, Table 9 ("operated kilometres") | 2015-2023 | |
| Car-km | **ESTIMATE**: train-km × 6.87 cars per train (range 6.5 to 7.3) | 2015-2023 | Method [`london_car_km`](../../methods/london_car_km.md). TfL does not publish car-km. |
| Staff | Quarterly reports, headcount table, FTE at 31 March | 2015-2018, 2022-2024 | 2019-2021 not yet read verbatim. |

## Comparability with the NYC (NTD) figures

- **Cost scope is close to NTD's.** Both exclude depreciation, capital renewals and interest, and both include allocated overhead. TfL's "indirect operating cost" plays the role of NTD general administration. Central TfL costs that TfL does not allocate to the Underground are left out.
- **Pensions differ.** TfL's management accounts charge pension cost at the cash contribution rate. The employer rate fell from 27.3% to 10.5% of pay in 2024/25 after the fund's valuation, which lowers 2024 cost. NTD reports pension expense under US accounting rules.
- **Policing.** British Transport Police costs are inside LU direct cost (the 2022/23 report mentions them). NYC transit policing is mostly paid by the NYPD and is outside NTD subway cost. This makes London look more expensive, not less.
- **Trips are counted differently.** TfL counts a journey stage per entry through the gates; a change between Underground lines inside the gates is not a new stage. NTD unlinked trips for NYC count boardings, and MTA estimates transfers. If NYC counts more boardings per journey, NYC cost per trip looks lower. Cost per passenger-km avoids this problem.
- **Cars are smaller.** Deep-tube cars are about 16 to 18 m long and much narrower than NYC cars. Cost per car-km favours London less than cost per seat-km would. Use cost per train-km and per passenger-km as well.
- **Staff are FTE at year end**, including agency staff, for the Underground business area. NTD figures for NYC are head counts in operating functions. The two are close but not identical.
- **Fiscal year.** April to March. Converted to US dollars with the PPP factor of the calendar year in which it starts.

## Not found

- Operating cost for 2015/16 and 2016/17 (only quarterly figures were reachable).
- Passenger-km and train-km for 2024/25 (Travel in London 2025 tables were not readable).
- Staff for 2019/20 to 2021/22 (only in automated summaries, not verbatim).
- A cost split by function (operations, maintenance, stations), as NTD gives for NYC.
