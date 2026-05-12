# 2026-05-13 규칙 구조화 작업 로그

## 작업 순서

1. 전체 규칙 리스트 추가
2. C Reviewer benchmark 12건 생성
3. C 규칙 12건 checklist / fix_guidance 보강
4. C++ / Java 우선 규칙 상세 확장

## 진행 기록

- 00:39 기준 요청 확인: 작업 순서와 중간 보고를 남기기로 결정
- 00:40~00:44: 기존 구조화 결과 재확인 (C 158+17 / C++ 228 / Java 174)
- 00:45: `knowledge/rule-catalog.md` 생성
- 00:46: `knowledge/examples/c/reviewer-benchmark.v1.jsonl` 12건 생성
- 00:47: C 규칙 12건 review_checklist / fix_guidance 단계화 보강
- 00:48: C++ 우선 규칙 3건(0-1-1, 0-1-2, 0-1-3) 상세 확장
- 00:49: Java 우선 규칙 3건(EXP00-J, NUM00-J, ERR00-J) 상세 확장
- 00:50: examples/rules README 및 index 동기화
- 00:51~00:54: JSON/JSONL 파싱, 규칙 수, benchmark 수 재검증

## 결과 요약

- 전체 규칙 카탈로그 추가 완료
- C benchmark 12건 생성 완료
- C 규칙 12건 보강 완료
- C++/Java 우선 규칙 상세화 완료

## 검증 메모

- `git diff --check` 통과
- C 규칙 수: 158 / Directive 수: 17
- C benchmark 수: 12
- C++ 규칙 수: 228 / 상세 확장 3건
- Java 규칙 수: 174 / 상세 확장 3건
- JSON/JSONL 파싱 통과

## 후속 작업 후보

- C benchmark를 12건에서 전수 규칙 기준으로 확대
- C++ 상세 확장 범위를 우선순위 3건에서 추가 확대
- Java 상세 확장 범위를 우선순위 3건에서 추가 확대
- Sparrow export 연동 후 mapping 검증
