# Fact-check of hand-collected data

This file records the independent fact-check of rows that other threads collected. The row-by-row record is `docs/verification_log.csv`: one line per checked row, with the result and a note.

## How rows were checked

- The checker opened each cited source again, read the value at the stated locator, and compared value, unit, period and definition. The checker read the source without looking at the value in the repo first.
- **Primary sources** (agency reports, official statistics, the Transit Costs Project survey): a matching row is set to `verification = verified`.
- **Secondary sources** (Wikipedia, blogs, news): AGENTS.md says these stay `unverified` until checked against a primary source. When the transcription matched, the row stays `unverified` and gets a note "transcription matches the cited secondary source". The log calls this `transcription_ok_secondary`.
- **Derived rows** were recomputed from their input rows (`verified_recompute`).
- **Corrections** are listed below and in the log as `corrected`.

## Results (pass 1: factors, reliability and NTD, 2026-11-26)

See the summary table at the end of this file once all passes are done.

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
