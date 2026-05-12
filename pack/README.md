# Pack

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
- rules total: 577
- eval C/C++/Java: 12/0/0
- sft total: 12

재생성:
```bash
python3 scripts/build_pack.py
python3 scripts/validate_pack.py
```

주의:
- 현재 데이터는 `draft-unverified` 성격이 포함됩니다.
- C benchmark만 SFT seed로 변환되어 있습니다.
- 실제 폐쇄망 모델 반입 시 벤더 포맷, tokenizer, role schema 요구사항에 맞는 마지막 변환은 별도로 수행해야 합니다.
