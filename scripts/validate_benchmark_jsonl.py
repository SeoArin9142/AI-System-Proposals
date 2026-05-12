#!/usr/bin/env python3

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONFIGS = [
    {
        "name": "C",
        "dir": ROOT / "knowledge/examples/c",
        "index": ROOT / "knowledge/examples/c/_index.json",
    }
]

REQUIRED_TOP_KEYS = {"benchmark_id", "metadata", "input", "expected"}
REQUIRED_METADATA_KEYS = {"schema_version", "validation_status", "source_rule_file", "source_kind"}
REQUIRED_INPUT_KEYS = {
    "language",
    "rule_group",
    "finding_id",
    "rule_candidates",
    "code",
    "context",
    "risk_context",
    "keywords",
}
REQUIRED_EXPECTED_KEYS = {
    "primary_rule",
    "severity",
    "decision",
    "explanation_ko",
    "review_focus",
    "must_mention",
    "noncompliant_signals",
    "fix_guidance",
    "acceptance_checks",
    "confidence",
    "keywords",
}
LIST_FIELDS = {
    ("input", "rule_candidates"),
    ("input", "keywords"),
    ("expected", "review_focus"),
    ("expected", "must_mention"),
    ("expected", "noncompliant_signals"),
    ("expected", "fix_guidance"),
    ("expected", "acceptance_checks"),
    ("expected", "keywords"),
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(errors):
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)


def validate_record(record, source, line_no, seen_ids, errors):
    missing = sorted(REQUIRED_TOP_KEYS - record.keys())
    if missing:
        errors.append(f"{source}:{line_no}: missing top-level keys {missing}")
        return

    benchmark_id = record["benchmark_id"]
    if benchmark_id in seen_ids:
        errors.append(f"{source}:{line_no}: duplicate benchmark_id {benchmark_id}")
    seen_ids.add(benchmark_id)

    metadata = record["metadata"]
    input_data = record["input"]
    expected = record["expected"]

    if sorted(REQUIRED_METADATA_KEYS - metadata.keys()):
        errors.append(f"{source}:{line_no}: metadata keys incomplete")
    if sorted(REQUIRED_INPUT_KEYS - input_data.keys()):
        errors.append(f"{source}:{line_no}: input keys incomplete")
    if sorted(REQUIRED_EXPECTED_KEYS - expected.keys()):
        errors.append(f"{source}:{line_no}: expected keys incomplete")

    for section, key in LIST_FIELDS:
        container = record[section]
        if key in container and not isinstance(container[key], list):
            errors.append(f"{source}:{line_no}: {section}.{key} must be a list")


def main():
    errors = []
    summaries = []

    for cfg in CONFIGS:
        index_data = load_json(cfg["index"])
        listed_files = index_data.get("files", [])
        expected_count = index_data.get("benchmark_count", 0)
        seen_ids = set()
        actual_count = 0

        for name in listed_files:
            path = cfg["dir"] / name
            if not path.exists():
                errors.append(f"{cfg['name']}: missing benchmark file {name}")
                continue

            with path.open("r", encoding="utf-8") as handle:
                for line_no, line in enumerate(handle, start=1):
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    validate_record(record, name, line_no, seen_ids, errors)
                    actual_count += 1

        if actual_count != expected_count:
            errors.append(
                f"{cfg['name']}: benchmark_count mismatch actual={actual_count} expected={expected_count}"
            )

        summaries.append(
            f"{cfg['name']}: validated {actual_count} benchmark records across {len(listed_files)} file(s)"
        )

    if errors:
        fail(errors)

    print("benchmark_jsonl_validation=ok")
    for summary in summaries:
        print(summary)


if __name__ == "__main__":
    main()
