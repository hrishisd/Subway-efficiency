# Rules for contributors (people and AI agents)

This repository is built by several agents working over time. These rules let any agent check any number without asking anyone.

## 1. Every number has a source

- Every row in `data/observations.csv` has a `source_id` that exists in `sources/sources.csv`.
- `source_locator` says exactly where in the source the number is: page and table, field name, or section heading. "See report" is not enough.
- Add a source to `sources/sources.csv` **before** you use it. Give the direct URL to the document, not to a search page. Fill `accessed_on` with the date you opened it.
- If the source is a PDF or a page that may change, also record an archived copy in `archive_url` (for example from web.archive.org) when you can.
- Never enter a number from memory. If you cannot find a source, leave the number out and list it as an open question in the pull request.

## 2. Mark what kind of number it is

`value_type` must be one of:

- `reported`: copied as published by the source. Only unit or currency formatting may change.
- `derived`: computed from other rows by arithmetic (for example cost divided by car-km). Fill `method_id`, and list the input rows' `obs_id`s in `inputs`.
- `estimated`: needs an assumption that is not in any source (for example splitting a company-wide cost between metro and bus). Fill `method_id`. The method note must give the inputs, the formula, every assumption, and a low and high value (`value_low`, `value_high`).

Estimates must be impossible to miss. Every table or chart in the report marks estimated values.

`verification` is `unverified` until a second agent or person has opened the source and confirmed the number and locator, then `verified`. Secondary sources (blogs, news, other people's compilations) stay `unverified` until checked against the primary source.

## 3. Keep scope explicit

The `scope` column says what the number covers, for example `metro_only`, `metro_with_allocated_overhead`, or `whole_agency`. Comparisons must use the same scope, or say clearly that they do not. See the comparability table in `docs/scoping.md`.

Money values carry `currency` and `price_basis` (`nominal`, or for example `PPP_USD_2024`). Keep the nominal local-currency value as a `reported` row and add conversions as `derived` rows.

## 4. Methods

A derived or estimated row points to a file `methods/<method_id>.md`. Use `methods/_template.md`. One method can serve many rows.

## 5. Workflow

- Work on a branch and open a pull request. Do not push to `main` directly.
- Run `python3 scripts/validate.py` and make sure it passes.
- In the pull request, list the sources added and anything you could not find.
- Keep CSVs sorted by `system_id`, then `year`, then `metric_id`, so diffs stay readable.
- Use IDs in lowercase with underscores (for example `nyc_subway`, `ntd_2024_mta_nyct`).
