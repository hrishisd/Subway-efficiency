# NYC subway baseline from the National Transit Database

Phase 2 output. All figures come from the National Transit Database (NTD), heavy-rail mode, and are rows in [`../data/observations.csv`](../data/observations.csv) with obs_ids ending in `_ntd`. How the rows were built: [`../scripts/build_ntd_baseline.py`](../scripts/build_ntd_baseline.py) and [`../data/raw/ntd/README.md`](../data/raw/ntd/README.md). Methods: [`../methods/`](../methods/) (`ntd_*`).

**No value on this page is an estimate.** Every value is either reported by NTD or derived from NTD values by plain arithmetic. Money is **nominal US dollars** of the NTD report year (each agency's fiscal year) unless marked as 2024 dollars. Constant-dollar rows (obs_ids ending `_real2024_ntd`) use the US CPI-U; see [`../methods/ntd_cpi_real_2024.md`](../methods/ntd_cpi_real_2024.md). All rows are `unverified` until a second person checks them.

## What the US data says (first read)

1. **Among US heavy-rail systems, NYC is not the expensive one per rider.** In 2019 NYC cost $0.31 per passenger-km and $1.92 per trip. Per passenger-km that was about the same as Boston and Philadelphia; only Chicago and BART were lower. Per trip, NYC and Boston were the two cheapest of the seven systems. The main reason is that NYC cars are full: about 30 passengers on board on average in 2019, against 15 to 25 for most peers (PATH, at about 34, is the exception).
2. **Per car-km, NYC is in the middle-to-high part of the US range.** $9.12 in 2019 and $11.58 in 2024, against $5 to $8 for Chicago, BART, Washington, Boston and Philadelphia in 2019. PATH, in the same city and labor market, is far more expensive per car-km ($21 in 2019).
3. **Labor productivity per rider is the best in the US set.** About 450,000 passenger-km per operating employee in 2024, against 200,000 to 340,000 for the peers. Per car-km, NYC staffing (about 49 employees per million car-km in 2024) is between Chicago and Washington (about 41 to 43) and Boston and Philadelphia (62 to 66). BART is lowest (30) and PATH highest (74).
4. **US peers alone are not enough of a benchmark.** Secondary figures in the scoping notes (not yet checked) suggest that US systems cost more per car-km than European ones. The real test of NYC is against London, Paris, Tokyo, Seoul, Hong Kong, Singapore and Madrid in phase 3.
5. **NYC cost per car-km rose 27% from 2019 to 2024 in nominal terms** ($9.12 to $11.58), **but only 3% after inflation** ($11.19 to $11.58 in 2024 dollars). Excluding general administration, real cost per car-km **fell** 9% ($9.79 to $8.93). About two thirds of the nominal rise is general administration, which went from $0.65 billion to $1.49 billion. The 2024 part of that jump is mostly claims reserves; the 2023 part is administration labor whose cause is not yet settled. See [`nyc_admin_cost_jump.md`](nyc_admin_cost_jump.md).

## Levy's $11.58 per car-km, recomputed

Alon Levy's figure of $11.58 per car-km for NYC (row `nyc_subway_2024_opex_per_car_km_levy`) is reproduced exactly from NTD report year 2024: $6,500,549,691 operating expense / (348,953,066 car revenue miles × 1.609344) = **$11.58 per car-km**. It is nominal US dollars, heavy-rail mode, and includes general administration allocated by MTA New York City Transit. Without general administration it is $8.93.

## Unit cost, 2019 (last year before the pandemic)

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Cost per car-km excl. admin | Farebox recovery | Avg trip (km) | Avg passengers per car |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NYC subway | $0.31 | $1.92 | $9.12 | $7.98 | 70% | 6.2 | 29.5 |
| PATH | $0.64 | $5.07 | $21.34 | $14.63 | 43% | 8.0 | 33.6 |
| Washington Metrorail | $0.53 | $4.86 | $8.12 | $5.43 | 48% | 9.2 | 15.4 |
| Boston (MBTA) | $0.33 | $1.90 | $8.20 | $7.15 | 74% | 5.7 | 24.8 |
| Philadelphia (SEPTA) | $0.31 | $2.21 | $7.29 | $6.48 | 56% | 7.1 | 23.4 |
| Chicago L | $0.28 | $2.85 | $5.27 | $4.69 | 50% | 10.2 | 18.7 |
| BART | $0.23 | $5.20 | $5.19 | $4.11 | 72% | 22.6 | 22.5 |

## Unit cost, 2024

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Cost per car-km excl. admin | Farebox recovery | Avg trip (km) | Avg passengers per car |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NYC subway | $0.52 | $2.95 | $11.58 | $8.93 | 44% | 5.7 | 22.3 |
| PATH | $1.22 | $9.58 | $29.70 | $19.63 | 25% | 7.8 | 24.3 |
| Washington Metrorail | $1.34 | $11.93 | $10.79 | $8.53 | 18% | 8.9 | 8.1 |
| Boston (MBTA) | $0.88 | $4.80 | $14.49 | $9.93 | 34% | 5.4 | 16.4 |
| Philadelphia (SEPTA) | $0.80 | $5.26 | $12.09 | $10.92 | 17% | 6.6 | 15.1 |
| Chicago L | $0.67 | $6.55 | $7.46 | $6.63 | 20% | 9.8 | 11.1 |
| BART | $0.71 | $16.00 | $7.36 | $5.42 | 25% | 22.4 | 10.3 |

## Unit cost, 2025 (latest NTD year)

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Cost per car-km excl. admin | Farebox recovery | Avg trip (km) | Avg passengers per car |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NYC subway | $0.51 | $2.88 | $11.59 | $9.17 | 45% | 5.6 | 22.7 |
| PATH | $1.35 | $10.12 | $31.33 | $21.16 | 27% | 7.5 | 23.2 |
| Washington Metrorail | $1.16 | $9.99 | $11.66 | $9.38 | 22% | 8.6 | 10.0 |
| Boston (MBTA) | $0.95 | $4.91 | $12.98 | $8.45 | 31% | 5.2 | 13.6 |
| Philadelphia (SEPTA) | $0.77 | $4.39 | $11.34 | $9.94 | 20% | 5.7 | 14.7 |
| Chicago L | $0.63 | $6.43 | $6.77 | $6.04 | 19% | 10.1 | 10.7 |
| BART | $0.69 | $15.65 | $8.12 | $5.94 | 27% | 22.6 | 11.7 |

## Staff and reliability, 2024

Operating employees are full-time plus part-time staff in vehicle operations, vehicle maintenance, facility maintenance and general administration. Capital-project staff are left out. Part-time staff count as one each. "Car-km per major failure" uses NTD major mechanical failures only.

| System | Operating employees | Employees per million car-km | Passenger-km per employee | Trips per employee | Car-km per major failure | Avg cars per train |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NYC subway | 27,587 | 49.1 | 455k | 80k | 317k | 9.1 |
| PATH | 1,490 | 73.9 | 328k | 42k | 272k | 7.7 |
| Washington Metrorail | 6,478 | 40.8 | 198k | 22k | 382k | 7.6 |
| Boston (MBTA) | 1,747 | 62.3 | 263k | 49k | 113k | 6.0 |
| Philadelphia (SEPTA) | 1,578 | 66.1 | 228k | 35k | 84k | 4.4 |
| Chicago L | 4,788 | 42.8 | 260k | 27k | 169k | 7.2 |
| BART | 3,474 | 30.0 | 343k | 15k | 680k | 7.2 |

## NYC subway, 2012 to 2025

2012 to 2014 come from single-year NTD agency profiles (no breakdown by function); 2015 onward from NTD TS2.1. The 2012 figure looks low against 2013 (operating expense $3.74B against $4.76B, with service almost unchanged). The cause is not known; treat 2012 as a possible series break.

| Year | Operating expense | of which admin | Cost per passenger-km | Cost per trip | Cost per car-km | Cost per car-km (2024 $) | Excl. admin (2024 $) | Farebox recovery |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2012 | $3.74B | – | $0.23 | $1.46 | $6.81 | $9.30 | – | 73% |
| 2013 | $4.76B | – | $0.27 | $1.79 | $8.58 | $11.55 | – | 64% |
| 2014 | $5.02B | – | $0.28 | $1.83 | $9.04 | $11.98 | – | 63% |
| 2015 | $5.20B | $0.85B | $0.30 | $1.95 | $9.36 | $12.38 | $10.37 | 64% |
| 2016 | $5.56B | $0.96B | $0.31 | $2.08 | $9.95 | $13.01 | $10.76 | 60% |
| 2017 | $4.79B | $0.54B | $0.28 | $1.77 | $8.51 | $10.89 | $9.67 | 73% |
| 2018 | $5.07B | $0.58B | $0.32 | $1.93 | $9.04 | $11.29 | $10.00 | 69% |
| 2019 | $5.21B | $0.65B | $0.31 | $1.92 | $9.12 | $11.19 | $9.79 | 70% |
| 2020 | $4.94B | $0.46B | $0.66 | $4.44 | $9.45 | $11.45 | $10.37 | 33% |
| 2021 | $5.03B | $0.59B | $0.55 | $3.83 | $9.43 | $10.92 | $9.64 | 35% |
| 2022 | $5.35B | $0.59B | $0.47 | $2.99 | $9.83 | $10.54 | $9.37 | 43% |
| 2023 | $6.05B | $1.01B | $0.47 | $3.00 | $10.93 | $11.25 | $9.37 | 45% |
| 2024 | $6.50B | $1.49B | $0.52 | $2.95 | $11.58 | $11.58 | $8.93 | 44% |
| 2025 | $6.68B | $1.40B | $0.51 | $2.88 | $11.59 | $11.30 | $8.93 | 45% |

## Definitions and caveats

- **Heavy-rail mode only.** MTA New York City Transit reports its subway as NTD mode `HR` and its buses separately. The subway figures include general administration that NYCT allocates to the subway. It has not yet been checked which MTA-wide costs (for example headquarters services or police) are inside NYCT's report. The Staten Island Railway is a separate NTD reporter and is not included.
- **Car-km, not train-km.** NTD counts each car. NYC runs long trains (about 9 cars on average), so it looks cheaper per car-km than it would per train-km.
- **Trips are boardings.** A transfer between lines counts as a new trip if the agency counts it that way. NYC's average trip length (about 6 km) is short partly for this reason.
- **Fiscal years differ.** NTD report year is each agency's own fiscal year.
- **Pandemic years** (2020 to 2022) distort every per-rider figure. Some peers also had big service cuts in single years (Washington 2021 to 2022, Boston 2023 to 2024).
- **Failures:** "other" mechanical failures are not comparable between agencies or years (NYC reported 18,806 in 2022 and 111 in 2025), so only major failures are used.

## Not yet done

- **2000 to 2011 for NYC, and 2000 to 2014 for the peers.** The portal copy of NTD TS2.1 starts in 2015, and the archive workbook for 1991 to 2014 could not be downloaded. NYC 2012 to 2014 were taken from NTD agency profiles instead. Profiles for 2000 to 2011 exist (for example "Thirty Largest Agencies, 2000 Report Year" at https://rosap.ntl.bts.gov/view/dot/370) but their NYC pages could not be read as text in this session.
- **Employees and failures before 2022.** In older yearly NTD tables.
- **Train hours.** Not in the NTD tables used here.
- **PPP adjustment** for international comparison (phase 3).
