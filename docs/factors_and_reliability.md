# Explanatory factors and reliability (phase 3 support data)

Added 2026-11-26. This file explains `data/factors.csv`, `data/reliability.csv` and their definition files. Every row cites a source and a locator. All rows are `unverified` until a second agent checks them.

## Files

| File | What it holds |
| --- | --- |
| `data/factor_definitions.csv` | One row per factor: name, kind (categorical, numeric or text), allowed values, definition. |
| `data/factors.csv` | One row per system, factor and source. Text and categorical values are allowed. A system can have several rows for one factor when sources differ. |
| `data/reliability_metrics.csv` | One row per reliability metric, with a flag for whether it can be compared across systems. |
| `data/reliability.csv` | Reliability values. Every row quotes the agency's own metric name and definition in `agency_metric_name` and `agency_definition`, because definitions differ. |
| `data/raw/ntd/opex_by_type_hr_2024.csv` | NTD operating expense by object class, 2024, for the seven US heavy-rail systems (input to the benefit-share rows). |

`scripts/validate.py` now checks both new files with the same rules as `observations.csv`.

## What the data says so far

### Crew size: NYC is the outlier

The Transit Costs Project (Nov 2025) surveyed over 400 lines in 36 cities and found that "fewer than 6.25%" use two-person crews. It calls New York "almost globally unique in maintaining TPTO". Every foreign peer the report covers runs one-person or unattended trains on all or almost all lines (Tokyo Metro and Toei are not identified in it). The exception is Seoul, where lines 1 to 4 still have two-person crews.

In NYC, two-person crews come from the TWU Local 100 contract, not from state law. A bill to write them into law was vetoed in December 2025. One-person operation already runs on parts of the A, G, M and 5 and on all shuttles. Reason, citing the Citizens Budget Commission, puts the saving from one-person crews at $442 million a year (secondary; the CBC report is not yet checked).

### 24/7 service and maintenance windows

NYC runs 24/7 and works around trains by using express tracks. Paris closes about 4.5 to 5 hours each weeknight. Berlin closes about 3.5 hours on weeknights and runs all night on weekends. Madrid closes about 02:00 to 06:00 (from a summary of a Wikipedia section; to verify). Copenhagen runs 24/7 but is driverless and single-tracks around work sites. Source for the cost link: Alon Levy, "Overnight Public Transit" (2019), who argues that constant work around live trains makes NYC maintenance very expensive. This is a secondary argument and should be tested in the analysis phase.

### Signaling

About 85% of the NYC system still uses fixed-block signals (Wikipedia, 2025). CBTC runs on the L (2009) and the 7 (2019); four more projects are delayed to late 2027 or 2028. Most peers already run automatic train operation (GoA2) on most lines, and Paris, Singapore, Istanbul, Hong Kong, Shanghai and Beijing have fully automatic (GoA4) lines.

### Benefits share (US systems only)

NTD 2024 fringe benefits as a share of labor cost: NYC 40.6%, PATH 48.8%, CTA 39.2%, SEPTA 36.0%, WMATA 33.0%, MBTA 32.0%, BART 25.7%. NYC is high but not the highest. No comparable foreign figures were found.

### Reliability

| System | Car-km per failure | Definition of a failure | Period | Source |
| --- | --- | --- | --- | --- |
| NYC Subway | about 198,000 (123,293 car-miles) | Mechanical problem causing a delay | 2025 | MTA via data.ny.gov (pooled by us); LTA compilation gives 198,000 car-km |
| Hong Kong MTR | 4,822,007 and 8,085,886 (two line groups) | Train failure causing a delay of 5 minutes or more | 2025 | MTR Annual Report 2025 |
| Singapore MRT | 7,747,000 (LTA conversion from 1,606,000 train-km) | Delay of more than 5 minutes | 2025 | LTA |

Even allowing for different definitions, NYC trains fail roughly 25 to 40 times as often per car-km as trains in Hong Kong or Singapore. NYC's pooled MDBF has also fallen from about 141,000 miles (2019) to about 123,000 miles (2025).

Service delivered (share of scheduled train-km run), as compiled by Singapore's LTA: Hong Kong 99.9%, Singapore 99.8%, Berlin 95.7%, NYC 94.2%, London 91.8%. Berlin's own figure is 94.3% for 2025. These use each system's own measure, so treat them as rough.

London's own series (Travel in London 2024 Table 9 and 2025 Table 4) shows scheduled train-km operated of 96.6% to 97.6% from 2013/14 to 2018/19, then 94.0% in 2019/20, a low of 87.2% in 2020/21, and a slow recovery to 91.0% in 2024/25. TfL blames train operator availability, lack of rolling stock and asset condition on the Central and Bakerloo lines.

NYC terminal on-time performance (pooled by us, all lines and days): 63% to 70% in 2015-2018, then 81% to 89% from 2019. The jump in 2019 is probably a change in the MTA's on-time standard, not a real improvement. Use within-period trends only.

Japan: Tokyo Metro had 12 transport disruptions (cancellation or delay of 30 minutes or more) in FY2024. Per million train-km (LTA compilation), Tokyo Metro had 0.26 and Toei 0.06 such delays in 2024.

## Gaps (not found or not readable)

- **London lost customer hours, excess journey time and fleet failure rates.** Scheduled km operated (2013/14 to 2024/25) and the journey time metric are now in the data. The other measures are only in the LU Performance Data Almanac (xlsx), which this environment cannot download: the proxy blocks data.london.gov.uk and web.archive.org, and the fetch tool returns spreadsheets as unreadable binary. TfL board papers that may hold them refuse automated access. Next step: download the almanac on a machine with normal internet access.
- **Paris network-wide figure and full-year 2024.** Only January-September 2024 per-line contract punctuality is in the data. The IDFM bulletin index page refused automated access.
- **Madrid reliability, staff, hours and signaling.** The CRTM report has network size and funding only. The Metro de Madrid financial document was blocked.
- **Seoul, Shanghai, Beijing, Istanbul** primary reliability data. Only LTA's compiled punctuality figures are available.
- **Crew model for US peers** (PATH, WMATA, MBTA, SEPTA, CTA, BART) and for Tokyo Metro and Toei. The Transit Costs Project does not cover them.
- **Unions and work rules** outside NYC. Not yet collected.
- **Pension and benefit share** outside the US.
- **Platform screen doors** for most systems; only Tokyo Metro (94% of stations) and partial Hong Kong data.
- **Train length (cars and meters), express tracks and interlining** outside NYC.
- **Outsourcing / contracting model** for each system.
- **NYC MDBF definition detail** and the date of the MTA's on-time standard change.
- **Wikipedia revision ids** were not captured; rows citing Wikipedia should be re-checked against a permanent link.
