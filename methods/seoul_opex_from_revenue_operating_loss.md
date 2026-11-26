# Method: seoul_opex_from_revenue_operating_loss

**Used for:** `opex_total` of `seoul_metro`, 2022-2024 (obs_ids `seoul_metro_<year>_opex_total_est`). **These rows are estimates**, built on a secondary source, and so is every ratio built on them.

**Type:** estimated

## Inputs

| Input | obs_id |
| --- | --- |
| 매출액 (operating revenue of the whole corporation) | `seoul_metro_<year>_operating_revenue_sankun` |
| 영업이익 (operating income; negative = operating loss) | `seoul_metro_<year>_ebit_sankun` |
| Contract work for others (수탁사업원가) | Not in the source. Assumed range below. |
| Depreciation (감가상각비) | Not in the source. Assumed range below. |

## Formula

gross operating expense = 매출액 − 영업이익

opex_total = gross operating expense − contract work − depreciation

Central: contract work 70 billion won, depreciation 410 billion won.
value_low uses contract work 110 and depreciation 480 billion won; value_high uses 40 and 340 billion won.

## Assumptions

- **Gross operating expense.** For a Korean income statement, 매출액 − 영업이익 = 매출원가 + 판매비와관리비 = 영업비용. In 2019 this identity held in Seoul Metro's own statements (see `seoul_opex_excl_depreciation`).
- **Contract work.** In 2018 and 2019 수탁사업원가 was 64 and 74 billion won (`seoul_metro_<year>_opex_other_business_sm`). 40-110 billion won is assumed for 2022-2024.
- **Depreciation.** Seoul Metro's accounting summary page (`seoul_metro_accounting_page`) appeared to show about 385 billion won for 2021 and 418 billion won for 2024 (partial extraction, not verified). 340-480 billion won is assumed.
- **Ancillary businesses** stay in, as in `seoul_opex_excl_depreciation`.
- **Secondary source.** The revenue and operating income come from an aggregator page that does not name its document. They have not been checked against Seoul Metro's statements.

## Range

About ±3% around the central value from the two assumed items. Errors in the secondary source are not in the range.

## Known weaknesses

Replace with reported 영업비용, 수탁사업원가 and 감가상각비 from Seoul Metro's statements (Excel files at http://www.seoulmetro.co.kr/kr/page.do?menuIdx=110, or the data.go.kr dataset 15139455 "서울교통공사_손익계산서", which this project's tools could not download).
