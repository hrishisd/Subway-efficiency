# Method: seoul_car_km_from_train_km

**Used for:** `car_km` of `seoul_metro`, 2018, 2019 and 2024 (obs_ids `seoul_metro_<year>_car_km_est`). **Estimates.**

**Type:** estimated

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Train-km including empty running (열차주행키로, 회송포함) | `seoul_metro_<year>_train_km_smgross` |
| Cars and train sets in the fleet (전동차(편성)) | `seoul_metro_settlement_2019`, 사업보고서 2.가 업무량, p.16: 3,551 cars in 405 sets (2019); 3,570 in 423 (2018) |

## Formula

car_km = train-km × (cars ÷ train sets) × (1 − share of empty running)

Central: empty running 4%. Low: 7% empty running and cars per train 3% below the fleet average. High: 2% empty running and cars per train 2% above the fleet average.

## Assumptions

- Trains run with the fleet's average set length (8.4-8.8 cars). Seoul Metro lines use sets of 6, 8 or 10 cars (and 4 or 6 on the Line 2 branches); busy 10-car lines run more train-km, so the true average could be a little higher.
- Empty running (to and from depots) is a few percent of train-km, as on other metros.

## Range

As above, about −10% to +4%.

## Known weaknesses

Seoul Metro's annual statistics report (통계연보) probably gives car-km (차량주행거리) directly. Replace these rows when found.

## 2024

The 2024 row uses 2024 train-km (`seoul_metro_2024_train_km_mh`, from `seoul_mediahub_2025_ridership_2024`) with the 2019 average cars per train set, because the 2024 fleet is not in a readable source. The range is widened by a further −5% and +3%.
