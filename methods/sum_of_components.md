# Method: sum_of_components

**Used for:** a total that the source does not print but whose parts it does, for example `opex_total` = `opex_direct` + `opex_indirect_allocated` for London Underground.

**Type:** derived

## Inputs

The component rows listed in `inputs`, all from the same system, year and scope.

## Formula

total = sum of the input values.

## Assumptions

None, other than that the parts do not overlap. For TfL, the check is that direct plus indirect operating cost equals the Underground segment's gross expenditure in the audited accounts for the years where both exist (2018/19: 2,027 + 383 = 2,410; 2019/20: 1,979 + 344 = 2,323, in £m).

## Range

Not an estimate. No range.

## Known weaknesses

The parts can be restated in later reports. Each input row names the report used.
