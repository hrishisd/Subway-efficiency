# European peer systems (phase 3)

Per-city notes: [London](london_underground.md), [Madrid](madrid_metro.md), [Paris](paris_metro.md), [Berlin](berlin_ubahn.md), [Istanbul](istanbul_metro.md).

Asian peer systems (Tokyo Metro, Toei, Hong Kong MTR, Seoul Metro, Singapore SMRT, Beijing) are in [asia.md](asia.md).

Input rows live in `data/peers/<system_id>.csv`. `scripts/build_peers.py` adds ratio rows (method `peer_unit_ratios`) and 2024 PPP-dollar rows (method `ppp_usd_2024`) to `data/observations.csv`.

## Coverage

| System | Cost | Trips | Passenger-km | Car-km | Train-km | Staff | Years |
| --- | --- | --- | --- | --- | --- | --- | --- |
| London Underground | reported | yes | yes | **estimated** | yes | yes | 2015-2024 (cost 2017-2024) |
| Madrid Metro | **estimated** (2018, 2019, 2024) | yes | no | yes | no | 2018, 2024 | 2015-2024 |
| Paris Métro | none | 2018, 2019, 2024 | no | no | 2019, 2024 | no | |
| Berlin U-Bahn | 2017 cost per trip only | 2025 | 2024, 2025 | no | 2024, 2025 | no | |
| Istanbul (Metro İstanbul) | 2019, 2020, company-wide incl. tram | no | no | no | no | 2020 | |

## First read: 2019, in 2024 US dollars at PPP

NYC values are NTD values (nominal US dollars, rows `*_ntd`) restated in 2024 dollars here with the US GDP deflator (rows `*_real2024_ntd`, ×1.208 for 2019, ×1.026 for 2023), the same deflator that method `ppp_usd_2024` uses for the peers. **EST** marks values that depend on an estimate (range in brackets).

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Cost per train-km | Farebox recovery | Avg trip (km) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NYC subway | $0.37 | $2.32 | $11.02 | n/a | 70% | 6.2 |
| London Underground (2019/20) | $0.36 | $3.13 | $7.40 EST ($6.97-7.82) | $50.85 | 117% | 8.8 |
| Madrid Metro | n/a | $2.64 EST ($2.51-2.77) | $10.16 EST ($9.65-10.67) | n/a | n/a | n/a |

2023: NYC $0.48 per passenger-km, $3.07 per trip, $11.21 per car-km, about $102 per train-km (NTD 2023 cost / NTD train-km, restated). London (2023/24) $0.40, $3.60, $7.91 EST, $54.32. Staff per million car-km: NYC 48.6, London 30.0 EST (FTE, range 28.2-31.7).

What this suggests, to be tested in phase 4:

1. **Per passenger-km, London and NYC cost about the same.** NYC's cars carry many more people on average (29.5 against about 21 in London in 2019), which offsets a much higher cost per unit of service.
2. **Per unit of service, NYC is much more expensive.** About 50% more per car-km than London, and about twice as much per train-km (NYC trains are longer). Staff per car-km is about 60% higher in NYC.
3. **Per trip, NYC is cheaper than London**, because NYC trips are shorter (6.2 km against 8.8 km) and because the two count trips differently (see the London note).
4. **Madrid at PPP is close to NYC per car-km.** Spain's low price level raises Madrid's costs when converted at PPP; at market exchange rates Madrid would look much cheaper. The Madrid cost is an estimate from press releases.

## Open questions and gaps

- Paris: no metro-only cost exists in published sources (second search 2026-11-26; the Cour des comptes says RATP does not track cost by line). Berlin: only a 2017 cost per trip (€0.93, about $1.57 at 2024 PPP, against NYC's $2.32 in 2019). Istanbul: no ridership or service data found. See each note.
- Madrid: audited accounts, staff FTE and passenger-km.
- London: 2015/16 and 2016/17 cost; 2019/20 to 2021/22 staff; 2024/25 passenger-km and train-km.
- Several source sites block automated access (metro.istanbul, metromadrid.es, board.tfl.gov.uk, web.archive.org, older bvg.de files). A person with a normal browser can download the missing documents.
