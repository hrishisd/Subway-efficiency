# Method: ntd_gdp_deflator_real_2024

**Used for:** money rows of US systems restated in constant 2024 US dollars: `opex_total`, `fare_revenue`, `opex_per_car_km`, `opex_excl_ga_per_car_km`, `opex_per_passenger_km`, `opex_per_trip`, `opex_per_car_hour`, `opex_per_train_km`. These rows have obs_ids ending `_real2024_ntd` and `price_basis` = `real_USD_2024_GDP_deflator`. Built by `scripts/build_ntd_baseline.py`.

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Nominal value | The first obs_id in `inputs` |
| US GDP deflator for the row's year and for 2024 | `us_gdp_deflator_<year>` and `us_gdp_deflator_2024` in `data/raw/ppp/ppp_deflator.csv` (source `fred_gdp_deflator`, BEA series A191RD3A086NBEA, 2017 = 100). Both factor ids are listed in `inputs`. |

## Formula

real 2024 USD = nominal USD × deflator(2024) / deflator(year)

The factor used is written in each row's `notes`.

## Why the GDP deflator and not CPI-U

The international comparison (method [`ppp_usd_2024`](ppp_usd_2024.md)) turns foreign currency into US dollars of year t with GDP purchasing-power parities, then into 2024 dollars with the US GDP deflator. The GDP deflator is the price index that matches GDP PPPs. Using the same deflator for the US rows means an NYC value in 2024 dollars and a London value in PPP 2024 dollars are on exactly the same basis. Decided 2026-11-26. Before that, these rows used CPI-U (method `ntd_cpi_real_2024`, now removed), which gave 2024-dollar values about 2% higher for 2019. The CPI-U series stays in `data/price_indices.csv` for anyone who wants a consumer-price view.

## Assumptions

- **National deflator, not a New York index.** No metro-area GDP deflator is used. NYC prices rose at a different pace from the US average.
- **Calendar-year deflator applied to NTD report years.** NTD report years are agency fiscal years, and several agencies' fiscal years end in June. The mismatch is at most half a year of inflation.
- A general price index measures the price of all domestic output. It does not measure transit input costs (wages, power, parts). Real cost growth here means "growth faster than general prices", not "growth in physical inputs".

## Range

Not an estimate. No range.

## Known weaknesses

- The deflator values come from FRED, which republishes the BEA series. They have not yet been checked against the BEA site directly.
- BEA revises the deflator (annual and comprehensive updates). Values were taken on 2026-11-26.
