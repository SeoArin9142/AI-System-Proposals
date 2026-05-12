# C Reviewer Benchmark 구조

이 폴더는 C 규칙 카드와 연결되는 Reviewer benchmark JSONL을 저장하기 위한 위치입니다.

## 상태

```text
validation_status = structure-ready
benchmark_count = 0
```

## 권장 내용

- finding 1건당 입력 1건
- `primary_rule` 1개
- `decision` 포함
- `explanation_ko`와 `fix_guidance` 포함

## 다음 단계

1. 현재 상세 확장된 C 규칙 카드 12건 기준으로 benchmark 12건 생성
2. 이후 전수 규칙으로 benchmark 범위 확대
3. Sparrow export와 매칭 검증
4. 현업 검토 후 확정본 분리
