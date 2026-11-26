# Method: ntd_operating_staff

**Used for:** `employees_operating`, `employee_hours_operating`, `employees_vehicle_operations`, `employees_vehicle_maintenance`, `employees_facility_maintenance`, `employees_general_administration` for US heavy-rail systems, report years 2022 to 2025.

**Type:** derived

## Inputs

The reported NTD Employees rows listed in `inputs`: `employee_count_<function>_ft`, `employee_count_<function>_pt` (and the `employee_hours_...` rows for hours), from source `ntd_employees_by_mode`.

## Formula

- employees in a function = full-time count + part-time count for that function.
- employees_operating = sum over the four operating functions (vehicle operations, vehicle maintenance, facility maintenance, general administration).
- employee_hours_operating = same sum, using work hours.

**Capital labor is left out**, because it is staff working on capital projects, and capital costs are out of scope. The capital labor rows are kept in the dataset as reported rows (`employee_count_capital_labor_ft`, and so on).

## Assumptions

- A part-time employee counts as one employee. Part-time staff are a small share for most systems, but not for the Chicago L (about 460 to 680 part-time vehicle-operations staff a year in 2022 to 2025, against about 1,700 to 1,900 full-time). For a like-for-like labor measure use `employee_hours_operating`, which does not depend on this choice.
- Blank NTD cells are treated as zero.

## Range

Not an estimate. No range.

## Known weaknesses

- NTD employee counts are as each agency reports them. Some agencies report fractional counts (for example WMATA and BART), which suggests full-time equivalents rather than headcount. The NTD definition has not yet been checked in the NTD Policy Manual.
- Contractors are not in these counts. An agency that contracts out maintenance shows fewer employees and higher purchased services. Compare costs first, staff second (see `docs/scoping.md`).
- NTD employee data by mode is only in this dataset for 2022 to 2025. Earlier years need the older annual NTD Employees tables (open question).
