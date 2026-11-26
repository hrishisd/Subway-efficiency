# Method: ntd_unit_ratios

**Used for:** all ratio metrics built from the National Transit Database (NTD) for US heavy-rail systems: `opex_per_car_km`, `opex_excl_ga_per_car_km`, `opex_per_car_hour`, `opex_per_passenger_km`, `opex_per_trip`, `farebox_recovery`, `avg_trip_length_km`, `avg_car_load`, `avg_cars_per_train`, `employees_per_million_car_km`, `passenger_km_per_employee`, `trips_per_employee`, `opex_per_employee_hour`.

**Type:** derived

## Inputs

Each row lists its input `obs_id`s in `inputs`. All inputs are the same system, the same NTD report year, and the heavy-rail mode (`HR`), directly operated (`DO`).

## Formula

| Metric | Formula |
| --- | --- |
| opex_per_car_km | opex_total / car_km |
| opex_excl_ga_per_car_km | (opex_total − opex_general_administration) / car_km |
| opex_per_car_hour | opex_total / car_revenue_hours |
| opex_per_passenger_km | opex_total / passenger_km |
| opex_per_trip | opex_total / unlinked_trips |
| farebox_recovery | fare_revenue / opex_total |
| avg_trip_length_km | passenger_km / unlinked_trips |
| avg_car_load | passenger_km / car_km |
| avg_cars_per_train | car_km / train_km |
| employees_per_million_car_km | employees_operating / (car_km / 1,000,000) |
| passenger_km_per_employee | passenger_km / employees_operating |
| trips_per_employee | unlinked_trips / employees_operating |
| opex_per_employee_hour | opex_total / employee_hours_operating |

## Assumptions

No assumption beyond the NTD definitions. Points to keep in mind when reading the numbers:

- **Money is nominal US dollars** of each report year. No inflation or PPP adjustment yet.
- **Report year is the agency's fiscal year.** Fiscal years differ between agencies. Check each agency's fiscal year before comparing single years closely.
- **Car-km, not train-km.** NTD "vehicle revenue miles" for rail count each car. Systems with long trains (NYC averages about 9 cars) look cheaper per car-km than per train-km.
- **Unlinked trips count each boarding.** A transfer between lines inside fare control may or may not count as a new boarding, depending on how each agency estimates ridership. This affects `opex_per_trip` and `avg_trip_length_km`.
- **Car revenue hours are car hours, not train hours.** `opex_per_car_hour` is per car.
- `opex_per_employee_hour` divides **all** operating expense (labor, materials, power, services and so on) by operating labor hours. It is not a wage rate.

## Range

Not an estimate. No range.

## Known weaknesses

- **Overhead allocation:** NTD mode-level expense includes general administration that the reporting agency allocates to the mode by its own formula. For NYC the reporter is MTA New York City Transit, which also runs buses; this repository has not checked which MTA-wide costs (for example MTA headquarters services or police) are or are not inside NYCT's report. `opex_excl_ga_per_car_km` is given so results can be read with and without overhead.
- **NYC general administration more than doubled after 2022** (from about $0.59 billion in 2022 to $1.49 billion in 2024, rows `nyc_subway_*_opex_general_administration_ntd`). The cause is not yet known (it could be an accounting or allocation change rather than real cost growth). Until explained, compare NYC across years with `opex_excl_ga_per_car_km` as well.
- **Pandemic years** 2020 to 2022 distort every per-trip and per-passenger-km figure. Use 2019 or 2024 onward.
- **Service changes** distort single years for some peers (for example MBTA car-km fell in 2023 and 2024, and WMATA car-km fell in 2021 and 2022). Read single-year peer values with care.
