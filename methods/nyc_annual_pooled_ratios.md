# Method: nyc_annual_pooled_ratios

**Used for:** `mdbf_car_miles`, `mdbf_car_km` and `terminal_otp` rows for `nyc_subway` in `data/reliability.csv`, 2015-2025.

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Car-miles and failures per year | `nyc_subway_<year>_car_miles_mdbf_basis`, `nyc_subway_<year>_failures_mdbf_basis` (source `nys_mta_subway_mdbf`, one Socrata query per year, URL in the locator) |
| On-time and scheduled trips per year | `nyc_subway_<year>_on_time_trips`, `nyc_subway_<year>_scheduled_trips` (source `nys_mta_subway_otp`) |

## Formula

- MDBF (miles) = sum of `total_miles` over all car classes and months of the year, divided by the sum of `number_of_failures` over the same rows. Rounded to whole miles.
- MDBF (km) = MDBF (miles) x 1.609344.
- Terminal OTP = sum of `num_on_time_trips` divided by sum of `num_sched_trips`, over all lines, both day types (weekday and weekend) and all months of the year.

The input sums were computed by the data.ny.gov API (`$select=sum(...)` with `$where=date_extract_y(month)=<year>`), not by us.

## Assumptions

- Pooling (total miles divided by total failures) is the right way to get one systemwide figure. The MTA publishes MDBF by car class, and a 12-month average per car class; it does not publish a systemwide figure in this dataset. Pooling weights each car class by the miles it ran.
- Every row in the dataset is subway revenue service. Staten Island Railway is a separate dataset and is not included.

## Range

Not an estimate; no range.

## Known weaknesses

- The MTA's own systemwide MDBF (for example in board books) may differ from this pooled value because of the 12-month averaging and data revisions.
- The MTA's definition of a countable failure (a mechanical problem that causes a delay) is not the same as Hong Kong MTR's (delay of 5 minutes or more) or Singapore's (delay over 5 minutes, per train-km). Compare across systems only with that caveat.
- Scheduled trips in the OTP dataset rise from about 2.0 million (2015) to 2.5 million (2019) and 2.75 million (2025). This may reflect changes in which trips are counted, not service growth. Before comparing years, check the MTA's notes on changes to the terminal OTP standard.
