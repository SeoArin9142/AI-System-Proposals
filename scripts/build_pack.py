#!/usr/bin/env python3

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack"

RULE_CONFIGS = [
    {
        "language": "C",
        "standard_family": "MISRA C 2012",
        "index": ROOT / "knowledge/rules/c/_index.json",
        "dir": ROOT / "knowledge/rules/c",
    },
    {
        "language": "C++",
        "standard_family": "MISRA C++ 2008",
        "index": ROOT / "knowledge/rules/cpp/_index.json",
        "dir": ROOT / "knowledge/rules/cpp",
    },
    {
        "language": "Java",
        "standard_family": "CERT Java",
        "index": ROOT / "knowledge/rules/java/_index.json",
        "dir": ROOT / "knowledge/rules/java",
    },
]

EVAL_CONFIGS = [
    {
        "language": "C",
        "standard_family": "MISRA C 2012",
        "index": ROOT / "knowledge/examples/c/_index.json",
        "dir": ROOT / "knowledge/examples/c",
        "output": "benchmark_c.jsonl",
    },
    {
        "language": "C++",
        "standard_family": "MISRA C++ 2008",
        "index": ROOT / "knowledge/examples/cpp/_index.json",
        "dir": ROOT / "knowledge/examples/cpp",
        "output": "benchmark_cpp.jsonl",
    },
    {
        "language": "Java",
        "standard_family": "CERT Java",
        "index": ROOT / "knowledge/examples/java/_index.json",
        "dir": ROOT / "knowledge/examples/java",
        "output": "benchmark_java.jsonl",
    },
]

SYSTEM_PROMPT = """# Reviewer System Prompt

당신은 정적분석 기반 코드 리뷰어다.

목표:
- 주어진 규칙 후보, 정적분석 finding, 코드 조각을 보고 가장 적합한 규칙을 식별한다.
- 위반 원인을 한국어로 설명한다.
- 도메인 위험과 연결해 위험도를 판단한다.
- 수정 가이드를 탐지/판단/수정/검증 단계로 제시한다.

출력 원칙:
- 추정은 줄이고 입력 근거를 우선한다.
- 규칙 후보가 불명확하면 불확실성을 명시한다.
- 코드 수정 제안은 보수적으로 제시한다.
- JSON 구조를 깨지 않는다.
"""


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_jsonl(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_rule_exports():
    output_path = PACK / "kb/rules.jsonl"
    records = []
    language_counts = {}
    validation_counts = {}

    for cfg in RULE_CONFIGS:
        index_data = load_json(cfg["index"])
        listed = list(index_data.get("rules", [])) + list(index_data.get("directives", []))
        language_counts[cfg["language"]] = len(listed)

        for name in listed:
            source_path = cfg["dir"] / name
            payload = load_json(source_path)
            payload["source_file"] = str(source_path.relative_to(ROOT))
            payload["record_type"] = "rule_card"
            records.append(payload)
            status = payload.get("validation_status", "unknown")
            validation_counts[status] = validation_counts.get(status, 0) + 1

    records.sort(key=lambda item: (item["language"], item["rule_id"]))
    write_jsonl(output_path, records)

    manifest = {
        "schema_version": "1.0",
        "record_type": "rule_card",
        "purpose": "model-agnostic knowledge base export for RAG or downstream transformation",
        "total_count": len(records),
        "language_counts": language_counts,
        "validation_status_counts": validation_counts,
        "files": ["rules.jsonl"],
        "source_indexes": [str(cfg["index"].relative_to(ROOT)) for cfg in RULE_CONFIGS],
        "notes": [
            "규칙 카드 원본을 JSONL로 합친 export 파일이다.",
            "일부 classification/title/summary는 draft-unverified 상태다.",
            "벤더별 지식베이스 포맷 요구가 있으면 이 파일에서 최종 변환한다.",
        ],
    }
    write_json(PACK / "kb/rules_manifest.json", manifest)
    return manifest


def build_eval_exports():
    manifest = {
        "schema_version": "1.1",
        "purpose": "evaluation and few-shot seed datasets",
        "benchmarks": {},
    }

    for cfg in EVAL_CONFIGS:
        index_data = load_json(cfg["index"])
        records = []
        for name in index_data.get("files", []):
            records.extend(load_jsonl(cfg["dir"] / name))

        output_name = cfg["output"]
        write_jsonl(PACK / "eval" / output_name, records)
        manifest["benchmarks"][cfg["language"]] = {
            "standard_family": cfg["standard_family"],
            "file": output_name,
            "count": len(records),
            "source_index": str(cfg["index"].relative_to(ROOT)),
            "validation_status": index_data.get("validation_status", "unknown"),
        }

    write_json(PACK / "eval/eval_manifest.json", manifest)
    return manifest


def build_sft_exports():
    source_records = load_jsonl(ROOT / "knowledge/examples/c/reviewer-benchmark.v1.jsonl")
    source_records.sort(key=lambda item: item["benchmark_id"])

    sft_records = []
    for item in source_records:
        sft_records.append(
            {
                "sample_id": item["benchmark_id"],
                "instruction": "주어진 정적분석 finding과 코드 조각을 검토해 적용 규칙, 위험, 수정 가이드를 JSON 형식으로 정리하라.",
                "input": {
                    "language": item["input"]["language"],
                    "rule_group": item["input"]["rule_group"],
                    "finding_id": item["input"]["finding_id"],
                    "rule_candidates": item["input"]["rule_candidates"],
                    "code": item["input"]["code"],
                    "context": item["input"]["context"],
                    "risk_context": item["input"]["risk_context"],
                    "keywords": item["input"]["keywords"],
                },
                "output": item["expected"],
                "metadata": {
                    "schema_version": "1.0",
                    "standard_family": "MISRA C 2012",
                    "validation_status": item["metadata"]["validation_status"],
                    "source_benchmark_id": item["benchmark_id"],
                    "source_rule_file": item["metadata"]["source_rule_file"],
                    "source_kind": item["metadata"]["source_kind"],
                },
            }
        )

    train_records = sft_records[:8]
    val_records = sft_records[8:10]
    test_records = sft_records[10:]

    write_jsonl(PACK / "sft/train.jsonl", train_records)
    write_jsonl(PACK / "sft/val.jsonl", val_records)
    write_jsonl(PACK / "sft/test.jsonl", test_records)
    write_text(PACK / "sft/system_prompt.md", SYSTEM_PROMPT)

    manifest = {
        "schema_version": "1.0",
        "format": "instruction-input-output",
        "purpose": "seed SFT dataset for later model-specific conversion",
        "split_counts": {
            "train": len(train_records),
            "val": len(val_records),
            "test": len(test_records),
            "total": len(sft_records),
        },
        "source": {
            "language": "C",
            "standard_family": "MISRA C 2012",
            "benchmark_file": "knowledge/examples/c/reviewer-benchmark.v1.jsonl",
        },
        "notes": [
            "현재는 C benchmark 12건만 seed dataset으로 포함한다.",
            "모델 벤더별 포맷 요구가 있으면 train/val/test를 후처리해서 맞춘다.",
            "실제 fine-tuning 전에는 validation_status와 정답 품질을 추가 검증해야 한다.",
        ],
    }
    write_json(PACK / "sft/dataset_manifest.json", manifest)
    return manifest


def write_pack_readme(kb_manifest, eval_manifest, sft_manifest):
    text = f"""# Pack

폐쇄망 모델 도입 전 단계에서 사용할 수 있는 **모델 비의존 export 패키지**입니다.

목적:
- 현재 `knowledge/` 원본 데이터를 한 번 더 정리해 RAG / eval / SFT 초안에 바로 연결
- 향후 벤더 전용 포맷이 확정되면 `pack/`만 변환하면 되게 만들기

구성:
- `kb/rules.jsonl` : 규칙 카드 통합 knowledge base export
- `eval/benchmark_*.jsonl` : 평가/ few-shot seed 데이터
- `sft/train.jsonl`, `val.jsonl`, `test.jsonl` : seed SFT 데이터
- `tools/validate_pack.py` : pack 산출물 검증 스크립트

현재 export 범위:
- rules total: {kb_manifest["total_count"]}
- eval C/C++/Java: {eval_manifest["benchmarks"]["C"]["count"]}/{eval_manifest["benchmarks"]["C++"]["count"]}/{eval_manifest["benchmarks"]["Java"]["count"]}
- sft total: {sft_manifest["split_counts"]["total"]}

재생성:
```bash
python3 scripts/build_pack.py
python3 scripts/validate_pack.py
```

주의:
- 현재 데이터는 `draft-unverified` 성격이 포함됩니다.
- C benchmark만 SFT seed로 변환되어 있습니다.
- 실제 폐쇄망 모델 반입 시 벤더 포맷, tokenizer, role schema 요구사항에 맞는 마지막 변환은 별도로 수행해야 합니다.
"""
    write_text(PACK / "README.md", text)


def write_top_level_manifest(kb_manifest, eval_manifest, sft_manifest):
    manifest = {
        "schema_version": "1.0",
        "package_name": "closed-network-llm-bootstrap-pack",
        "purpose": "model-agnostic bootstrap package for RAG, eval, and later SFT adaptation",
        "artifacts": {
            "kb_manifest": "kb/rules_manifest.json",
            "eval_manifest": "eval/eval_manifest.json",
            "sft_manifest": "sft/dataset_manifest.json",
            "system_prompt": "sft/system_prompt.md",
            "validator": "tools/validate_pack.py",
        },
        "counts": {
            "rule_cards": kb_manifest["total_count"],
            "eval_records": sum(item["count"] for item in eval_manifest["benchmarks"].values()),
            "sft_records": sft_manifest["split_counts"]["total"],
        },
        "notes": [
            "이 패키지는 원본 knowledge 데이터를 재구성한 export 결과다.",
            "모델 구매 후 벤더 포맷이 정해지면 이 패키지 기준으로 최종 변환한다.",
        ],
    }
    write_json(PACK / "manifest.json", manifest)


def write_pack_tools():
    source_validator = ROOT / "scripts/validate_pack.py"
    target_validator = PACK / "tools/validate_pack.py"
    target_validator.parent.mkdir(parents=True, exist_ok=True)
    target_validator.write_text(source_validator.read_text(encoding="utf-8"), encoding="utf-8")

    tools_readme = """# Tools

`validate_pack.py`
- `pack/` 산출물의 JSON / JSONL 구조와 count 일치를 검증한다.
- 사용:

```bash
python3 tools/validate_pack.py
```
"""
    write_text(PACK / "tools/README.md", tools_readme)


def main():
    if PACK.exists():
        shutil.rmtree(PACK)
    PACK.mkdir(parents=True, exist_ok=True)
    kb_manifest = build_rule_exports()
    eval_manifest = build_eval_exports()
    sft_manifest = build_sft_exports()
    write_pack_readme(kb_manifest, eval_manifest, sft_manifest)
    write_top_level_manifest(kb_manifest, eval_manifest, sft_manifest)
    write_pack_tools()
    print("pack_build=ok")
    print(f"rules={kb_manifest['total_count']}")
    print(
        "eval="
        f"{eval_manifest['benchmarks']['C']['count']}/"
        f"{eval_manifest['benchmarks']['C++']['count']}/"
        f"{eval_manifest['benchmarks']['Java']['count']}"
    )
    print(f"sft={sft_manifest['split_counts']['total']}")


if __name__ == "__main__":
    main()
