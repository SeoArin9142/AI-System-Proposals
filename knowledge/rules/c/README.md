# 정규화된 C 규칙 카드 초안

이 폴더는 Gemini-Pro로 생성된 MISRA C 초안을 **내부망 LLM 반입용 규칙 카드 형식**으로 정규화한 결과를 저장합니다.

## 상태

```text
validation_status = draft-unverified
```

의미:
- 구조화와 분할은 완료
- 실제 MISRA 라이선스 문서와 대조 전
- Sparrow export 실제 finding 명칭과 대조 전

즉, **교육/정리 초안**으로는 사용 가능하지만 **최종 학습 데이터 확정본**은 아닙니다.

## 포함 규칙

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
3. Reviewer benchmark JSONL 생성
4. 현업 검토 후 내부망 반입
