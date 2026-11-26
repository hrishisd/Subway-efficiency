# Method: ntd_cpi_real_2024

**Used for:** money rows of US systems restated in constant 2024 US dollars: `opex_total`, `fare_revenue`, `opex_per_car_km`, `opex_excl_ga_per_car_km`, `opex_per_passenger_km`, `opex_per_trip`, `opex_per_car_hour`. These rows have obs_ids ending `_real2024_ntd` and `price_basis` = `real_USD_2024_CPI-U`.

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Nominal value | The row named in `inputs` |
| CPI-U annual average for the row's year and for 2024 | `data/price_indices.csv`, index `us_cpi_u` (source `fred_cpiaucns`) |

## Formula

real 2024 USD = nominal USD × CPI-U(2024) / CPI-U(year)

CPI-U is the US city average, all items, not seasonally adjusted, annual average (1982-84 = 100). The factor used is written in each row's `notes`.

## Assumptions

- **National CPI-U, not the New York area index.** This keeps the US systems on one deflator. NYC prices rose at a different pace from the US average, so a local index would give slightly different NYC trends.
- **Calendar-year CPI applied to NTD report years.** NTD report years are agency fiscal years, and several agencies' fiscal years end in June. The mismatch is at most half a year of inflation.
- A general price index measures what money buys for households. It does not measure transit input costs (wages, power, parts). Real cost growth here means "growth faster than general prices", not "growth in physical inputs".

## Range

Not an estimate. No range.

## Known weaknesses

- The CPI values come from FRED, which republishes the BLS series. They have not yet been checked against the BLS site directly.
- The 2025 annual average may be affected by the missing October 2025 BLS release. Not checked.
- **Not the same deflator as the international comparison.** Cross-country rows use `methods/ppp_usd_2024.md` (World Bank PPP and the US GDP deflator). These CPI-U rows are for US trends over time only. The two give slightly different 2024-dollar values for the same nominal US number.
