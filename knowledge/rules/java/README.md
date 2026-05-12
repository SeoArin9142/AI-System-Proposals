# 정규화된 Java 규칙 카드 구조

이 폴더는 **CERT Java** 기준 Java 규칙 카드를 **1규칙 1파일** 형식으로 저장합니다.

## 상태

```text
validation_status = mixed-draft
rule_count = 174
group_count = 19
expanded_draft_count = 10
```

의미:
- 공식 공개 CERT Java 규칙 목록 기준으로 전체 skeleton 생성 완료
- 각 규칙 파일에 rule_title과 group 정보가 반영됨
- 공개 risk summary 기반 severity는 반영했지만, localized summary와 예제는 아직 placeholder 상태
- 내부용 적응 과정에서 tool mapping과 현업 예제 보강이 필요

## 현재 기준

- 표준 기준: `CERT Java`
- source: SEI CERT Oracle Coding Standard for Java public rules site

## 다음 단계

1. Java 정적분석 도구 export와 mapping 정리
2. 현재 확장된 10건의 summary / example / fix_guidance 현업 검토
3. 현업 위반 예제 수집
4. Reviewer benchmark JSONL 생성
