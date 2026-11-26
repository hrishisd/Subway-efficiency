# Why NYC subway "general administration" cost more than doubled after 2022

**Short answer.** The jump has two parts. The 2024 step is mostly a rise in **claims reserves** (casualty and liability), which MTA's audited statements attribute to reserves for selected injury cases. The 2023 step is **not** claims: it is labor cost booked to the administration function, and it coincides with the number of NTD-reported administration staff on the subway roughly doubling in one year. Whether that was real hiring or staff being reclassified into the administration function is **not yet known**. The rise is agency-wide (bus administration rose by a similar share), so it is not a shift of overhead from bus to subway.

All dollar figures are nominal. Rows marked with an obs_id are in `data/observations.csv`; other figures give their source and locator inline. This is analysis, not new data: no value here is an estimate except where marked **[assumption]**.

## 1. The size of the jump

NYC subway (NTD heavy rail, MTA New York City Transit), general administration operating expense (`nyc_subway_<year>_opex_general_administration_ntd`):

| Year | General administration | Change |
| --- | ---: | ---: |
| 2022 | $592M | |
| 2023 | $1,015M | +$423M |
| 2024 | $1,487M | +$472M |
| 2025 | $1,397M | −$90M |

## 2. Not a shift from bus to subway

The same NTD table for all NYCT modes (source `ntd_opex_by_function`, dataset dkxx-zjd6, `ntd_id=20008`, column `general_administration`) shows bus (mode MB) administration rising at a similar rate: $395M (2022), $589M (2023), $877M (2024), $846M (2025). Across all five NYCT modes, administration went from $1,185M (2022) to $2,554M (2024). If overhead had simply moved from bus to subway, bus administration would have fallen. It rose.

## 3. 2023 to 2024: claims reserves

NTD casualty and liability cost for the subway (`nyc_subway_<year>_opex_type_casualty_and_liability_ntd`, source `ntd_opex_by_type`): $174M (2022), $167M (2023), $578M (2024), $443M (2025). Bus (same dataset, mode MB): $93M, $85M, $306M, $245M.

In the 2025 NTD cross tab of function by object class (source `ntd_opex_function_by_type_2025`, dataset 4ucy-dac3, column `casualty_and_liability_costs`), **all** subway casualty and liability cost sits in general administration. **[assumption]** The same was true in 2022 to 2024. The function-by-type cross tab for those years was not found on the portal.

On that assumption, casualty and liability explains about $411M of the $472M rise in 2024 (87%), and about $403M of the $895M rise from 2022 to 2024 (45%).

MTA's own reports tell the same story, for subway and bus combined:

- Audited public liability claims expense, in thousands of USD: 243,770 (2023), 800,163 (2024), 645,536 (2025). Source `nycta_fs_2025`, table on p.10 (page inferred from printed markers). The 2024 rise is described as "primarily due to the increase in claims reserve for selected cases" (p.11), and the 2025 fall as "primarily due to the higher claims reserve in the prior year" (p.11).
- The 2024 year-end report says claims were "$247.7 million unfavorable to the Final Estimate, reflecting the latest actuarial estimate" (source `mta_nyct_2024_year_end`, section on non-labor expenses).

So the 2024 step is an accounting accrual for expected injury payouts. It is a real cost, but it is lumpy, and it is not a change in how many people run the subway.

## 4. 2022 to 2023: administration labor, cause not yet known

Casualty and liability fell slightly in 2023, so the $423M rise that year came from elsewhere. Across all four subway functions, object classes that grew most from 2022 to 2023 (source `ntd_opex_by_type`): other salaries and wages +$296M, fringe benefits +$178M, other materials and supplies +$103M, miscellaneous +$71M, services +$53M. Function-level data for 2022 and 2023 by object class is not available, so these cannot be tied to administration alone.

The NTD Employees table shows the change clearly (source `ntd_employees_by_mode`, full-time rows):

| Year | Admin staff (count) | Admin hours | All subway full-time staff |
| --- | ---: | ---: | ---: |
| 2022 | 1,127 | 1.72M | 29,766 |
| 2023 | 2,192 | 3.33M | 31,450 |
| 2024 | 2,334 | 3.67M | 32,647 |
| 2025 | 2,402 | 3.85M | 33,200 |

(rows `nyc_subway_<year>_employee_count_general_administration_ft_ntd`, `..._employee_hours_general_administration_ft_ntd`, `..._employee_count_total_ft_ntd`)

Subway administration staff nearly doubled in one year (+1,065). The other operating functions did not shrink to match: vehicle operations went from 6,652 to 6,604, vehicle maintenance from 5,094 to 5,029, and facility maintenance from 12,609 to 12,862.

Two explanations fit and the data here cannot separate them:

1. **Reclassification.** Staff who already worked for NYCT (for example in safety, security, customer-facing or support roles, or staff previously charged to capital work) began to be reported under the NTD administration function. Capital labor also rose (4,284 to 4,763 full-time), so a shift between capital and operating charging is possible.
2. **Real growth** in administrative staff.

Evidence against simple hiring: MTA's 2023 year-end report shows NYCT's "Administration" department **below** its budgeted headcount, with 312 positions, or 32%, vacant (source `mta_nyct_2023_year_end`, headcount table). That department has far fewer people than the 2,192 subway staff NTD reports under administration, so NTD's "general administration" function is wider than MTA's "Administration" department. That points toward a change in how staff are mapped to NTD functions, but it is not proof.

## 5. What this means for the comparison

- Read NYC trends with and without administration (`opex_excl_ga_per_car_km`). In constant 2024 dollars, NYC cost per car-km excluding administration **fell** from $10.40 (2015) to $8.93 (2024); including administration it was about flat ($12.40 to $11.58). See `docs/ntd_baseline.md`.
- For cross-system comparison, treat claims accruals separately. A single year's reserve change can move NYC cost per car-km by about $0.73 (the 2024 casualty rise of $411M over 562M car-km).
- MTA pension and OPEB accounting (GASB 68 and 75) produced large swings in MTA's own reports in 2023 and 2024, but NTD fringe benefits for the subway were nearly flat from 2023 to 2024 ($1,947M to $1,928M), so they do not explain the NTD administration jump.

## Open questions

- Get the NTD function-by-object-class cross tab for 2022 to 2024 (to confirm the casualty assumption and locate the 2023 labor rise).
- Ask or search for an NTD reporting note from NYCT about re-mapping staff to functions in report year 2023.
- MTA documents cover subway and bus together. Their claims figures (for example $800M in 2024) are not directly comparable with NTD subway-only figures ($578M).
