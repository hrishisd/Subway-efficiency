# Paris Métro: sources and comparability

Rows: `data/peers/paris_metro.csv`. Calendar years. **Paris has no cost figure.** It has trips, train-km, length and stations for 2019 and 2024 (trips also 2018).

## What the data is

| Item | Source | Years |
| --- | --- | --- |
| Trips | STRMTG (French metro safety regulator) annual reports, Tableau 1; INSEE for 2018 | 2018, 2019, 2024 |
| Train-km ("km commerciaux") | STRMTG, Tableau 1 | 2019, 2024 |
| Route length, stations | STRMTG, Tableau 1 | 2019, 2024 |

## Why there is no cost

RATP runs the metro, two RER lines, trams and buses under one contract with Île-de-France Mobilités (IDFM). Neither RATP's reports nor IDFM's budget documents that could be reached give cost, staff or fare revenue for the metro alone. The documents that might (RATP's statutory accounts at the back of its annual financial reports) were cut off before those pages when read by the research tools. The only metro-specific money figure found is the regulated pay of RATP's infrastructure manager (about €856 million in 2021, in 2020 euros, set by the Autorité de régulation des transports), but it covers metro **and** RER infrastructure and excludes train operation, so it is not usable as metro operating cost.

A cost estimate would need RATP's total operating cost and a split by mode (for example by train-km or staff). Both inputs are missing, so no estimate is made.

## Comparability notes

- **Trips** are entries to the metro network as reported by RATP; changes between metro lines are not counted again.
- **Train-km** is the regulator's "km commerciaux". Paris trains are short (most lines run 5 or 6 cars; lines 3bis and 7bis run 3 or 4), so per-train costs are not comparable with NYC's 9-car trains without a car-km figure.
- **Stations** are counted per line (a station served by four lines counts four times).

## To find

RATP Epic accounts (charges d'exploitation, staff costs, FTE) and any IDFM or Cour des comptes document with metro cost. RATP's "Rapport financier" for each year has the Epic accounts near the end.
