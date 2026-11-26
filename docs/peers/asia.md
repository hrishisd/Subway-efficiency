# Asian peer metros: Tokyo, Hong Kong, Seoul, Singapore, Beijing, Shanghai

Phase 3 output for the Asian peers. Rows are in [`../../data/observations.csv`](../../data/observations.csv). They are built from the per-system files in [`../../data/peers/`](../../data/peers/) by `scripts/build_tokyo_inputs.py`, `scripts/build_hk_inputs.py`, `scripts/build_seoul_singapore_inputs.py` and then `scripts/build_peers.py`. Transcriptions of the source tables are in [`../../data/raw/asia/`](../../data/raw/asia/).

**Read this first.** Money in the tables below is in **2024 US dollars at purchasing power parity** (method [`ppp_usd_2024`](../../methods/ppp_usd_2024.md)). Values in **bold with "(est.)"** are estimates: they rest on an assumption that is not in any source, and each has a method note and a low-high range in the data. All rows are `unverified` until a second agent checks them against the source.

## Main findings (first read)

1. **The Asian metros cost about the same as NYC per car-km, but far less per passenger.** In 2019, Tokyo Metro spent $9.42 per car-km and Toei $8.36, against $11.02 for NYC (NYC's NTD figure of $9.12, restated in 2024 dollars with the same US deflator). Hong Kong's heavy rail was lower, about $6.44 (estimate). So NYC is 15-70% more expensive per unit of service, not several times more.
2. **Per passenger-km and per trip the gap is large: 3 to 4 times.** NYC cost $0.37 per passenger-km and $2.32 per trip in 2019 (2024 dollars). Tokyo Metro, Toei and Hong Kong cost $0.11-0.14 per passenger-km (estimates) and about $1.00-1.16 per trip. Seoul cost about $1.12 per trip (estimate).
3. **The main reason is full trains, not cheap trains.** An average car carried 59-76 passengers in Tokyo and Hong Kong in 2019, against 30 in NYC. Car sizes differ between systems, so per-car figures still need a check against per-train-km or per-seat figures (phase 4).
4. **Staffing per car-km is lower in Tokyo and Hong Kong, but Seoul is like NYC.** Tokyo Metro had 36-37 staff per million car-km, Toei 28 and Hong Kong about 29 (estimate), against 49 in NYC (2023). Seoul Metro had about 50 (estimate; its count includes every employee of the corporation). Passenger-km per employee is about 4 times NYC's in Tokyo and Hong Kong.
5. **These metros cover their operating costs from fares.** Tokyo Metro and Toei recovered 145-170% of operating cost (excluding depreciation) from fares before the pandemic, and MTR's whole Hong Kong transport business 140-150%. Seoul recovered about 78% (estimate), held down by free rides for seniors. NYC recovered 70% in 2019 and 45% in 2023.

## Unit cost, 2018

#### 2018

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Farebox recovery | Avg trip (km) | Avg passengers per car | Staff per million car-km | Passenger-km per staff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tokyo Metro | $0.12 | $0.97 | $9.23 | 153% | 8.0 | 76.3 | – | – |
| Toei Subway | $0.14 | $0.96 | $8.07 | 171% | 7.0 | 58.8 | 28.5 | 2,064k |
| Hong Kong MTR heavy rail | **$0.09 (est.)** | **$0.96 (est.)** | **$5.54 (est.)** | – | 10.8 | 62.5 | **29.8 (est.)** | **2,100k (est.)** |
| Seoul Metro lines 1-8 | – | **$1.13 (est.)** | **$9.00 (est.)** | **78% (est.)** | – | – | **51.0 (est.)** | – |

## Unit cost, 2019 (last year before the pandemic)

#### 2019

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Farebox recovery | Avg trip (km) | Avg passengers per car | Staff per million car-km | Passenger-km per staff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tokyo Metro | **$0.12 (est.)** | $1.00 | $9.42 | 147% | **8.0 (est.)** | **75.8 (est.)** | 37.2 | **2,039k (est.)** |
| Toei Subway | **$0.14 (est.)** | $1.00 | $8.36 | 163% | **7.0 (est.)** | **58.5 (est.)** | 28.0 | **2,086k (est.)** |
| Hong Kong MTR heavy rail | **$0.11 (est.)** | **$1.16 (est.)** | **$6.44 (est.)** | – | 10.6 | 58.8 | **28.7 (est.)** | **2,047k (est.)** |
| Seoul Metro lines 1-8 | – | **$1.12 (est.)** | **$8.84 (est.)** | **78% (est.)** | – | – | **50.0 (est.)** | – |

## Unit cost, 2023

#### 2023

| System | Cost per passenger-km | Cost per trip | Cost per car-km | Farebox recovery | Avg trip (km) | Avg passengers per car | Staff per million car-km | Passenger-km per staff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tokyo Metro | **$0.13 (est.)** | $1.01 | $8.34 | 147% | **8.0 (est.)** | **66.0 (est.)** | 36.0 | **1,833k (est.)** |
| Toei Subway | **$0.15 (est.)** | $1.07 | $7.72 | 145% | **7.0 (est.)** | **50.1 (est.)** | 28.3 | **1,768k (est.)** |
| Hong Kong MTR heavy rail | **$0.10 (est.)** | **$1.12 (est.)** | **$6.36 (est.)** | – | 11.1 | 63.2 | **28.4 (est.)** | **2,227k (est.)** |
| Singapore SMRT Trains | **$0.14 (est.)** | **$1.57 (est.)** | **$7.13 (est.)** | – | 10.8 | 49.2 | – | – |

NYC for comparison, in 2024 US dollars (NTD values from `docs/ntd_baseline.md` times the US GDP deflator ratio, 1.2078 for 2019 and 1.0256 for 2023; rows `*_real2024_ntd`): 2019 cost per passenger-km $0.37, per trip $2.32, per car-km $11.02, farebox recovery 70%, average trip 6.2 km, 29.5 passengers per car. 2023: $0.48, $3.07, $11.21, 45%, 6.4 km, 23.3 passengers per car, 48.6 staff per million car-km, 479,000 passenger-km per employee. These match the `*_real2024_ntd` rows, which use the same deflator factors as the PPP rows (`data/raw/ppp/ppp_deflator.csv`).

Staff counts are head counts (not full-time equivalents) at the end of the year, except where the notes say otherwise. NYC's staff figure is the NTD count of operating employees.

## Per-system notes on comparability

### Tokyo Metro (`tokyo_metro`) and Toei Subway (`tokyo_toei`)

- **Source:** Japan's national railway statistics (鉄道統計年報, MLIT), the yardstick cost table for subway operators, FY2015 to FY2023. One uniform government table covers both operators. Cost covers the **railway business only** (Tokyo Metro's real estate and retail are outside it). The transcription is checked against three printed sum identities in `scripts/build_tokyo_inputs.py`. Toei's FY2018-FY2019 cost matches the Tokyo audit committee's figures to the thousand yen.
- **Cost definition:** operating expense minus depreciation (method [`mlit_opex_excl_depreciation`](../../methods/mlit_opex_excl_depreciation.md)). Includes taxes (Tokyo Metro pays ¥10-14 billion a year; Toei almost none) and general administration.
- **Fiscal year** April to March; `year` is the starting year.
- **Trips** are passengers carried by that operator (輸送人員). A transfer between two lines of the same operator is not counted twice. A trip that continues onto the other operator, or onto a through-running private railway, is counted by each. So Tokyo Metro plus Toei double-counts some trips, and per-trip costs are slightly low relative to NTD boardings, which count every boarding.
- **Passenger-km** are published for FY2015-FY2018 only. **FY2019 onward are estimates** from trips times the FY2015-FY2018 average trip length (method [`tokyo_passenger_km_from_trip_length`](../../methods/tokyo_passenger_km_from_trip_length.md)). Use 2018 for fully reported per-passenger-km figures.
- **Car-km** include other companies' trains that run through onto Tokyo Metro and Toei tracks. The operators settle through-running by car-use fees (車両使用料), which appear in revenue and cost.
- **Staff:** Tokyo Metro uses the group transport segment head count from its securities reports (company plus transport subsidiaries; FY2018 missing). The company's own transport staff (about 9,400-9,800) are also given as `employees_headcount_parent`. Toei uses the subway business head count from the Tokyo audit committee's opinions (FY2017-FY2023). Both exclude outside contractors.
- **Subsidy:** Toei receives ¥2.7-6.1 billion a year from the Tokyo government in its operating account, mostly to repay special subway bonds and to pay public pension contributions (`operating_subsidy`). Tokyo Metro receives no operating subsidy.

### Hong Kong MTR (`hong_kong_mtr`)

Three scopes are kept apart:

- `hk_transport_operations_all` (reported): MTR's whole Hong Kong transport business, 2016-2025, from the profit and loss account: expenses (before depreciation and payments to KCRC), staff costs, revenue and staff. It includes buses, Light Rail, Airport Express, intercity trains and, from September 2018, the high-speed rail link. The jump in expenses from 2018 to 2019 is mostly the high-speed rail's first full year.
- `hk_rail_excl_hsr_mtr_definition` (reported): MTR's own published operating cost per car-km and per passenger for its Hong Kong rail network excluding high-speed rail.
- `metro_only`: the Domestic heavy-rail lines plus Cross-boundary trips on East Rail. Car-km, passengers and average trip length are reported. **Cost and staff are estimates** (methods [`hk_metro_cost_from_car_km`](../../methods/hk_metro_cost_from_car_km.md), [`hk_metro_staff_share`](../../methods/hk_metro_staff_share.md)). The cost range is about -9% to +5%; staff about -23% to +21%.
- MTR counts a passenger once per journey inside its network. Depreciation and MTR's variable annual payment to KCRC (for the former KCR network) are outside operating cost here, as for the other systems.
- **2015 is missing** (no ten-year table in reach covers it).

### Seoul Metro (`seoul_metro`)

- **Source:** Seoul Metro's 2019 draft financial statements and business report, submitted to the Seoul city council (calendar 2019 and 2018). Later years exist only as Excel files on Seoul Metro's site, which this project could not read.
- **Cost is an estimate:** operating expense minus contract work for others minus depreciation, and depreciation is not in the readable part of the source (method [`seoul_opex_excl_depreciation`](../../methods/seoul_opex_excl_depreciation.md); range about ±3.5%).
- **Car-km is an estimate** from train-km (which include empty running) times average train length (method [`seoul_car_km_from_train_km`](../../methods/seoul_car_km_from_train_km.md)).
- **No passenger-km** source was found, so there is no cost per passenger-km for Seoul.
- **Trips** count entries plus transfers in from other operators' lines (승차인원+환승인원), close to NTD's boardings. Trips on through-running commuter services count only on Seoul Metro's own sections.
- **Staff** (about 16,900) is the whole corporation's head count, including some staff on contract work and side businesses.
- **Fares:** 14.9% of riders travelled free in 2018, mostly seniors (source `newdaily_2019_seoul_metro`, secondary). Seoul Metro reports that it gets no compensation for this (source `mt_2026_seoul_metro_loss`, secondary), which holds farebox recovery down.

### Singapore (`singapore_mrt`)

- **Only SMRT Trains** (North-South, East-West and Circle lines, plus Thomson-East Coast from FY2023/24). SBS Transit reports bus and rail together, so the North East and Downtown lines are not covered.
- **Cost is an estimate** from revenue minus EBIT (method [`smrt_opex_from_revenue_ebit`](../../methods/smrt_opex_from_revenue_ebit.md); range -20% to +10%, +25% for FY2023/24). SMRT Corporation is private and publishes no cost breakdown.
- Car-km, ridership and passenger-km are reported (rounded to the nearest million). No staff numbers, so no productivity ratios. Years FY2021/22 to FY2023/24 only; the first is pandemic-affected.
- Under the New Rail Financing Framework the government (LTA) owns trains and infrastructure; the operator pays licence charges. The government pays "more than $2 billion annually" in operating subsidies to bus and rail together (source `ptc_fmmr_2023`, p.2).

### Beijing (`beijing_subway`)

- Only **cost per trip**, 2019 (¥7.82) and 2022 (¥14.32), from a news report of the operators' own cost disclosures (secondary source, unverified). The cost definition and the trip counting rule are not stated. Treat as indicative.
- Beijing's subway depends heavily on city subsidy: the city's infrastructure investment company (京投) booked ¥26.3 billion of operating-related government grants in 2022 against ¥4.6 billion of fare revenue (same news report, citing 京投's 2022 accounts; not entered as rows because the scope is the whole company).

### Shanghai (`shanghai_metro`)

- **No usable data found.** Shanghai Shentong Metro Co. (the listed company) runs only a small part of the network. The parent Shanghai Shentong Metro Group publishes financial statements through the Shanghai Clearing House for its bonds, but this project could not reach them. Not compiled.

## What could not be found (open questions)

- Tokyo: passenger-km for FY2019-FY2023 (in MLIT table (2), Excel only); Tokyo Metro staff for FY2018; FY2024 MLIT data (not yet published).
- Hong Kong: 2015; the cost of the heavy-rail lines alone; heavy-rail fare revenue by year in a readable form.
- Seoul: depreciation, car-km and passenger-km; all years after 2019 in a primary source. Seoul Metro publishes statements for 2017-2025 as Excel files at http://www.seoulmetro.co.kr/kr/page.do?menuIdx=110.
- Singapore: any cost breakdown or staff numbers; SBS Transit rail on its own.
- Shanghai and Beijing: primary operator cost data (bond-issuer financial statements on the Shanghai Clearing House site).
- The common blocker: this environment cannot open Excel files from the web, and several sites block automated access.
