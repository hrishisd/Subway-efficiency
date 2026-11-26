# Subway efficiency

How much does the New York City subway cost to run, per unit of service, compared with peer metros around the world? How reliable is it by comparison? What explains the gap?

This repository holds the dataset, the sources behind every number, and the analysis. **Capital and expansion costs are out of scope.** Only operating cost, operating efficiency, and reliability are covered.

## Status

Phase 1 (scoping) is done. See [`docs/scoping.md`](docs/scoping.md). Phase 2 (NYC baseline from the National Transit Database) is next.

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

## Core rule

**Every number traces to a source.** No row enters `data/observations.csv` without a `source_id` that exists in `sources/sources.csv` and a locator (page, table, or field) that lets someone else find the figure. Estimates are allowed but must be flagged and must link to a written method. See [`AGENTS.md`](AGENTS.md) for the full rules, which apply to people and AI agents alike.

Run `python3 scripts/validate.py` before committing.
