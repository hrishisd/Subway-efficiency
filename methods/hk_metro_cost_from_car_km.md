# Method: hk_metro_cost_from_car_km

**Used for:** `opex_total` of `hong_kong_mtr`, scope `metro_only`, 2016-2025 (obs_ids `hong_kong_mtr_<year>_opex_total_est`). **These rows are estimates.** Every ratio built on them (cost per car-km, per passenger-km, per trip, and their PPP versions) is an estimate too.

**Type:** estimated

## Why an estimate is needed

MTR reports one cost figure for all its Hong Kong transport operations: heavy rail, Airport Express, Light Rail, buses, intercity trains and the high-speed rail section. It does not publish the cost of the heavy-rail metro alone. It does publish, in its Ten-Year Statistics, "operating costs per car-km operated" for Hong Kong transport operations **excluding high-speed rail**, where the car-km are those of heavy rail, Airport Express and Light Rail.

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| c: operating cost per car-km, rail excluding high-speed rail (HK$, rounded to 0.1) | `hong_kong_mtr_<year>_opex_per_car_km_mtrrail` |
| K_h: car-km, Domestic and Cross-boundary | `hong_kong_mtr_<year>_car_km_mtr` |
| K_ae, K_lr: car-km, Airport Express and Light Rail | `hong_kong_mtr_<year>_car_km_mtrael`, `..._car_km_mtrlr` |

## Formula

Total rail cost C = c × (K_h + K_o), with K_o = K_ae + K_lr.
If Airport Express and Light Rail cost r times as much per car-km as heavy rail, heavy-rail cost per car-km is c_h = C / (K_h + r × K_o), and

opex_total (metro) = c_h × K_h

- Central value: r = 1 (all rail costs the same per car-km), so opex_total = c × K_h.
- value_low: r = 2. value_high: r = 0.5.

Airport Express and Light Rail are 9-10% of rail car-km in normal years (about 7% in 2021-2022), so the range is roughly −9% to +5% around the central value.

## Assumptions

- MTR's per-car-km figure and the P&L line "Expenses relating to Hong Kong transport operations" use the same cost definition: operating costs before depreciation, amortisation and the variable annual payment to KCRC. This matches the NTD definition (no depreciation).
- MTR's per-car-km numerator is smaller than the P&L total even before high-speed rail opened (about 89% of it in 2016-2017). The difference is costs MTR leaves out of its rail unit cost (probably buses and intercity trains); MTR does not say exactly which. This method follows MTR's own definition.
- Light Rail cars are small and Airport Express trains run fast with few stops, so their cost per car-km could differ from heavy rail in either direction. The 0.5x-2x range covers this.

## Range

See formula. The rounding of c to HK$0.1 adds less than 0.4%.

## Known weaknesses

- Shared costs (headquarters, IT, the operations control centre) sit inside c in MTR's own allocation. We cannot check how MTR allocates them between rail and its other businesses (property, station retail).
- MTR does not pay most of the infrastructure cost of its newer lines through operating expense, and pays a variable annual payment to KCRC for the East Rail and West Rail assets; both are outside operating cost here, as capital costs are out of scope.
