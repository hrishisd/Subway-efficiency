# Method: ntd_mdbf_major

**Used for:** `mdbf` (mean distance between failures) for US heavy-rail systems, report years 2022 to 2025.

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Car revenue km | `<system>_<year>_car_km_ntd` (from NTD TS2.1 vehicle revenue miles) |
| Major mechanical failures | `<system>_<year>_major_mechanical_failures_ntd` (NTD Breakdowns table) |

## Formula

mdbf = car_km / major_mechanical_failures

## Assumptions

- Only **major** mechanical failures are used. "Other" mechanical failures are left out because agencies report them very differently. For example, NYC reported 18,806 other failures in 2022 and 111 in 2025, while the Chicago L reports about 9,000 a year. Those swings look like changes in reporting practice, not in fleet condition.
- Revenue car-km is used as the distance, not total car-km (which includes deadhead).

## Range

Not an estimate. No range.

## Known weaknesses

- The NTD definition of a major failure is applied by each agency. Agency practice may differ, so cross-system comparison is weak. Within-system trends are more reliable.
- Agency performance reports (for example the MTA's own mean distance between failures) use different definitions and will not match this number.
