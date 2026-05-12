# 규칙/예제 템플릿 안내

향후 내부망 LLM에 넣을 규칙 데이터와 Reviewer 평가셋은 아래 3종으로 나눠 관리하는 것을 권장합니다.

- **규칙 카드 JSON**: 규칙 요약, 체크리스트, 위반 패턴, 수정 가이드
- **리뷰 예제 JSONL**: Reviewer 평가셋, few-shot 예제, benchmark
- **Markdown 가이드**: 사람이 읽는 교육자료와 작성 규칙

## 폴더 구조

```text
templates/
  rules/
    c/
    cpp/
    java/
  examples/
```

## 사용 원칙

1. MISRA/CERT/사내 규칙 원문 전체를 복사하지 말고 **요약/패러프레이즈 + rule_id/reference** 방식으로 저장합니다.
2. 코드 예제는 실제 고객/프로젝트 코드가 아니라 **합성 예제** 또는 익명화된 예제를 사용합니다.
3. Sparrow finding과의 연결은 `sparrow_mapping` 필드에 넣습니다.
4. Reviewer 출력 검증용 데이터는 JSONL로 쌓습니다.

## 언어별 템플릿

- [C 규칙 카드 템플릿](rules/c/rule-card.template.json)
- [C++ 규칙 카드 템플릿](rules/cpp/rule-card.template.json)
- [Java 규칙 카드 템플릿](rules/java/rule-card.template.json)

## 예제 템플릿

- [C Reviewer benchmark 템플릿](examples/c-reviewer-benchmark.template.jsonl)
- [C++ Reviewer benchmark 템플릿](examples/cpp-reviewer-benchmark.template.jsonl)
- [Java Reviewer benchmark 템플릿](examples/java-reviewer-benchmark.template.jsonl)

## 권장 작성 순서

1. 규칙 카드 JSON 작성
2. Sparrow finding -> rule 매핑 정리
3. Reviewer benchmark JSONL 작성
4. 내부망 반입 전 검토

## 권장 표준 계열

- C: MISRA C, CERT C, 사내 C 코딩 규칙
- C++: MISRA C++, AUTOSAR C++14, CERT C++
- Java: CERT Java, 사내 Java 보안/품질 규칙
