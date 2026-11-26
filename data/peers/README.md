# Peer-system input files

One file per non-US system: `<system_id>.csv`, with the same columns as `data/observations.csv`. Put only hand-entered rows here: `reported` values from sources, `estimated` values (with `method_id`, `value_low`, `value_high`), and any `derived` row the script cannot make (for example a unit conversion). Use nominal local currency (`price_basis` = `nominal`).

Then run `python3 scripts/build_peers.py`. It adds the standard ratio rows (method `peer_unit_ratios`) and the 2024 PPP dollar rows (method `ppp_usd_2024`, suffix `_ppp24`), and rewrites every row of these systems in `data/observations.csv`. Do not edit those systems' rows in `observations.csv` by hand: edit the peer file and run the script again. After a rebase, rerun the script to settle conflicts in `observations.csv`.

Conventions:
- `year` is the calendar year in which the fiscal year starts. Say the fiscal year in `year_basis` (for example `fiscal_apr_mar` or `calendar`).
- End each obs_id with a short tag for the source (for example `_tfl`). Ratio rows reuse the numerator's tag.
- Keep one row per metric for each system, year and scope, or the script cannot pick inputs for ratios.
