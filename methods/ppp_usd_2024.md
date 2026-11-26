# Method: ppp_usd_2024

**Used for:** every money row converted to 2024 US dollars at purchasing power parity (`price_basis` = `PPP_USD_2024`, obs_id suffix `_ppp24`). Built by `scripts/build_peers.py`. Any system can use it.

**Type:** derived (or estimated, when the input row is an estimate)

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Money value in nominal local currency for year t | The first obs_id in `inputs` |
| PPP conversion factor for the country, year t (LCU per international $) | `ppp_<iso3>_<t>` in `data/raw/ppp/ppp_deflator.csv`, from source `worldbank_ppp` |
| US GDP deflator, year t and 2024 | `us_gdp_deflator_<t>` and `us_gdp_deflator_2024` in the same file, from source `fred_gdp_deflator` (BEA series A191RD3A086NBEA, 2017 = 100) |

## Formula

value_PPP_USD_2024 = value_LCU_t / PPP_t × (US_deflator_2024 / US_deflator_t)

Step 1 turns local currency into international dollars of year t (by definition, US dollars of year t). Step 2 restates year-t US dollars in 2024 US dollars with the US GDP deflator.

Ratios in money (for example cost per car-km) are converted the same way, which gives the same result as dividing the converted cost by the physical quantity.

## Assumptions

- **GDP PPP, not a transport-specific PPP.** The World Bank factor prices the whole economy's output. Metro cost is mostly labor, so a comparison at local wages is also useful (planned for phase 4).
- **Year t is the row's `year`.** For fiscal years that do not match the calendar year (for example TfL's April to March year), `year` is the calendar year in which the fiscal year starts, and this method uses that year's factor. The error from this is a few percent at most, except in high-inflation Turkey (see below).
- **Euro countries use their own national PPP factor** (France, Spain and Germany differ), not one euro-area rate.
- **US dollar rows (US systems)** have PPP = 1, so only the deflator applies.
- **One US deflator everywhere.** The NYC and other US constant-dollar rows (method `ntd_gdp_deflator_real_2024`) use the same `us_gdp_deflator_<year>` factors, so a peer value in PPP 2024 dollars and an NYC value in 2024 dollars can be compared directly. Until 2026-11-26 the US rows used CPI-U, which gave values about 2% different.

## Range

Not an estimate. Estimated input rows keep their estimate flag, and their low and high values are converted with the same factor.

## Known weaknesses

- The World Bank revises PPP factors when new International Comparison Program rounds come out. Values were taken on 2026-11-26 (database last updated 2026-11-11).
- **Turkey:** prices rose very fast after 2021 (the lira PPP factor went from 2.75 in 2021 to 11.55 in 2024). An annual factor applied to a flow of costs spread across the year is less exact. Read Istanbul's converted values after 2021 with care, and prefer 2019.
- 2025 factors are the World Bank's latest values and are more likely to be revised.
