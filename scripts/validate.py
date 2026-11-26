#!/usr/bin/env python3
"""Check that every observation traces to a source and, where needed, a method.

Run from the repository root: python3 scripts/validate.py
Exits with status 1 if any check fails.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALUE_TYPES = {"reported", "derived", "estimated"}
VERIFICATION = {"unverified", "verified"}


def read(path):
    with open(ROOT / path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    errors = []
    systems = {r["system_id"] for r in read("data/systems.csv")}
    metrics = {r["metric_id"] for r in read("data/metrics.csv")}
    sources = read("sources/sources.csv")
    source_ids = set()
    for s in sources:
        sid = s["source_id"]
        if sid in source_ids:
            errors.append(f"sources.csv: duplicate source_id {sid}")
        source_ids.add(sid)
        if not s["url"].strip():
            errors.append(f"sources.csv: {sid} has no url")
        if not s["accessed_on"].strip():
            errors.append(f"sources.csv: {sid} has no accessed_on date")

    factors = read("data/raw/ppp/ppp_deflator.csv")
    factor_ids = set()
    for fct in factors:
        if fct["factor_id"] in factor_ids:
            errors.append(f"ppp_deflator.csv: duplicate factor_id {fct['factor_id']}")
        factor_ids.add(fct["factor_id"])
        if fct["source_id"] not in source_ids:
            errors.append(f"ppp_deflator.csv: {fct['factor_id']}: source_id not in sources.csv")
        if not fct["source_locator"].strip():
            errors.append(f"ppp_deflator.csv: {fct['factor_id']}: source_locator is empty")

    obs = read("data/observations.csv")
    obs_ids = {o["obs_id"] for o in obs}
    seen = set()
    for o in obs:
        oid = o["obs_id"]
        where = f"observations.csv: {oid}"
        if oid in seen:
            errors.append(f"{where}: duplicate obs_id")
        seen.add(oid)
        if o["system_id"] not in systems:
            errors.append(f"{where}: unknown system_id {o['system_id']}")
        if o["metric_id"] not in metrics:
            errors.append(f"{where}: unknown metric_id {o['metric_id']}")
        try:
            float(o["value"])
        except ValueError:
            errors.append(f"{where}: value is not a number")
        if o["value_type"] not in VALUE_TYPES:
            errors.append(f"{where}: value_type must be one of {sorted(VALUE_TYPES)}")
        if o["verification"] not in VERIFICATION:
            errors.append(f"{where}: verification must be one of {sorted(VERIFICATION)}")
        if o["source_id"] not in source_ids:
            errors.append(f"{where}: source_id {o['source_id']!r} not in sources.csv")
        if not o["source_locator"].strip():
            errors.append(f"{where}: source_locator is empty")
        if o["value_type"] in {"derived", "estimated"} and o["method_id"].strip():
            if not (ROOT / "methods" / f"{o['method_id']}.md").exists():
                errors.append(f"{where}: methods/{o['method_id']}.md does not exist")
        if o["value_type"] == "derived":
            if not o["method_id"].strip():
                errors.append(f"{where}: derived value needs method_id")
            for i in filter(None, o["inputs"].split(";")):
                if i.strip() not in obs_ids and i.strip() not in factor_ids:
                    errors.append(f"{where}: input {i!r} is not an obs_id or price factor_id")
        if o["value_type"] == "estimated":
            # Estimates taken from a secondary source may lack our own method;
            # they must stay unverified until replaced or given a method.
            if not o["method_id"].strip() and o["verification"] == "verified":
                errors.append(f"{where}: verified estimate needs method_id")
            if o["method_id"].strip() and not (o["value_low"] and o["value_high"]):
                errors.append(f"{where}: estimate needs value_low and value_high")
            for i in filter(None, o["inputs"].split(";")):
                if i.strip() not in obs_ids and i.strip() not in factor_ids:
                    errors.append(f"{where}: input {i!r} is not an obs_id or price factor_id")

    n_fact, n_rel = check_factors_and_reliability(errors, systems, source_ids)

    for e in errors:
        print(e)
    print(f"{len(obs)} observations, {n_fact} factors, {n_rel} reliability rows, "
          f"{len(source_ids)} sources, {len(errors)} errors")
    return 1 if errors else 0


def check_factors_and_reliability(errors, systems, source_ids):
    """Check data/factors.csv and data/reliability.csv (added for explanatory
    factors and reliability). Same sourcing rules as observations.csv."""
    if not (ROOT / "data/factors.csv").exists():
        return 0, 0
    defs = {d["factor_id"]: d for d in read("data/factor_definitions.csv")}
    rel_metrics = {m["metric_id"] for m in read("data/reliability_metrics.csv")}
    facts = read("data/factors.csv")
    rels = read("data/reliability.csv")
    rel_ids = {r["rel_id"] for r in rels}
    for table, rows, id_col in (("factors.csv", facts, "fact_id"),
                                ("reliability.csv", rels, "rel_id")):
        seen = set()
        for r in rows:
            rid = r[id_col]
            where = f"{table}: {rid}"
            if rid in seen:
                errors.append(f"{where}: duplicate {id_col}")
            seen.add(rid)
            if r["system_id"] not in systems:
                errors.append(f"{where}: unknown system_id {r['system_id']}")
            if r["value_type"] not in VALUE_TYPES:
                errors.append(f"{where}: value_type must be one of {sorted(VALUE_TYPES)}")
            if r["verification"] not in VERIFICATION:
                errors.append(f"{where}: verification must be one of {sorted(VERIFICATION)}")
            if r["source_id"] not in source_ids:
                errors.append(f"{where}: source_id {r['source_id']!r} not in sources.csv")
            if not r["source_locator"].strip():
                errors.append(f"{where}: source_locator is empty")
            if r["value_type"] in {"derived", "estimated"}:
                if not r["method_id"].strip():
                    errors.append(f"{where}: {r['value_type']} value needs method_id")
                elif not (ROOT / "methods" / f"{r['method_id']}.md").exists():
                    errors.append(f"{where}: methods/{r['method_id']}.md does not exist")
            if r["value_type"] == "estimated" and not (r["value_low"] and r["value_high"]):
                errors.append(f"{where}: estimate needs value_low and value_high")
        for r in rows:
            if table == "reliability.csv" and r["value_type"] == "derived":
                for i in filter(None, r["inputs"].split(";")):
                    if i.strip() not in rel_ids:
                        errors.append(f"reliability.csv: {r['rel_id']}: input {i!r} is not a rel_id")
    for f in facts:
        where = f"factors.csv: {f['fact_id']}"
        d = defs.get(f["factor_id"])
        if d is None:
            errors.append(f"{where}: unknown factor_id {f['factor_id']}")
            continue
        if d["kind"] == "numeric":
            try:
                float(f["value"])
            except ValueError:
                errors.append(f"{where}: value is not a number")
        elif d["kind"] == "categorical":
            allowed = set(d["allowed_values"].split(";"))
            if f["value"] not in allowed:
                errors.append(f"{where}: value {f['value']!r} not in {sorted(allowed)}")
        elif not f["value"].strip():
            errors.append(f"{where}: value is empty")
    for r in rels:
        where = f"reliability.csv: {r['rel_id']}"
        if r["metric_id"] not in rel_metrics:
            errors.append(f"{where}: unknown metric_id {r['metric_id']}")
        try:
            float(r["value"])
        except ValueError:
            errors.append(f"{where}: value is not a number")
        if not r["agency_definition"].strip():
            errors.append(f"{where}: agency_definition is empty")
    return len(facts), len(rels)


if __name__ == "__main__":
    sys.exit(main())
