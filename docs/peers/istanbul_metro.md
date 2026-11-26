# Metro Istanbul: sources and comparability

Rows: `data/peers/istanbul_metro.csv`. Calendar years. **Istanbul data is very thin: there is cost for 2019 and 2020, but no trips, passenger-km or car-km, so no unit costs.**

## Why

Metro İstanbul's website (metro.istanbul), which hosts its annual reports and ridership tables, could not be fetched from the research environment, and neither could copies in the Internet Archive. The only primary source reached is the Turkish Court of Accounts (Sayıştay) audit report on the company for 2020.

## What the data is

| Item | Source | Years | Notes |
| --- | --- | --- | --- |
| Cost of sales, operating expenses, total | Sayıştay 2020 audit, Tablo 3 | 2019, 2020 | Company total: metro, tram, funicular and cable car. **Includes depreciation** (Turkish accounts put it in cost of sales). |
| Net sales | Same | 2019, 2020 | Mostly travel revenue; the split between fares and municipal payments is not given. |
| Staff | Same, section 1.2 | 2020 | 2,700 at year end, head count. |

## Comparability with NYC

- Not comparable yet: no service or ridership denominators.
- Cost scope differs from NTD in two ways: it includes depreciation, and it covers tram, funicular and cable-car lines as well as metro.
- Turkish inflation was very high after 2021. Use 2019 for any comparison (see method `ppp_usd_2024`).

## To find

Metro İstanbul annual reports (Faaliyet Raporu) 2015-2024 and its "Annual Passenger Figures of the Lines" tables, both on metro.istanbul. A person with a normal browser can download them.
