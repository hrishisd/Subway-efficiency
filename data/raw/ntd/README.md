# Raw NTD extracts

These files hold the National Transit Database (NTD) values that `scripts/build_ntd_baseline.py` turns into rows of `data/observations.csv`. They are kept so that anyone can check a row against the source without running the queries again.

All three come from the DOT Open Data Portal (data.transportation.gov), opened on 2026-11-26. Each file keeps the values exactly as published. Only the layout changed: TS2.1 is pivoted from one row per value to one column per year, and only the needed columns and agencies are kept.

| File | Source (`source_id`) | Query |
| --- | --- | --- |
| `ts21_hr_2015_2025.csv` | `ntd_ts21_by_mode` (dataset `npsm-38gk`) | `https://data.transportation.gov/resource/npsm-38gk.csv?ntd_id=<NTD ID>&mode=HR&$select=type_of_service,report_year,field,value&$limit=2000`, one query per agency |
| `employees_hr_2022_2025.csv` | `ntd_employees_by_mode` (dataset `uyv8-9jek`) | `https://data.transportation.gov/resource/uyv8-9jek.csv?mode=HR&$limit=500` |
| `breakdowns_hr_2022_2025.csv` | `ntd_breakdowns` (dataset `amkt-4ehs`) | `https://data.transportation.gov/resource/amkt-4ehs.csv?mode=HR&$limit=500` |

Agencies (all heavy rail `HR`, directly operated `DO`):

| NTD ID | Agency name in NTD | system_id |
| --- | --- | --- |
| 20008 | MTA New York City Transit | nyc_subway |
| 20098 | Port Authority Trans-Hudson Corporation | path |
| 30030 | Washington Metropolitan Area Transit Authority | wmata_metrorail |
| 10003 | Massachusetts Bay Transportation Authority | mbta_subway |
| 30019 | Southeastern Pennsylvania Transportation Authority | septa_subway |
| 50066 | Chicago Transit Authority | chicago_l |
| 90003 | San Francisco Bay Area Rapid Transit District | bart |

The MTA Staten Island Railway is a separate NTD reporter (NTD ID 20099). It is **not** inside the NYC subway figures.

## How the extracts were checked

The session that made these files could not download from data.transportation.gov directly; the responses came back through a web-fetch tool as text. To catch copying errors, `scripts/build_ntd_baseline.py` checks the files before it writes anything:

- In TS2.1, the four operating-expense functions add up exactly to total operating expense, for all 77 agency-years.
- In the Employees table, the five functions add up to the total, for both hours and counts, in every row.
- In the Breakdowns table, major plus other failures equal total failures.
- Car revenue miles in the Breakdowns table equal vehicle revenue miles in TS2.1 for all 28 agency-years that are in both. These are two separate datasets, so this is an independent check.
- NYC values for 2019 and 2024 were fetched twice in separate queries, and they matched.

All rows stay `unverified` until a second person or agent checks them against the portal.

## Gaps

- **2000 to 2014.** The portal copy of TS2.1 starts in 2015. Earlier years are in the archive workbook "Archive 1991-2014 TS2.1 Service Data and Operating Expenses Time Series by Mode.xlsx", linked from https://www.transit.dot.gov/ntd/data-product/ts21-service-data-and-operating-expenses-time-series-mode-1991-2014 . That file could not be downloaded in this session.
- **Employees and failures before 2022** are in the yearly NTD Employees and Breakdowns tables for earlier years. Not yet pulled.
- **Train hours** are not in any of these three datasets.
