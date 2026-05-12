# 정규화된 C 규칙 카드 초안

이 폴더는 MISRA C 2012 기준 C 규칙 카드를 **내부망 LLM 반입용 1규칙 1파일 형식**으로 정리한 결과를 저장합니다.

## 상태

```text
validation_status = mixed-draft
rule_count = 158
directive_count = 17
expanded_draft_count = 12
placeholder_count = 163
```

의미:
- 전체 규칙/지시문 뼈대는 생성 완료
- 12개 규칙은 Gemini-Pro 초안을 기반으로 상세 필드까지 확장됨
- 나머지는 제목/분류/예제/매핑을 채워야 하는 placeholder 상태
- 실제 MISRA 라이선스 문서와 대조 전
- Sparrow export 실제 finding 명칭과 대조 전

즉, **교육/정리 초안**으로는 사용 가능하지만 **최종 학습 데이터 확정본**은 아닙니다.

## 현재 상세 확장된 규칙 12건

- Rule 9.1
- Rule 10.3
- Rule 11.1
- Rule 11.3
- Rule 14.3
- Rule 16.3
- Rule 16.4
- Rule 17.2
- Rule 18.1
- Rule 20.7
- Rule 20.9
- Rule 21.3

## 다음 검증 단계

1. MISRA 라이선스 문서와 rule title / classification 대조
2. Sparrow export와 `sparrow_mapping` 대조
3. 상세 확장 규칙을 12건에서 전수 규칙으로 확대
4. Reviewer benchmark JSONL 생성
5. 현업 검토 후 내부망 반입
