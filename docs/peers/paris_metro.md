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

**Second search (2026-11-26), stopped.** These documents were read, each only in part because the research tool returns about 80,000 to 95,000 characters per PDF:
- The IDFM-RATP operating contracts for 2016-2020 and 2021-2024. The text read covers the general articles, not the financial titles (2016-2020: Titre VI, pp. 117-133; 2021-2024: Titre III, pp. 87-136). Their tables of contents show the payments are set per contract party, not per mode: an operating contribution "C1"/"C11" (2016-2020) and, from 2021, separate payments to RATP as transport operator ("R1", "R2") and as infrastructure manager. No heading suggests a metro-only price.
- RATP group financial report 2019. Segments are Transport, Engineering and Property, not metro vs RER vs bus.
- Cour des comptes report S2024-1197 on RATP's infrastructure management (October 2024). It gives costs for the infrastructure manager as a whole (operating charges of about €450-490 million a year, 2019-2022, about 3,000 staff; these figures come from a partial read and are not entered as rows), not by network. Its **Recommendation 1 asks RATP to "améliorer la connaissance des coûts d'exploitation, notamment par ligne et par actif"** (improve knowledge of operating costs, in particular by line and by asset). This strongly suggests that a metro-only cost does not exist in any published source.
- RATP's 2021 financial report could not be opened.

Conclusion: no published metro-only operating cost for Paris was found, and the national auditor says RATP does not track costs at that level. Paris stays without cost rows. Other public data for Paris (trips, train-km) remain useful for service comparisons.

## Comparability notes

- **Trips** are entries to the metro network as reported by RATP; changes between metro lines are not counted again.
- **Train-km** is the regulator's "km commerciaux". Paris trains are short (most lines run 5 or 6 cars; lines 3bis and 7bis run 3 or 4), so per-train costs are not comparable with NYC's 9-car trains without a car-km figure.
- **Stations** are counted per line (a station served by four lines counts four times).

## To find (low priority)

The financial annexes of the IDFM-RATP contracts, if a full copy can be uploaded by hand. They might give a per-mode service volume that would allow an allocation with a written method and a wide range.
