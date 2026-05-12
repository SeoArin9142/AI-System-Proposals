#!/usr/bin/env python3

import json
import sys
from pathlib import Path


SELF = Path(__file__).resolve()
if SELF.parents[1].name == "pack":
    PACK = SELF.parents[1]
    ROOT = PACK.parent
else:
    ROOT = SELF.parents[1]
    PACK = ROOT / "pack"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def count_jsonl(path: Path):
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                json.loads(line)
                count += 1
    return count


def fail(errors):
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)


def main():
    errors = []

    manifest = load_json(PACK / "manifest.json")
    kb_manifest = load_json(PACK / "kb/rules_manifest.json")
    eval_manifest = load_json(PACK / "eval/eval_manifest.json")
    sft_manifest = load_json(PACK / "sft/dataset_manifest.json")

    rules_count = count_jsonl(PACK / "kb/rules.jsonl")
    if rules_count != kb_manifest["total_count"]:
        errors.append(
            f"kb rules count mismatch actual={rules_count} expected={kb_manifest['total_count']}"
        )

    eval_total = 0
    for _, item in eval_manifest["benchmarks"].items():
        file_count = count_jsonl(PACK / "eval" / item["file"])
        if file_count != item["count"]:
            errors.append(
                f"eval {item['file']} count mismatch actual={file_count} expected={item['count']}"
            )
        eval_total += file_count

    sft_total = 0
    for split in ("train", "val", "test"):
        count = count_jsonl(PACK / "sft" / f"{split}.jsonl")
        expected = sft_manifest["split_counts"][split]
        if count != expected:
            errors.append(f"sft {split} count mismatch actual={count} expected={expected}")
        sft_total += count

    if sft_total != sft_manifest["split_counts"]["total"]:
        errors.append(
            f"sft total mismatch actual={sft_total} expected={sft_manifest['split_counts']['total']}"
        )

    if manifest["counts"]["rule_cards"] != rules_count:
        errors.append("top-level manifest rule_cards mismatch")
    if manifest["counts"]["eval_records"] != eval_total:
        errors.append("top-level manifest eval_records mismatch")
    if manifest["counts"]["sft_records"] != sft_total:
        errors.append("top-level manifest sft_records mismatch")

    if errors:
        fail(errors)

    print("pack_validation=ok")
    print(f"rules={rules_count}")
    print(f"eval={eval_total}")
    print(f"sft={sft_total}")


if __name__ == "__main__":
    main()
