# Method: peer_unit_ratios

**Used for:** ratio metrics for non-US systems built by `scripts/build_peers.py` from the rows in `data/peers/<system_id>.csv`: `opex_per_car_km`, `opex_per_train_km`, `opex_per_passenger_km`, `opex_per_trip`, `farebox_recovery`, `avg_trip_length_km`, `avg_car_load`, `avg_cars_per_train`, `employees_per_million_car_km`, `passenger_km_per_employee`, `trips_per_employee`.

**Type:** derived (estimated when an input is an estimate)

## Inputs

The two rows named in `inputs`. Both belong to the same system, the same `year` and the same `scope`. The script makes a ratio only when exactly one row exists for each input metric in that system, year and scope.

## Formula

| Metric | Formula |
| --- | --- |
| opex_per_car_km | opex_total / car_km |
| opex_per_train_km | opex_total / train_km |
| opex_per_passenger_km | opex_total / passenger_km |
| opex_per_trip | opex_total / unlinked_trips |
| farebox_recovery | fare_revenue / opex_total |
| avg_trip_length_km | passenger_km / unlinked_trips |
| avg_car_load | passenger_km / car_km |
| avg_cars_per_train | car_km / train_km |
| employees_per_million_car_km | employees_fte / (car_km / 1,000,000) |
| passenger_km_per_employee | passenger_km / employees_fte |
| trips_per_employee | unlinked_trips / employees_fte |

These match the formulas in `ntd_unit_ratios` used for US systems, with one difference: US rows use `employees_operating` (NTD head count), and peer rows use `employees_fte` as the source publishes it. Each system's note says what its staff figure covers.

## Assumptions

None beyond the inputs. If any input is `estimated`, the ratio is `estimated` and its range is low = numerator_low / denominator_high and high = numerator_high / denominator_low (an input without a range counts as exact).

## Range

See above. Not an estimate when both inputs are reported or derived.

## Known weaknesses

The ratio is only as comparable as its inputs. Check `scope` and the per-system notes in `docs/peers/` before comparing systems. In particular, trips may be counted differently (station entries versus boardings including transfers), and car length differs between systems.
