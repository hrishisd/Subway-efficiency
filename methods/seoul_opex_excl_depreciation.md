# Method: seoul_opex_excl_depreciation

**Used for:** `opex_total` of `seoul_metro`, 2018 and 2019 (the rows for 2022-2024 use `seoul_opex_from_revenue_operating_loss`) (obs_ids `seoul_metro_<year>_opex_total_est`). **These rows are estimates**, and so is every ratio built on them.

**Type:** estimated

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| 영업비용 (operating expense of the whole corporation, including depreciation) | `seoul_metro_<year>_opex_incl_depreciation_sm` |
| 수탁사업원가 (cost of work done under contract for others) | `seoul_metro_<year>_opex_other_business_sm` |
| Depreciation (감가상각비) | Not readable in the source. Assumed range below. |

## Formula

opex_total = 영업비용 − 수탁사업원가 − depreciation

Central depreciation 370 billion won; low and high cost use 450 and 300 billion won.

## Assumptions

- **Depreciation.** The 2019 statements put depreciation in the cost-of-sales schedule (부속명세서 p.172), which this project's tools could not read. Seoul Metro's accounting summary page (`seoul_metro_accounting_page`) appears to show about 385 billion won for 2021 and 418 billion won for 2024 (read from a partial extraction, not verified). Depreciation grows over time as new assets come into service, so 2018-2019 is taken as 300-450 billion won, central 370 billion won.
- **Contract work** (수탁사업: building or running sections for other owners, such as Line 9 phase 2-3) is removed. Its revenue equals its cost in the accounts.
- **Ancillary businesses** (advertising, retail leasing, about 200 billion won of revenue in 2019) stay in, because their costs are not shown separately. Their costs are probably small (most is rent on station space).
- What remains is lines 1-8 operating cost including the corporation's own overhead. Seoul Metro's cost also includes free rides for seniors (no cost effect) and its own police-like station security staff.

## Range

value_low = 영업비용 − 수탁사업원가 − 450 billion won; value_high = 영업비용 − 수탁사업원가 − 300 billion won. About ±3.5% around the central value.

## Known weaknesses

Replace this estimate with the reported 감가상각비 once someone reads the cost schedules (Excel statements at http://www.seoulmetro.co.kr/kr/page.do?menuIdx=110, or pp.167-173 of the 결산서).
