# Method: hk_metro_derived

**Used for:** `hong_kong_mtr` rows with scope `metro_only`: `unlinked_trips` and `passenger_km` (obs_ids `hong_kong_mtr_<year>_unlinked_trips_mtr` and `..._passenger_km_mtr`), 2016-2025.

**Type:** derived

## Inputs

All from MTR's Ten-Year Statistics in the 2025 annual report (source `mtr_ar2025_ten_year_stats`): Domestic Service passengers, Cross-boundary Service passengers, and average passenger km travelled on Domestic and Cross-boundary services.

## Formula

- unlinked_trips = Domestic Service passengers + Cross-boundary Service passengers
- passenger_km = unlinked_trips × average passenger km travelled (Domestic and Cross-boundary)

## Assumptions

- "Metro" here means MTR's heavy-rail urban lines (the Domestic Service, including East Rail, Tuen Ma and Tung Chung lines) plus Cross-boundary trips to Lo Wu and Lok Ma Chau, which run on the same East Rail trains and tracks. MTR publishes their car-km only as one combined figure, so the two cannot be split.
- Airport Express, Light Rail, buses, intercity trains and high-speed rail are left out.
- MTR counts a passenger once per journey inside its network, so transfers between MTR lines are not extra trips (unlike NTD boardings).

## Range

Not an estimate. The source rounds trip length to 0.1 km, so passenger-km has up to about 0.5% rounding error.

## Known weaknesses

Cross-boundary trips are long (to the border) and fell to almost nothing in 2020-2022, which moves the average trip length.
