# Method: mlit_opex_excl_depreciation

**Used for:** `opex_total` of `tokyo_metro` and `tokyo_toei`, FY2015 to FY2023 (obs_ids `*_opex_total_mlit`).

**Type:** derived

## Inputs

| Input | obs_id or source_id + locator |
| --- | --- |
| Railway operating expense including depreciation (営業費計（厚生福利施設収入控除前）) | `<system>_<year>_opex_incl_depreciation_mlit` |
| Depreciation (減価償却費) | `<system>_<year>_depreciation_mlit` |

Both come from the MLIT railway statistics yardstick table (sources `mlit_yardstick_fy<year>`), table 地下鉄事業者.

## Formula

opex_total = 営業費計（厚生福利施設収入控除前） − 減価償却費

This equals the printed 合計 (all operating cost items) plus 諸税 (taxes). The transcription in `data/raw/asia/mlit_yardstick_tokyo.csv` is checked by `scripts/build_tokyo_inputs.py` against three printed identities: the seven transport cost items sum to 運送費計; 運送費計 + publicity + welfare facilities + general administration = 合計; 合計 + depreciation + taxes = 営業費計 (FY2020 Tokyo Metro is off by ¥1,000, a rounding difference in the source).

## Assumptions

- Depreciation is removed so the figure matches the NTD definition of operating expense used for US systems. Everything else stays in: labor, materials, power, contracted services, leases (賃借料), taxes, and general administration of the railway business.
- The yardstick table covers the **railway business only**. Tokyo Metro's real estate, retail and advertising businesses are not in it. Its general administration (一般管理費) is the part the company assigns to the railway business.
- Welfare facility income (厚生福利施設収入, under ¥0.6 billion a year) is not deducted.

## Range

Not an estimate. No range.

## Known weaknesses

- Toei Subway's figure comes from a public enterprise account. Toei pays almost no taxes (諸税 is zero or ¥1,000), while Tokyo Metro pays about ¥10-14 billion a year. The NTD figure for NYC also has no corporate tax. For a strict comparison subtract 諸税 from Tokyo Metro (about 5% of its opex_total).
- Pension and retirement costs follow Japanese accounting rules, which differ from US GASB rules.
- Car-use fees paid to other operators for through-running (車両使用料) are in operating expense; car-use fees received are revenue, not a cost offset.
