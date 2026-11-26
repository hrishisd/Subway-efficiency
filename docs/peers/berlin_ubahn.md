# Berlin U-Bahn: sources and comparability

Rows: `data/peers/berlin_ubahn.csv`. Calendar years. **Berlin data is thin. The only cost figure is one reported cost per trip for 2017.**

## What the data is

| Item | Source | Years |
| --- | --- | --- |
| Passenger-km, train-km | BVG management report 2025, p.23 | 2024, 2025 |
| Trips (mode-level) | BVG in Zahlen 2025 | 2025 |
| Line length, stations, fleet | BVG in Zahlen 2025 | 2025 |
| Cost per trip | Berlin Senate answer to written question 18/15985, Frage 14 | 2017 |

## Cost: one figure only

The Senate's answer to written question 18/15985 (August 2018) says: "Die durchschnittlichen Kosten des Bereiches U-Bahn je Fahrgastfahrt lagen in 2017 bei 0,93 EUR inklusive der Kosten der zurechenbaren Verkehrsinfrastruktur". That is **€0.93 per U-Bahn trip in 2017, including attributable infrastructure cost**, or about **$1.57 per trip in 2024 dollars at PPP** (row `berlin_ubahn_2017_opex_per_trip_abghs`, scope `metro_with_allocated_infrastructure`). For scale, NYC's 2019 figure is $2.32 per trip in 2024 dollars. Cautions: the answer does not give the total cost, the trip count used, or whether BVG-wide overhead is included. BVG counts trips by mode, so a trip that uses U-Bahn and bus counts once for each. No 2017 U-Bahn trip count or car-km is in the repository, so no cost per car-km or per passenger-km can be derived.

## Why there is no other cost

BVG runs the U-Bahn, trams and buses as one company and publishes one income statement. No U-Bahn cost, cost per km or U-Bahn share of the Berlin transport contract was found in the documents that could be reached. BVG's earlier annual reports (2015 to 2024) redirect to a generic page or return "not found" for automated access. An allocation by passenger-km or vehicle-km would be possible, but a bus-km and a U-Bahn car-km have very different costs, so the range would be too wide to be useful. This is left as an open question.

**Second search (2026-11-26).** Seventeen Abgeordnetenhaus documents were read: written questions on U-Bahn costs, extensions, workshops, reliability and ridership (19/25247, 19/18171, 19/24351, 19/20647, 19/24551, 19/11503, 19/24249, 19/22518, 19/18145, 19/22371, 19/21177, 19/25233, 18/15985, 18/13890, 18/21233, 17/15456) and the main committee's report on the first revision of the BVG transport contract (Vorgang 19/1828 A). Only 18/15985 has a U-Bahn operating-cost figure (above). Other findings:
- The transport contract payment is one budget line for all modes (Kapitel 0730, Titel 540 45, "Leistungen des innerstädtischen ÖPNV": about €779 million actual in 2024). It is not split by mode.
- 19/25247 gives a subsidy need of about €0.158 per passenger-km for all BVG services in 2024 (subsidy, not cost, and not U-Bahn alone). It confirms the 2024 U-Bahn passenger-km (2,529 million) and train-km (20.7 million) already in the rows.
- 18/13890 says BVG has no cost breakdown for third-rail maintenance per km, and 18/21233 says BVG could not answer a question on U-Bahn maintenance cost in time.
- BVG's own Verkehrsvertrag text was not found in a readable form.

No further search is planned. A full Berlin cost series would need BVG's internal mode accounts.

## Partial staff figures (not entered as rows)

The Berlin Senate's answer to written question 19/21316 (January 2025) gives U-Bahn train-driving staff of 776 full-time equivalents and U-Bahn workshop staff of 355 at 31 December 2024. These are only two groups, not total U-Bahn staff, so they are not comparable with total staff for other systems.

## Comparability notes

- **Trips** are BVG's mode-level count (BBF): one trip per mode used, so a change between two U-Bahn lines is one U-Bahn trip.
- **Train-km** is Nutzzugkilometer (revenue train-km). Car-km is not published; trains run with 4, 6 or 8 cars depending on line and time of day.
- Small-profile lines (U1 to U4) have narrow 2.3 m cars; large-profile lines (U5 to U9) have 2.65 m cars. Both are narrower than NYC cars.
