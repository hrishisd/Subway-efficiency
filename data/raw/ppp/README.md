# Price factors

`ppp_deflator.csv` holds the World Bank values used by method [`ppp_usd_2024`](../../../methods/ppp_usd_2024.md):

- `ppp_<iso3>_<year>`: PPP conversion factor, GDP (LCU per international $), indicator PA.NUS.PPP. Source `worldbank_ppp`.
- `us_gdp_deflator_<year>`: US GDP deflator, index 2020 = 100, indicator NY.GDP.DEFL.ZS. Source `worldbank_us_gdp_deflator`.

Values were copied from the World Bank API on 2026-11-26 (database last updated 2026-11-11). Derived rows in `data/observations.csv` list these `factor_id`s in `inputs`, and `scripts/validate.py` accepts them there. To add a country, append rows with the same columns and a locator.
