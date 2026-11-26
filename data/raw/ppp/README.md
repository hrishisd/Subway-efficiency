# Price factors

`ppp_deflator.csv` holds the price factors used by method [`ppp_usd_2024`](../../../methods/ppp_usd_2024.md):

- `ppp_<iso3>_<year>`: PPP conversion factor, GDP (LCU per international $), indicator PA.NUS.PPP. Source `worldbank_ppp`.
- `us_gdp_deflator_<year>` (2000-2025): US GDP implicit price deflator, index 2017 = 100, BEA series A191RD3A086NBEA via FRED. Source `fred_gdp_deflator`. This is the **only** US deflator in the repository: method `ppp_usd_2024` (peer rows) and method `ntd_gdp_deflator_real_2024` (US NTD rows) both use it, so every 2024-dollar value is on the same basis.

PPP values were copied from the World Bank API on 2026-11-26 (database last updated 2026-11-11). Deflator values were copied from FRED on 2026-11-26. Derived rows in `data/observations.csv` list these `factor_id`s in `inputs`, and `scripts/validate.py` accepts them there. To add a country, append rows with the same columns and a locator.
