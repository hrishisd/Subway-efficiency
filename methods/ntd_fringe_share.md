# Method: ntd_fringe_share

**Used for:** `pension_benefit_share` rows in `data/factors.csv` for the seven US heavy-rail systems (NTD report year 2024).

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Operating expense by object class | `ntd_opex_by_type` (dataset j5uj-anzx), mode=HR, report_year=2024, one row per agency. Copy: `data/raw/ntd/opex_by_type_hr_2024.csv` |

## Formula

Labor cost = operators_wages + other_salaries_wages + operator_paid_absences + other_paid_absences + fringe_benefits.

Fringe share of labor cost = fringe_benefits / labor cost. The value is in `value`.

The notes column also gives fringe_benefits / total operating expense.

Check: for every agency the expense columns add up exactly to `total`.

## Assumptions

- NTD "fringe benefits" includes pensions, health insurance, payroll taxes and other benefits. It is the closest public measure to the pension and benefit cost share for US systems. It does not separate pensions.
- Purchased transportation is zero for these heavy-rail rows, so contracted labor does not hide inside "services". Some labor may still be in "services" (for example PATH, whose services line is large).

## Range

Not an estimate; no range.

## Known weaknesses

- Only report year 2024 is used. The dataset holds 2022 onward; 2019 is not available in it.
- Agencies differ in how they book pension costs (for example GASB 68 pension expense versus contributions), so year-to-year swings can be accounting effects.
- No comparable figure was found for foreign systems.
