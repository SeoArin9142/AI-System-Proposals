# 정규화된 C++ 규칙 카드 구조

이 폴더는 **MISRA C++ 2008** 기준 C++ 규칙 카드를 **1규칙 1파일** 형식으로 저장합니다.

## 상태

```text
validation_status = mixed-draft
rule_count = 228
title_coverage_count = 216
expanded_draft_count = 3
```

의미:
- 공개 규칙 번호 체계 기준으로 전체 skeleton 생성 완료
- 216건은 공개 coverage 페이지에서 rule_title까지 확보
- 나머지는 제목/분류/예제/매핑을 채워야 하는 placeholder 상태
- classification, localized summary, Sparrow 매핑은 아직 검증 전

## 현재 기준

- 표준 기준: `MISRA C++ 2008`
- source: Klocwork 공개 checker map + Cppcheck 공개 rule coverage page

## 다음 단계

1. 라이선스 허용 범위 내 rule title / classification 검증
2. 현업 C++ 위반 예제 수집
3. Sparrow 또는 대응 정적분석 export와 mapping 정리
4. Reviewer benchmark JSONL 생성
