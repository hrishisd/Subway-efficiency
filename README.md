# Subway efficiency

How much does the New York City subway cost to run, per unit of service, compared with peer metros around the world? How reliable is it by comparison? What explains the gap?

This repository holds the dataset, the sources behind every number, and the analysis. **Capital and expansion costs are out of scope.** Only operating cost, operating efficiency, and reliability are covered.

## Report

The research report is [`report/report.md`](report/report.md), built from the data by `scripts/build_report.py`.

## Website

A chart-first summary of the findings is published at https://hrishisd.github.io/Subway-efficiency/ . It is [`site/index.html`](site/index.html), **generated** from the CSVs by `python3 scripts/build_site.py` (edit [`site/template.html`](site/template.html) and the script, not `index.html`). Every chart value links to its row in the data and to its sources; [`site/data.json`](site/data.json) lists every value and computed ratio with its input rows. The GitHub Actions workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) rebuilds and publishes the site on every push to `main`.

## Status

Phase 1 (scoping) is done. See [`docs/scoping.md`](docs/scoping.md). Phase 2 (NYC baseline from the National Transit Database, 2015 to 2025, with six US peers) is in [`docs/ntd_baseline.md`](docs/ntd_baseline.md). Years 2000 to 2014 are still open.

## Layout

| Path | What it holds |
| --- | --- |
| [`docs/scoping.md`](docs/scoping.md) | Research questions, peer set, comparability rules, plan |
| [`data/systems.csv`](data/systems.csv) | The metro systems in the study and their tier |
| [`data/metrics.csv`](data/metrics.csv) | Definition and unit of every metric |
| [`data/observations.csv`](data/observations.csv) | Every number, one per row, each tied to a source |
| [`sources/sources.csv`](sources/sources.csv) | Every source, with URL and access date |
| [`methods/`](methods/) | One note per derived or estimated figure method |
| [`scripts/validate.py`](scripts/validate.py) | Checks that every number has a valid source and method |
| [`scripts/build_ntd_baseline.py`](scripts/build_ntd_baseline.py) | Rebuilds the NTD rows from the raw extracts in [`data/raw/ntd/`](data/raw/ntd/) |
| [`docs/ntd_baseline.md`](docs/ntd_baseline.md) | Phase 2 summary: NYC and US peers from NTD |
| [`docs/expert_explanations.md`](docs/expert_explanations.md) | What other analysts (CBC, State Comptroller, MTA, Imperial College, Transit Costs Project, Alon Levy) say explains NYC's operating cost, and how it fits our data |

## Core rule

**Every number traces to a source.** No row enters `data/observations.csv` without a `source_id` that exists in `sources/sources.csv` and a locator (page, table, or field) that lets someone else find the figure. Estimates are allowed but must be flagged and must link to a written method. See [`AGENTS.md`](AGENTS.md) for the full rules, which apply to people and AI agents alike.

Run `python3 scripts/validate.py` before committing.
