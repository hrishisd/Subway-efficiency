# Method: tokyo_passenger_km_from_trip_length

**Used for:** `passenger_km` of `tokyo_metro` and `tokyo_toei` for FY2019 to FY2023 (obs_ids `*_passenger_km_est`). **These rows are estimates.**

**Type:** estimated

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Passengers carried in the year (輸送人員) | `<system>_<year>_unlinked_trips_mlit` |
| Passenger-km published for FY2015-FY2018 (輸送人キロ) | `<system>_2015..2018_passenger_km_mlit` |
| Passengers FY2015-FY2018 | `<system>_2015..2018_unlinked_trips_mlit` |

## Formula

passenger_km(year) = trips(year) × mean over FY2015-FY2018 of (passenger_km / trips)

Mean trip length: Tokyo Metro 8.03 km (range of yearly values 8.01-8.04 km); Toei 6.97 km (6.95-6.98 km).

## Assumptions

- The average trip length on each network stayed at its FY2015-FY2018 level. The yardstick table stopped printing 輸送人キロ for subway operators from FY2019. The full passenger-km table (鉄道統計年報 table (2)) exists for every year but is published only as Excel, which this project could not open.
- The networks did not change in this period (Tokyo Metro 195 km, Toei 109 km), so trip length should be stable outside the pandemic.

## Range

- value_low = trips × (lowest FY2015-FY2018 trip length) × (1 − w)
- value_high = trips × (highest FY2015-FY2018 trip length) × (1 + w)
- w = 5% for FY2019 and FY2023, 10% for FY2020-FY2022, because the pandemic changed who travelled (fewer commuters, who make longer trips).

## Known weaknesses

Replace these rows with the published 輸送人キロ from 鉄道統計年報 table (2), 運輸成績表（延日キロ、人キロ、平均数）, when someone can read the Excel files (for example FY2023: https://www.mlit.go.jp/tetudo/content/001977414.xlsx).
