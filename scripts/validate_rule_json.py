#!/usr/bin/env python3

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_RULE_KEYS = {
    "language",
    "standard_family",
    "rule_id",
    "rule_group",
    "rule_title",
    "classification",
    "severity",
    "validation_status",
    "summary_ko",
    "intent_ko",
    "domain_context_ko",
    "review_checklist",
    "common_violation_patterns",
    "noncompliant_example",
    "compliant_example",
    "fix_guidance",
    "sparrow_mapping",
    "keywords",
    "source_reference",
    "confidentiality",
    "notes",
}

LIST_KEYS = {
    "review_checklist",
    "common_violation_patterns",
    "fix_guidance",
    "sparrow_mapping",
    "keywords",
}

CONFIGS = [
    {
        "name": "C",
        "dir": ROOT / "knowledge/rules/c",
        "language": "C",
        "standard_family": "MISRA C 2012",
        "primary_key": "rules",
        "primary_count_key": "rule_count",
        "secondary_key": "directives",
        "secondary_count_key": "directive_count",
    },
    {
        "name": "C++",
        "dir": ROOT / "knowledge/rules/cpp",
        "language": "C++",
        "standard_family": "MISRA C++ 2008",
        "primary_key": "rules",
        "primary_count_key": "rule_count",
    },
    {
        "name": "Java",
        "dir": ROOT / "knowledge/rules/java",
        "language": "Java",
        "standard_family": "CERT Java",
        "primary_key": "rules",
        "primary_count_key": "rule_count",
    },
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(errors):
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)


def validate_rule_file(path: Path, expected_language: str, expected_standard: str, errors):
    data = load_json(path)
    missing = sorted(REQUIRED_RULE_KEYS - data.keys())
    if missing:
        errors.append(f"{path}: missing keys {missing}")
        return

    if data["language"] != expected_language:
        errors.append(f"{path}: language={data['language']} expected={expected_language}")
    if data["standard_family"] != expected_standard:
        errors.append(
            f"{path}: standard_family={data['standard_family']} expected={expected_standard}"
        )

    for key in LIST_KEYS:
        if not isinstance(data[key], list):
            errors.append(f"{path}: {key} must be a list")


def main():
    errors = []
    summaries = []

    for cfg in CONFIGS:
        index_path = cfg["dir"] / "_index.json"
        index_data = load_json(index_path)

        listed_primary = index_data.get(cfg["primary_key"], [])
        if len(listed_primary) != index_data.get(cfg["primary_count_key"]):
            errors.append(
                f"{index_path}: {cfg['primary_key']} count mismatch "
                f"listed={len(listed_primary)} expected={index_data.get(cfg['primary_count_key'])}"
            )

        listed_secondary = []
        if cfg.get("secondary_key"):
            listed_secondary = index_data.get(cfg["secondary_key"], [])
            if len(listed_secondary) != index_data.get(cfg["secondary_count_key"]):
                errors.append(
                    f"{index_path}: {cfg['secondary_key']} count mismatch "
                    f"listed={len(listed_secondary)} expected={index_data.get(cfg['secondary_count_key'])}"
                )

        listed_all = listed_primary + listed_secondary
        actual_all = sorted(
            p.name for p in cfg["dir"].glob("*.json") if p.name != "_index.json"
        )

        if len(actual_all) != len(listed_all):
            errors.append(
                f"{cfg['name']}: actual json file count mismatch actual={len(actual_all)} listed={len(listed_all)}"
            )

        missing_files = [name for name in listed_all if not (cfg["dir"] / name).exists()]
        if missing_files:
            errors.append(f"{cfg['name']}: missing listed files {missing_files}")

        for name in listed_all:
            path = cfg["dir"] / name
            if path.exists():
                validate_rule_file(path, cfg["language"], cfg["standard_family"], errors)

        summaries.append(
            f"{cfg['name']}: validated {len(listed_all)} rule json files "
            f"(primary={len(listed_primary)} secondary={len(listed_secondary)})"
        )

    if errors:
        fail(errors)

    print("rule_json_validation=ok")
    for summary in summaries:
        print(summary)


if __name__ == "__main__":
    main()
