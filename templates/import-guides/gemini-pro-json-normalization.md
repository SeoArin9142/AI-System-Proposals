# Gemini-Pro JSON 정규화 가이드

Gemini-Pro가 만든 MISRA/Sparrow JSON은 **원본 입력(raw intake)** 으로는 사용할 수 있습니다.  
다만 내부망 LLM용 규칙 카드와 Reviewer benchmark로 쓰려면 아래 형태로 정규화하는 것이 맞습니다.

## 1. 현재 JSON이 좋은 점

- `rule_id`가 명확함
- `sparrow_id`가 같이 붙어 있음
- `violation_sample` / `compliant_sample`이 있어 예제셋 변환이 쉬움
- `technical_context`가 있어 규칙의 위험 배경 설명으로 활용 가능

## 2. 바로 쓰기 어려운 점

- 여러 규칙이 배열 하나에 묶여 있어 **규칙 카드 1파일 1규칙** 구조로 분리 필요
- `refactoring_guide`가 문자열 1개라서 **단계 배열**로 쪼개는 것이 좋음
- `rule_group`는 있으나 `classification`, `severity`, `source_reference`가 없음
- 도메인 예시가 방산/전술 맥락에 치우쳐 있어 범용 교육셋으로는 일부 일반화 필요
- `sparrow_id` 실제 명칭이 현업 export와 일치하는지 검증 필요

## 3. 필드 매핑

| Gemini-Pro JSON | 내부 템플릿 필드 | 처리 방식 |
|---|---|---|
| `language` | `language` | 그대로 사용 |
| `rule_id` | `rule_id` | 그대로 사용 |
| `rule_group` | `rule_group` | 그대로 사용 |
| `technical_context` | `intent_ko`, `domain_context_ko` | 위험 설명과 적용 맥락으로 분리 권장 |
| `sparrow_id` | `sparrow_mapping` | 이름만 변경 |
| `implementation.violation_sample` | `noncompliant_example` | 그대로 사용 |
| `implementation.compliant_sample` | `compliant_example` | 그대로 사용 |
| `implementation.refactoring_guide` | `fix_guidance` | 줄바꿈/번호 기준 배열로 분리 |

## 4. 추가로 채워야 하는 필드

- `standard_family`
- `rule_title`
- `classification`
- `severity`
- `summary_ko`
- `review_checklist`
- `keywords`
- `source_reference`
- `confidentiality`

## 5. 정규화 예시

### 입력 예시

```json
{
  "language": "C",
  "rule_group": "Switch Statements",
  "rule_id": "MISRA-C-2012-Rule-16.4",
  "sparrow_id": ["MISSING_DEFAULT_CASE"],
  "technical_context": "알 수 없는 상태 코드가 들어올 수 있으므로 default가 필요하다.",
  "implementation": {
    "violation_sample": "switch (state) { case A: ... }",
    "compliant_sample": "switch (state) { case A: ... default: break; }",
    "refactoring_guide": "1. default 누락 위치 확인\\n2. default 삽입\\n3. break 추가"
  }
}
```

### 출력 예시

```json
{
  "language": "C",
  "standard_family": "MISRA C 2012",
  "rule_id": "MISRA-C-2012-Rule-16.4",
  "rule_group": "Switch Statements",
  "rule_title": "Every switch statement shall have a default label",
  "classification": "Required",
  "severity": "high",
  "summary_ko": "모든 switch 문은 default 라벨을 가져야 한다.",
  "intent_ko": "예상치 못한 상태값 유입 시 안전한 종착지와 방어 로직이 필요하다.",
  "domain_context_ko": "통신 상태 코드, 장비 상태값, 메시지 타입 분기 처리에 직접 연결된다.",
  "review_checklist": [
    "switch 끝에 default 라벨이 있는가",
    "default에서 안전한 종료 또는 로그 처리가 있는가"
  ],
  "common_violation_patterns": [
    "enum 분기에서 일부 값만 처리",
    "알 수 없는 상태값 방어 로직 누락"
  ],
  "noncompliant_example": "switch (state) { case A: ... }",
  "compliant_example": "switch (state) { case A: ... default: break; }",
  "fix_guidance": [
    "default 누락 위치를 확인한다.",
    "default 라벨을 추가한다.",
    "default 내부에 안전한 종료 로직과 break를 추가한다."
  ],
  "sparrow_mapping": [
    "MISSING_DEFAULT_CASE"
  ],
  "keywords": [
    "switch",
    "default",
    "state-machine"
  ],
  "source_reference": "internal summary based on licensed material",
  "confidentiality": "internal",
  "notes": "원문 전체 복사 금지"
}
```

## 6. 반영 가능 여부 판단

결론:

```text
가능함
단, 그대로 쓰지 않고 정규화 후 반영해야 함
```

가장 좋은 흐름:

1. Gemini-Pro JSON을 raw 입력으로 보관
2. 규칙 카드 1파일 1규칙으로 분리
3. `sparrow_mapping` 실데이터와 대조
4. Reviewer benchmark JSONL 생성
5. 현업 검토 후 내부망 반입
