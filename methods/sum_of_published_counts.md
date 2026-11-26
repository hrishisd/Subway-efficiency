# Method: sum_of_published_counts

**Used for:** `singapore_mrt_2025_delays_over_30min` in `data/reliability.csv`.

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Monthly count of delays over 30 minutes, by line | `lta_rail_reliability_2025`, p. 8, Table 3 |

## Formula

Add the published monthly counts for all lines (NSL, EWL, NEL, CCL, DTL) for January to December 2025: March 1, April 1, August 2, September 2, November 1. Total 7.

## Assumptions

None beyond the table. The Thomson-East Coast Line is reported separately (Table 8, 3 delays) and is not included.

## Range

Not an estimate; no range.

## Known weaknesses

LTA says figures may be adjusted after incident investigations. The input counts are not stored as separate rows; the locator points to the table.
