# 2026-05-13 pack bootstrap

## 목적
- 현재 `knowledge/` 원본을 모델 비의존 `pack/` 산출물로 한 번 더 정리
- 폐쇄망 모델 구매 전에도 RAG / eval / SFT 초안 구조를 고정
- 이후 벤더 포맷 요구가 생기면 `pack/`에서 마지막 변환만 하도록 설계

## 생성 범위
- `pack/kb/rules.jsonl`
- `pack/kb/rules_manifest.json`
- `pack/eval/benchmark_c.jsonl`
- `pack/eval/benchmark_cpp.jsonl`
- `pack/eval/benchmark_java.jsonl`
- `pack/eval/eval_manifest.json`
- `pack/sft/train.jsonl`
- `pack/sft/val.jsonl`
- `pack/sft/test.jsonl`
- `pack/sft/system_prompt.md`
- `pack/sft/dataset_manifest.json`
- `pack/tools/validate_pack.py`
- `pack/manifest.json`
- `pack/README.md`

## 설계 원칙
- source of truth는 계속 `knowledge/` 아래에 둔다.
- `pack/`은 반입/변환 직전 단계의 export 결과로 본다.
- 모델 스펙이 확정되면 `pack/`에서 벤더 전용 포맷으로 마지막 변환만 수행한다.

## 현재 한계
- SFT seed는 현재 C benchmark 12건만 포함
- C++/Java benchmark는 아직 0건
- classification/title/summary 일부는 `draft-unverified`
