# AI System Proposals

사내 AI 개발지원 시스템 구축 검토 문서를 별도 공유하기 위한 문서 전용 저장소입니다.

## 구성

### 문서
- [폐쇄망 AI 개발지원 시스템 구축 검토안](docs/internal-closed-network-ai-system.md)
- [외부망 연계 AI 개발지원 시스템 구축 검토안](docs/external-connected-ai-system.md)

### 발표자료
- [폐쇄망 PPT](presentations/issue-170-internal-ai-system-proposal.pptx)
- [폐쇄망 Word](presentations/issue-170-internal-ai-system-proposal.docx)
- [외부망 PPT](presentations/issue-171-external-ai-system-proposal.pptx)
- [외부망 Word](presentations/issue-171-external-ai-system-proposal.docx)

## 문서 요약

### 1. 폐쇄망 구축안
- 기존 Git/Jenkins 재사용
- 중간형 GPU 서버 1대 기준
- Owner / Reviewer / Orchestrator 구조
- 완전 폐쇄망에서는 오픈소스 로컬 모델 + RAG가 현실적
- 첫 유즈케이스는 Sparrow / MISRA / 6016F 기반 Reviewer 권장

### 2. 외부망 연계 구축안
- 내부 Git/Jenkins 유지
- Claude / GPT / Gemini 같은 관리형 모델 활용 가능
- 폐쇄망형보다 현재 상용 AI 협업 구조에 더 가깝게 구축 가능
- 다만 외부 전송 범위, 비용, 서비스 의존성 관리 필요

## 참고

- 본 저장소는 제안서와 발표자료 공유 목적입니다.
- 원본 검토 과정은 별도 작업 저장소에서 진행되었습니다.
