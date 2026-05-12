# C Reviewer Benchmark 구조

이 폴더는 C 규칙 카드와 연결되는 Reviewer benchmark JSONL을 저장하기 위한 위치입니다.

## 상태

```text
validation_status = mixed-draft
benchmark_count = 12
standard_family = MISRA C 2012
```

## 권장 내용

- finding 1건당 입력 1건
- `primary_rule` 1개
- `decision` 포함
- `explanation_ko`와 `fix_guidance` 포함

## 다음 단계

1. 현재 benchmark 12건의 explanation/fix_guidance 현업 검증
2. 이후 전수 규칙으로 benchmark 범위 확대
3. Sparrow export와 매칭 검증
4. 현업 검토 후 확정본 분리

## 현재 생성 파일

- `reviewer-benchmark.v1.jsonl` (12건)
