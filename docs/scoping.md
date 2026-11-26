# Scoping (phase 1)

Decided on 2026-11-26. This file is the repository copy of the phase 1 scoping work. Sources for the claims here are in [`../sources/sources.csv`](../sources/sources.csv).

## Question

How much more does the NYC subway cost to run, per unit of service, than comparable metros, and why? How does its reliability compare? Capital and expansion costs are out of scope.

Working hypothesis, to be tested: the gap is mostly a labor-productivity gap (staff per car-km and per station), not a wage gap. Candidate causes are crew size, maintenance and track-access practice, 24/7 service, old signaling, station staffing, and overhead. Some differences are not inefficiency (trip length, network shape, system age), and the analysis must separate them.

## Decisions

1. **Headline metrics:** operating cost per passenger-km and per trip. Cost per car-km is always shown next to them. Staff per car-km is the main labor-productivity measure.
2. **Peer set:** see [`../data/systems.csv`](../data/systems.csv). Tier 1 is the core comparison. Tiers 2 to 4 are used only where they answer a specific question. Mumbai is excluded because its main network is commuter rail, not a metro.
3. **Estimates:** allowed, but always flagged and backed by a method note (see [`../AGENTS.md`](../AGENTS.md)). The report also shows main results with estimated systems left out.
4. **Dataset:** CSV files in this repository.
5. **Rider-experience topics** (weekend service changes, crowding, station conditions) are not a focus.
6. **Time range (default, not yet confirmed):** 2000 onward for NYC and US systems, 2015 onward for foreign systems. Use 2019 as the main year for cost per trip, because of pandemic ridership effects.

## Question bank

### A. Efficiency and unit cost
1. (core) Operating cost per car-km and per train-hour.
2. (core) Operating cost per passenger-km and per trip.
3. (core) Staff per million car-km, per station, per route-km.
4. Cost split: train operations, rolling-stock maintenance, track and infrastructure maintenance, stations, administration. Which part holds most of NYC's gap?
5. Wages plus benefits per employee, relative to local wages.
6. Passengers and passenger-km per employee.
7. Real cost per car-km over time since about 2000.
8. Load factor (share of offered capacity used).

### B. Funding
9. (core) Farebox recovery ratio.
10. Sources of the remaining funding (dedicated taxes, general government, property and retail income).
11. Fare level per trip and per km, relative to local income.
12. Do systems that must cover their costs (Hong Kong, Tokyo Metro) have lower unit costs?
13. Revenue lost to fare evasion.

### C. Reliability
14. (core) On-time or schedule-adherence performance (definitions differ; within-system trends only).
15. (core) Mean distance between failures for the car fleet.
16. Delay minutes or lost customer hours per million passenger-km, by cause.
17. Planned closures and service changes.
18. Headways and wait times, peak and off-peak.

### D. Explanatory factors
24/7 service; crew size (one-person, two-person, driverless); unions and specific work rules; track access and maintenance practice; signaling (fixed-block vs CBTC); system age and state of repair; network shape (interlining, express tracks, station spacing, trip length); station design and staffing; rolling stock (fleet age, mixed fleets, car length); pensions and benefits; overtime; procurement; management and governance; policing, cleaning and security; accessibility (elevators, escalators); ridership recovery since 2019.

## Comparability rules

| Pitfall | Rule |
| --- | --- |
| Metro vs whole agency | Use metro-only figures where they exist. Otherwise allocate with a written method and give a range. Record `scope` on every row. |
| Boundary of the metro | Define the boundary per system in `data/systems.csv` and keep it fixed across years (for example Tokyo through-running, Paris RER). |
| Overhead allocation | Report cost with and without general administration. |
| Contracted vs in-house work | Compare cost first, staff second. Note the contracting model. |
| Capitalized maintenance | Record each system's rule. Where possible add a maintenance-plus-renewal measure. |
| Pensions and benefits | Keep wages and benefits separate. Test results with and without pension costs. |
| Debt service | Always excluded from operating cost. |
| Policing | Record who pays for transit police and treat it the same way in every system. |
| Currency | Keep nominal local values as reported rows. Use PPP for main comparisons; also compare against local wages. |
| Year | 2020 to 2022 are distorted. Use 2019 for per-trip measures. |
| Car size | Check per-car-km results against per-train-km or per-seat-km. |
| Trip length | Always show cost per trip next to cost per passenger-km. |
| Reliability definitions | Prefer mean distance between failures and delays per car-km for cross-system comparison. |

## Data sources found so far

- **National Transit Database (FTA):** best source for NYC and other US systems. Uniform definitions. Overhead is allocated to modes by formula.
- **Transit Costs Project (NYU Marron):** construction costs only, except a November 2025 report on train crew size with no cost figures.
- **Community of Metros (formerly CoMET and Nova, Imperial College):** 48 members including NYC and PATH. Data confidential and anonymized. Public outputs are academic papers.
- **Pedestrian Observations (Alon Levy, May 2026):** secondary estimates of cost per car-km for NYC, London, Paris and Berlin. Entered as unverified rows in `data/observations.csv`.
- **To find:** agency annual reports (TfL, RATP and IDFM, Tokyo Metro, Toei, Seoul Metro, MTR, SMRT, SBS Transit, Metro de Madrid); Japan's railway statistics yearbook; MTA budget and performance data; NY State Comptroller and Citizens Budget Commission reports; the TfL benchmarking report cited by Levy.

## Plan

1. Phase 1, scoping: done.
2. Phase 2, NYC baseline: full NTD profile of the NYC subway and US heavy-rail peers and PATH.
3. Phase 3, peer data: one set of rows per Tier 1 system, same metrics as NYC.
4. Phase 4, analysis: unit costs, the gap, and its breakdown by wage level, staffing by function, and benefits. A structured case comparison, not a regression.
5. Phase 5, report, then possibly a website built from the same data.
