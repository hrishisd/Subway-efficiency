# Method: staff_cost_per_employee

**Used for:** `staff_cost_per_employee`, `staff_wages_per_employee`, `staff_benefits_per_employee` and `staff_cost_share_of_opex` rows for NYC (NTD, 2022 onward), Tokyo Metro and Toei (FY2023) and Hong Kong MTR (all years with staff costs).

**Type:** derived (NYC, Tokyo, Toei); estimated (Tokyo Metro benefits per employee; Hong Kong).

## Inputs

| System | Staff cost | Employees |
| --- | --- | --- |
| NYC subway | `opex_staff_costs` = wages, salaries and paid absences (`opex_staff_wages`) plus fringe benefits, NTD object classes (`ntd_opex_by_type`) | `employees_operating` (NTD operating head count, full- and part-time) |
| Tokyo Metro | `opex_staff_costs` = sum of the 人件費 (personnel cost) column of MLIT's yardstick table, railway business (`mlit_yardstick_fy2023`) | `employees_headcount_parent` (Tokyo Metro Co. itself, transport segment, year end) |
| Toei | same as Tokyo Metro, Toei column | `employees_fte` (Toei subway business head count, year end) |
| Hong Kong MTR | `opex_staff_costs` ("Staff costs and related expenses", Hong Kong transport operations) | `employees_fte` (Hong Kong transport operations head count) |

Tokyo Metro wages: `staff_wages_per_employee` = 平均年間給与 (average annual salary) from the securities report.

## Formula

- staff cost per employee = staff cost ÷ employees.
- NYC wages per employee = wages, salaries and paid absences ÷ employees; benefits per employee = fringe benefits ÷ employees.
- Tokyo Metro benefits per employee (ESTIMATE) = staff cost per employee − average salary.
- staff cost share = staff cost ÷ operating expense (same scope).
- Money is converted to 2024 dollars by the usual methods (`ntd_gdp_deflator_real_2024` for NYC, `ppp_usd_2024` for others).

## Assumptions

- Staff cost covers only the operator's own employees. Work contracted out (for example Tokyo Metro's maintenance subsidiaries) is in non-labour cost, so it is not in these figures for any system.
- NYC fringe benefits include pensions, active and retiree health care and payroll taxes as the MTA books them (accrual basis, GASB 68 and 75, per `nycta_fs_2023`).
- Tokyo's 人件費 is assumed to include salaries, bonuses, retirement-benefit cost and statutory welfare (social insurance). No document defining the term was opened.
- Tokyo Metro railway staff are assumed to earn the company-wide average salary (the salary covers all 9,551 parent employees in FY2023; railway staff are 9,431 of them).
- Hong Kong: staff costs may include corporate-support staff that the head count excludes.

## Range

- Tokyo Metro benefits per employee: low uses all parent employees (9,551) as the denominator of personnel cost; high is the mirror image around the central value.
- Hong Kong: high = the computed value (all staff cost belongs to counted staff); low = 85% of it (up to 15% of staff cost for uncounted staff). The 15% is an assumption, not from a source.

## Known weaknesses

- Head counts at year end, not FTE; part-time staff count as one.
- NYC is calendar 2023; Tokyo is April 2023 to March 2024.
- Hong Kong covers all its Hong Kong transport operations (heavy rail, light rail, buses, Airport Express, high-speed rail), not metro only.
- Pension and retiree-health accounting differs across countries; accrual charges can swing from year to year.
