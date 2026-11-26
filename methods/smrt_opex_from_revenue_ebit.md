# Method: smrt_opex_from_revenue_ebit

**Used for:** `opex_total` of `singapore_mrt` (SMRT Trains only), financial years 2014/15, 2015/16 and 2021/22 to 2023/24 (obs_ids `singapore_mrt_<year>_opex_total_est`). **Estimates.**

**Type:** estimated

## Why an estimate is needed

SMRT Corporation has not been listed since 2016 and its Group Reviews give only SMRT Trains' revenue, EBIT and profit, not its costs. SBS Transit (the other rail operator) reports bus and rail together. No public source gives Singapore MRT operating cost directly.

## Inputs

| Input | obs_id |
| --- | --- |
| SMRT Trains revenue | `singapore_mrt_<year>_operating_revenue_smrt` |
| SMRT Trains EBIT | `singapore_mrt_<year>_ebit_smrt` |

## Formula

opex_total ≈ revenue − EBIT

- value_low = 0.80 × (revenue − EBIT): removes an assumed up-to-20% share for depreciation of operator-owned assets and licence charges paid to the Land Transport Authority (LTA). Under the New Rail Financing Framework, LTA owns the trains and infrastructure and charges the operator a licence fee; these are capital-type costs that NTD operating expense for US systems does not contain.
- value_high = 1.10 × (revenue − EBIT): adds back other operating income (which raises EBIT without being revenue), for example government grants such as the Rail Reliability Incentive (2020-2023).
- For FY2023/24 the high end is 1.25 ×, because the operating data for that year include the Thomson-East Coast line while its costs may sit in a separate company (SMRT TEL Pte Ltd).

## Assumptions

- SMRT Trains' revenue and the operating data in the same table cover the same lines (North-South, East-West and Circle lines; plus Thomson-East Coast in FY2023/24).
- SBS Transit's lines (North East, Downtown, and LRTs) are not covered. These rows describe SMRT Trains, not the whole Singapore MRT.

- **FY2014/15 and FY2015/16** come from the 2016 annual report (`smrt_ar_2016`), where SMRT split Rail into Train (MRT) and LRT. These rows use the Train figures, so the Bukit Panjang LRT is excluded. SMRT then still owned its trains (before its move to the New Rail Financing Framework), so depreciation is a larger share of cost; the low end (0.80×) covers this. FY2015/16 EBIT includes a S$16.4 million property tax refund, about 2.5% of cost, inside the high end. There are no car-km or ridership figures for these years, so they give a cost trend only.

## Range

As above.

## Known weaknesses

- No staff numbers, so no labor-productivity ratios for Singapore.
- Pandemic-affected years: FY2021/22 especially.
- SMRT's year runs April to March; `year` is the starting calendar year.
