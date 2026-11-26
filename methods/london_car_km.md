# Method: london_car_km

**Used for:** `car_km` for `london_underground`, every year. **This is an ESTIMATE.** TfL does not publish London Underground car-km; it publishes operated train-km.

**Type:** estimated

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Operated train-km | `london_underground_<year>_train_km_til` (Travel in London 2024, Table 9) |
| Cars per train, by stock, and fleet size | `tfl_rs_info_sheets_4th`, the sheet for each passenger stock |

## Formula

car_km = train_km × cars per train, with cars per train = 6.87 (central), 6.5 (low), 7.3 (high).

The central value is the fleet-wide ratio of cars to trains in the rolling stock information sheets: 4,769 cars / 694.5 trains = 6.87. (1972 stock 252/36, 1973 stock 519/86.5, 1992 stock Central line 680/85 and Waterloo & City 20/5, 1995 stock 636/106, 1996 stock 441/63, 2009 stock 376/47, D78 stock 450/75, S7 stock 931/133, S8 stock 464/58.)

## Assumptions

1. **Trains run with their full formation.** LU does not run part-length trains in normal service.
2. **Train-km by line is proportional to the number of trains in each fleet.** Not checked: no train-km by line is published. Lines with 8-car trains (Central, Victoria, Metropolitan) and 6-car trains (Piccadilly, Northern) both run very frequent services.
3. **Fleet mix.** The information sheets predate the replacement of the 6-car D78 stock on the District line by 7-car S7 stock (completed in 2017). With that change the ratio rises to roughly 7.0.

## Range

Low 6.5 and high 7.3 cover a train-km weighting that leans toward the 6-car lines (Piccadilly, Northern, District before 2017) or toward the 8-car lines (Central, Victoria, Metropolitan), and the fleet change in assumption 3. That is about −5% to +6% around the central value.

## Known weaknesses

- LU cars are shorter and narrower than NYC cars (about 16 to 18 m on deep tube stock against 18 m or 23 m in New York), so cost per car-km is not a like-for-like measure of capacity. Compare per train-km and per passenger-km as well.
- Alon Levy's figure (row `london_underground_2024_opex_per_car_km_levy`) assumed 7 cars per train, inside this range.
