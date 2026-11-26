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

## Results (pass 2: European and Asian peer data, 2026-11-26)

Pass 2 checked the peer rows from PRs 7 and 8 and re-checked the deflator change from PR 10.

| Data | Rows checked | Matched source | Needed a fix |
| --- | --- | --- | --- |
| Hong Kong MTR (ten-year statistics, annual results 2020 and 2025) | 102 | 102 | 0 |
| Singapore SMRT annual reports | 18 | 18 | 0 |
| Seoul Metro 2019 settlement report | 16 | 16 values | 4 page locators |
| Tokyo (MLIT FY2019 and FY2023, Tokyo Metro yuho FY2020, Toei audit FY2023) | 42 | 42 | 0 |
| London (TfL QPR 2024/25, Travel in London Tables 1, 2 and 9, financial statements 2019/20) | 38 | 38 | 0 (one restatement note) |
| Paris STRMTG 2019 and 2024; Berlin BVG | 14 | 14 | 0 |
| Istanbul Sayıştay audit | 7 | 7 | 0 |
| Madrid (CRTM reports, regional ridership releases, inputs of the cost estimate) | 14 | 14 | 0 |
| Beijing (Jiemian news, secondary) | 2 | 2 transcriptions match | 0 |
| Peer derived rows: PPP conversions (value, low, high) | 369 | 369 | 0 |
| Peer derived rows: unit ratios and other methods | about 400 | all | 0 |
| US GDP deflator from FRED (`us_gdp_deflator_2000` to `_2025`) | 26 | 26 | 0 |
| NTD `_real2024` rows on the new deflator | 557 recomputed | 557 | 0 |

Error rate in pass 2: no wrong numbers in about 1,550 checked values. The only fixes were four wrong page numbers in the Seoul locators (업무량 p.15, 직원 현황 p.13, summary p.16, pp.28-31).

After the deflator change, the 88 rows that PR 10 marked `SUPERSEDED` recompute from verified inputs and the re-fetched FRED series, so they are `verified` again.

Estimated rows (289, mostly Madrid, Seoul and Tokyo cost splits) stay `unverified` on purpose: their inputs were checked (`source_value_ok`) but the assumptions are not facts a source can confirm.

### Open points from pass 2

- London 2023 indirect cost: 456 (GBP m) in the cited QPR 2023/24, but the QPR 2024/25 prior-year column restates it as 455. Not changed; the row cites the earlier report correctly.
- Travel in London table pages: the PDF page and the printed page differ by one. Locators use the PDF page.
- MLIT `001745001.pdf`: the values match, but the fiscal-year label was not visible in the text extraction.
- Seoul depreciation is an assumption (300-450 billion won). The report shows only 3.49 billion won of depreciation in selling and admin costs; cost-of-sales depreciation was not found.
- Beijing 2019 (Jiemian) gives no primary source; stays `unverified`.
- Hong Kong `employees_fte` values are year-end headcounts, not full-time equivalents.
- Not re-checked in pass 2: TfL QPRs before 2024/25 (except overlapping columns), MLIT FY2015-2018 and FY2020-2022, CRTM 2016-2022 car-km, Toei FY2018-2022, other yuho years, MTR results 2017, 2018, 2021 and 2023, rolling-stock fact sheets, INSEE, and Alon Levy's blog.

## Overall

Across the three passes, about 4,500 values were checked against their sources or recomputed. No wrong number was found. About 10 hand-collected rows (roughly 2%) had a wrong scope, locator, wording or outdated fact. The only material correction is WMATA's automation status (automatic train operation restarted on the Red Line in December 2024).

## Results (pass 3: follow-up peer data from PRs 12 and 13, 2026-11-26)

| Data | Rows checked | Result |
| --- | --- | --- |
| Seoul 2018 (prior-year column of the 2019 settlement): fare revenue, operating expense, contract-work cost, staff | 4 | all match; now `verified` |
| Seoul 2024 ridership, train-km, stations (Seoul city article of 2025-02-21) | 3 | all match; now `verified` |
| Seoul 2022-2024 revenue and operating income (sankun.com aggregator) | 6 | transcriptions match; stay `unverified` (secondary, names no document) |
| Singapore SMRT Train revenue and EBIT, FY2015 and FY2016 (Annual Report 2016) | 4 | values agree, but only through an extraction summary of the chart; Train + LRT sums match the verbatim Rail totals on p.9. Stay `unverified` |
| Berlin U-Bahn cost per trip 2017 (Abgeordnetenhaus Drucksache 18/15985, Frage 14, p.6) | 1 | matches (0,93 EUR, includes attributable infrastructure); now `verified` |
| New estimated rows (Seoul opex 2022-2024, Seoul car-km 2024, SMRT opex FY2015-16) | 6 | recompute with their method notes, including low and high |
| PPP rows after the rebuild | 385 (+90 low, +90 high) | all recompute |

No wrong numbers. One fix: PR 12 regenerated the Seoul rows from `scripts/build_seoul_singapore_inputs.py`, which still held the old page numbers, so the pass 2 locator fix was lost. The fix is now in the script itself (업무량 p.15, 직원 현황 p.13, summary p.16, income statement pp.28-31).

Open point: the Seoul 2022-2024 cost estimates rest on an aggregator page and on assumed depreciation (340-480 billion won). They should be replaced with Seoul Metro's own statements when those can be downloaded.
