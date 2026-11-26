# Method: ntd_miles_to_km

**Used for:** `car_km`, `passenger_km`, `directional_route_km`, `train_km` for every US system built from the National Transit Database (NTD).

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Miles value as published by NTD | The row named in `inputs` (`car_revenue_miles`, `passenger_miles`, `directional_route_miles` or `train_revenue_miles`) |

## Formula

km = miles × 1.609344

## Assumptions

None. 1.609344 km is the exact length of the international mile.

## Range

Not an estimate. No range.

## Known weaknesses

None from the conversion. Values over 100,000 are rounded to the nearest km.
