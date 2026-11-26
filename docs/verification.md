# Fact-check of hand-collected data

This file records the independent fact-check of rows that other threads collected. The row-by-row record is `docs/verification_log.csv`: one line per checked row, with the result and a note.

## How rows were checked

- The checker opened each cited source again, read the value at the stated locator, and compared value, unit, period and definition. The checker read the source without looking at the value in the repo first.
- **Primary sources** (agency reports, official statistics, the Transit Costs Project survey): a matching row is set to `verification = verified`.
- **Secondary sources** (Wikipedia, blogs, news): AGENTS.md says these stay `unverified` until checked against a primary source. When the transcription matched, the row stays `unverified` and gets a note "transcription matches the cited secondary source". The log calls this `transcription_ok_secondary`.
- **Derived rows** were recomputed from their input rows (`verified_recompute`).
- **Corrections** are listed below and in the log as `corrected`.

## Results (pass 1: factors, reliability and NTD, 2026-11-26)

| Data | Rows checked | Matched source | Needed a fix | Not checked |
| --- | --- | --- | --- | --- |
| `factors.csv`, primary sources | 43 | 42 | 1 (scope) | 0 |
| `factors.csv`, secondary sources (Wikipedia, blogs, news) | 88 | 87 transcriptions match | 1 outdated fact (WMATA), plus 1 unsupported phrase in a primary-source row | 0 |
| `reliability.csv` (incl. London series from PR 5) | 188 | 184 | 0 value errors; 2 locator or wording issues | 4 NYC trip-count inputs |
| `observations.csv`, NTD reported rows | 272 re-fetched of 1,718 (16%) | 272 | 0 | rest covered by rebuild check |
| `observations.csv`, derived rows | all 1,798 recomputed | 1,798 | 0 | 0 |
| PPP factors and US deflator (`data/raw/ppp/ppp_deflator.csv`) | 121 | 121 | 0 | 0 |
| CPI-U (`data/price_indices.csv`) | 26 | 26 | 0 | 0 |

Rebuild check: `scripts/build_ntd_baseline.py` rebuilds `observations.csv` byte for byte from `data/raw/ntd/`. The raw files were checked against the NTD API for NYCT (all TS2.1 fields 2015-2025), CTA employees, WMATA breakdowns, and NYCT and BART operating expense by type. The NYCT 2012-2014 profile rows match the three FTA profile PDFs and their printed cost ratios.

Error rate in pass 1: no wrong numbers were found in about 2,350 checked values. Six rows had a wrong scope, locator, wording or stale fact (about 2% of the 320 hand-collected rows). One of these is material: WMATA's automation status.

Rows that pass and come from primary sources are now `verified` (43 factors, 165 reliability rows, 546 observations). Rows from secondary sources stay `unverified` with a note, as AGENTS.md requires.

**Update 2026-11-26 (after pass 1): one US deflator.** All 2024-dollar rows now use the BEA GDP implicit price deflator from FRED (source `fred_gdp_deflator`, factors `us_gdp_deflator_2000` to `_2025` in `data/raw/ppp/ppp_deflator.csv`). This replaced the World Bank copy of the US deflator (checked in pass 1) for PPP rows, and CPI-U for the NYC and US `_real2024_ntd` rows. Values moved by 0.1% (PPP rows) to about 2% (US real rows). The 88 verified rows whose value changed, and the 11 old deflator factors, are marked `SUPERSEDED` in the log and are `unverified` until checked again. Rows whose value did not change keep their `verified` mark. The CPI-U series in `data/price_indices.csv` is kept but no row uses it.

## Corrections made in pass 1

| Row | Problem | Fix |
| --- | --- | --- |
| `wmata_metrorail_automation_goa_wikipedia` | Wikipedia says WMATA runs in manual mode since 2009. This is out of date: WMATA restarted automatic train operation on the Red Line on 15 Dec 2024, and NBC4 reports Blue, Orange and Silver from June 2025. | Note added marking the row outdated. New row `wmata_metrorail_automation_goa_wmata` cites the WMATA press release (primary). |
| `nyc_subway_cbtc_share_lines_mta` | Said "Queens Boulevard in final stages". The cited MTA page does not say this. | Replaced with what the MTA timeline says (contracts 2015-2017). |
| `docs/factors_and_reliability.md` | Said four CBTC projects are delayed. The Streetsblog article names three delayed projects (Fulton St/8 Av, Queens Blvd east, Crosstown); the fourth (A/C) is not described as late. | Changed to three. |
| `hong_kong_mtr_funding_mix_mtr` | Scope was `metro_only`, but the MTR table covers the whole Hong Kong Transport Operations segment (heavy rail, light rail and buses). | Scope set to `whole_agency`. |
| `hong_kong_mtr_platform_screen_doors_mtr` | Locator said p. 24; the platform-gate paragraph is on p. 25. | Locator fixed. |
| `madrid_metro_crew_model_tcp` | Locator said p. 9; the Madrid table runs over pp. 9-10. | Locator fixed. |

## Open points found in pass 1

- `beijing_subway_crew_model_tcp`: our reading of the Transit Costs Project table also lists lines 16, 17 and 19 as unattended. The PDF text is flattened, so the row notes ask a later reader to check the layout.
- `hong_kong_mtr_platform_screen_doors_mtr`: the label `most_stations` is a judgment; the source does not state network coverage.
- `nyc_subway_unionization_streetsblog`: Streetsblog writes "Transit Workers Union"; the union's name is Transport Workers Union (as Reason writes it). The row value already uses the right name.
- The London rows from Travel in London 2024 matched, but the text extraction placed Table 9 on printed p. 26, not p. 25. Not changed, because the extraction's page mapping was uncertain.
- Four NYC on-time-performance input rows (2023 and 2025 on-time and scheduled trips) were not re-queried; the derived ratios for those years recompute correctly from them.
