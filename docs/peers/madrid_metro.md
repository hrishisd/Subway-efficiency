# Metro de Madrid: sources and comparability

Rows: `data/peers/madrid_metro.csv`. Calendar years.

**Madrid's cost figures are ESTIMATES.** Metro de Madrid's own annual report and accounts were not reachable from the research environment (its website blocks automated access). Cost comes from regional-government press releases about the accounts (2018, 2019) and the 2024 budget. See method [`madrid_opex_from_press`](../../methods/madrid_opex_from_press.md).

## What the data is

| Item | Source | Years | Notes |
| --- | --- | --- | --- |
| Car-km | CRTM (regional transport authority) annual reports, supply table by operator | 2015-2023 | Metro only; light rail is a separate column. 2019 from the 2019 report. |
| Trips | CRTM annual reports, demand table by operator; Comunidad de Madrid press releases for 2023 and 2024 | 2015-2024 | Several CRTM values were read through an automated summary, not verbatim (see row notes). |
| Operating cost | **ESTIMATE** from press releases | 2018, 2019, 2024 | 2018 and 2019: income minus operating result before depreciation and financial costs. 2024: budgeted cost of services. ±5%. |
| Fare revenue | **ESTIMATE**: 2024 budgeted fare share | 2024 | Fares are pooled by the CRTM for the whole region and assigned to operators. |
| Staff | Press releases (head count) | 2018, 2024 | Company head count, not FTE. |
| Route length, stations | CRTM | 2015, 2019, 2023 | 269.5 km and 237 stations, excluding the TFM concession section of line 9. |

## Comparability with NYC

- **Cost scope.** The 2018 and 2019 estimates exclude depreciation and interest, like NTD. The 2024 budget may include capital charges; it is not stated.
- **Company vs metro.** Metro de Madrid S.A. also runs light-rail line ML1. Its cost is a few percent of the total and is not separated.
- **Trips** are entries to the metro network, so a change between metro lines is one trip, as in London.
- **Cars are short.** Madrid's fleet mixes narrow-profile and wide-profile cars, many shorter than NYC cars. Compare per trip and per car-km together.
- **No passenger-km** figure was found, so Madrid has no cost per passenger-km.
- **PPP.** Spain's price level is low, so converting at PPP raises Madrid's costs in dollars much more than converting at market exchange rates would.

## Not found

- Metro de Madrid's audited accounts (cost by type, staff costs), any year.
- Passenger-km and train-km.
- Operating cost for 2015-2017 and 2020-2023.
