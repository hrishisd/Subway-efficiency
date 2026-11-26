# Method: hk_metro_staff_share

**Used for:** `employees_fte` of `hong_kong_mtr`, scope `metro_only`, 2016-2025 (obs_ids `hong_kong_mtr_<year>_employees_fte_est`). **These rows are estimates**, and so are the staff ratios built on them.

**Type:** estimated

## Inputs

| Input | obs_id |
| --- | --- |
| Staff of Hong Kong transport operations (year end) | `hong_kong_mtr_<year>_employees_fte_mtrall` |
| Estimated metro operating cost (with its range) | `hong_kong_mtr_<year>_opex_total_est` |
| Expenses relating to Hong Kong transport operations | `hong_kong_mtr_<year>_opex_total_mtrall` |

## Formula

share = metro opex_total (central) / Hong Kong transport operations expenses
employees (metro) = Hong Kong transport operations staff × share

- value_low = staff × (metro opex low / total) × 0.85
- value_high = staff × (metro opex high / total) × 1.15, capped at the total staff

## Assumptions

- Staff are spread across services in proportion to operating cost. Buses and Light Rail are probably more labor-intensive per dollar than heavy rail (drivers per passenger), which would make the true metro share lower; high-speed rail uses mainland-style ticketing and immigration areas, which could go either way. The extra ±15% covers this.
- MTR's staff count is a head count at year end, not full-time equivalents. It excludes corporate support, station commercial, capital project and property staff, but includes transport operations staff of all services.

## Range

See formula.

## Known weaknesses

MTR outsources some cleaning, security and maintenance work. Contractors are not in the staff count, so staff per car-km understates total labor, as it does for other systems that contract out.
