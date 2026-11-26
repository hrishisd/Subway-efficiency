# Method: madrid_opex_from_press

**Used for:** `opex_total` for `madrid_metro` in 2018, 2019 and 2024, and `fare_revenue` in 2024. **These are ESTIMATES.** Metro de Madrid's own annual report and accounts could not be reached from the research environment (metromadrid.es blocks automated access), so the figures come from regional-government press releases.

**Type:** estimated

## Inputs

| Year | Input | source_id + locator |
| --- | --- | --- |
| 2018 | Company income 1,046 million EUR; operating result before depreciation and financial costs 134 million | `cam_press_2019_05_metro_accounts_2018` |
| 2019 | Company income 1,054 million EUR; operating result before depreciation and financial costs 159 million | `cam_press_2020_07_metro_accounts_2019`, paragraphs 2 and 3 |
| 2024 | Budgeted cost of Metro services, about 987 million EUR; of which 414.2 million to be covered by fares | `cam_press_2023_12_metro_funding_2024`, paragraph 3 |

## Formula

- 2018 and 2019: opex_total = income − operating result before depreciation and financial costs. This gives operating cost **excluding depreciation and interest**, which matches the NTD definition used for NYC.
- 2024: opex_total = the budgeted cost as printed; fare_revenue = the budgeted fare share as printed.

## Assumptions

1. **All company income is operating income.** If part of the 1,054 million is financial or extraordinary income, operating cost is lower than the estimate.
2. **The company is the metro.** Metro de Madrid S.A. also runs light-rail line ML1 (a few percent of its service). Its costs are not separated.
3. **The 2024 budget is close to the actual.** Budgets set before the year can differ from outturn by several percent. The 987 million may also include capital charges (depreciation or financing of rolling stock) that the 2018-2019 estimates exclude; this is not stated.

## Range

±5% around each central value, for assumptions 1 to 3. The 2018 and 2019 values (912 and 895 million) differ in a way that does not fit the press release's statement that operating costs grew 1.7% in 2019, which shows the precision is no better than this.

## Known weaknesses

- Press releases round figures and do not define their terms.
- There is no Madrid staff figure or passenger-km figure from a primary source yet, so Madrid has no cost per passenger-km or staff ratios.
- Replace these rows with figures from Metro de Madrid's audited accounts ("Cuentas anuales" and "Informe de gestión") when they can be reached.
