#!/usr/bin/env python3
"""Check decision-record integrity. Read-only; standard library only."""
import json
import sys
from datetime import date
from pathlib import Path


def validate(record):
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def check_date(value, field):
        try:
            date.fromisoformat(value)
        except (ValueError, TypeError):
            errors.append(f"{field}: expected ISO date YYYY-MM-DD")

    if not isinstance(record, dict):
        return ["record: expected object"]
    require(nonempty(record.get("question")), "question: missing")
    facts = record.get("facts", [])
    options = record.get("options", [])
    if not isinstance(facts, list) or not isinstance(options, list):
        return errors + ["facts/options: expected arrays"]
    fact_map = {}
    for fact in facts:
        if not isinstance(fact, dict):
            errors.append("fact: expected object")
            continue
        fid = fact.get("id")
        require(nonempty(fid), "fact.id: missing")
        if not nonempty(fid):
            continue
        require(fid not in fact_map, f"fact.id: duplicate {fid}")
        fact_map[fid] = fact
        require(nonempty(fact.get("text")), f"{fid}.text: missing")
        require(nonempty(fact.get("source")), f"{fid}.source: missing")
        require(fact.get("status") in ("confirmed", "assumption", "unknown", "conflict"), f"{fid}.status: invalid")
    option_ids = []
    for option in options:
        if not isinstance(option, dict):
            errors.append("option: expected object")
            continue
        oid = option.get("id")
        require(nonempty(oid), "option.id: missing")
        if nonempty(oid):
            require(oid not in option_ids, f"option.id: duplicate {oid}")
            option_ids.append(oid)
        require(nonempty(option.get("text")), "option.text: missing")
    require(bool(option_ids), "options: empty")
    rec = record.get("recommendation")
    if not isinstance(rec, dict):
        return errors + ["recommendation: expected object"]
    require(rec.get("option_id") in option_ids, "recommendation.option_id: unknown option")
    require(nonempty(rec.get("conditions")), "recommendation.conditions: missing")
    require(nonempty(rec.get("reconsider_if")), "recommendation.reconsider_if: missing")
    for field, statuses in (
        ("basis_fact_ids", ("confirmed",)),
        ("assumption_fact_ids", ("assumption",)),
        ("unknown_fact_ids", ("unknown", "conflict")),
    ):
        ids = rec.get(field)
        if not isinstance(ids, list):
            errors.append(f"recommendation.{field}: expected array")
            continue
        for fid in ids:
            if not isinstance(fid, str) or fid not in fact_map:
                errors.append(f"{field}: unknown fact reference {fid!r}")
            elif fact_map[fid].get("status") not in statuses:
                errors.append(f"{field}: {fid} has incompatible status")
    require("user_decision" in record, "user_decision: missing (use null if undecided)")
    require(record.get("user_decision") is None or record.get("user_decision") in option_ids, "user_decision: unknown option")
    step = record.get("next_step")
    if not isinstance(step, dict):
        return errors + ["next_step: expected object"]
    for field in ("owner", "action", "budget_cap", "observe", "stop_if"):
        require(nonempty(step.get(field)), f"next_step.{field}: missing")
    check_date(step.get("due"), "next_step.due")
    check_date(record.get("review_on"), "review_on")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: check_record.py <record.json>", file=sys.stderr)
        return 2
    try:
        record = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Cannot read record: {exc}", file=sys.stderr)
        return 2
    errors = validate(record)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Record integrity passed; source truth and decision quality remain unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
