# 📚 프로젝트 명세서 및 문서 모음

이 폴더에는 **뭐냑? (AMApill)** 프로젝트의 상세 명세서 및 설계 문서가 포함되어 있습니다.

---

## 📋 목차

- [프로젝트 기획 및 명세](#-프로젝트-기획-및-명세)
- [아키텍처 및 설계](#%EF%B8%8F-아키텍처-및-설계)
- [개발 규칙](#-개발-규칙)
- [페르소나](#-페르소나)

---

## 📖 프로젝트 기획 및 명세

### [PROJECT_SPECIFICATION.md](./PROJECT_SPECIFICATION.md)
**전체 프로젝트 요구사항 및 기능 정의**

- 프로젝트 개요 및 목표
- 핵심 기능 상세 명세
- 기술 스택 선정 이유
- 법적/보안 고려사항
- 비즈니스 모델

### [MVP_DTO_SPECIFICATION.md](./MVP_DTO_SPECIFICATION.md)
**MVP 기능 우선순위 및 API 명세**

- MVP 1~3순위 기능 정의
- 40개 이상의 DTO 명세
- REST API 엔드포인트 정의
- Request/Response 스키마

### [CHAT_API_SPECIFICATION.md](./CHAT_API_SPECIFICATION.md)
**채팅 및 상담 기능 API 명세**

- 의사/AI 챗봇 상담 기능
- WebSocket 프로토콜 (STOMP)
- REST API 정의
- 메시지 포맷 및 이벤트 처리

### [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md)
**7주 개발 일정 및 마일스톤**

- 주차별 개발 계획
- 팀 역할 분담
- 마일스톤 및 체크포인트
- 리스크 관리 계획

---

## 🏗️ 아키텍처 및 설계

### [ARCHITECTURE.md](./ARCHITECTURE.md)
**시스템 아키텍처 및 기술 설계**

- 전체 시스템 구조 (Mermaid 다이어그램 9개)
- 마이크로서비스 아키텍처 설계
- 기술 스택 상세 설명
- 데이터 흐름 및 통신 방식

### [MICROSERVICES_SETUP.md](./MICROSERVICES_SETUP.md)
**마이크로서비스 설정 및 구성**

- 6개 마이크로서비스 구성
- MySQL/PostgreSQL 분리 전략
- Docker Compose 설정
- 서비스별 API 게이트웨이 라우팅

### [SRC_STRUCTURE.md](./SRC_STRUCTURE.md)
**소스 코드 구조 가이드**

- Frontend/Backend 디렉토리 구조
- SOLID 원칙 적용
- AOP 패턴 및 디자인 패턴
- 패키지 구조 및 명명 규칙

### [FRONTEND_COMPONENTS_SPECIFICATION.md](./FRONTEND_COMPONENTS_SPECIFICATION.md)
**프론트엔드 컴포넌트 정의서**

- 화면별 컴포넌트 트리 구조
- Props 명세 및 타입 정의
- API 연동 방식
- 라우팅 구조 및 네비게이션

---

## 📏 개발 규칙

### [CONVENTIONS.md](./CONVENTIONS.md)
**프로젝트 컨벤션 및 코딩 규칙**

- Git 브랜치 전략 (Git Flow)
- 커밋 메시지 규칙 (Conventional Commits)
- 코드 네이밍 규칙
  - React 컴포넌트 (PascalCase)
  - Java 클래스/메서드 (CamelCase)
  - 데이터베이스 (snake_case)
- 코드 리뷰 가이드라인

---

## 👥 페르소나

### [페르소나설정.md](./페르소나설정.md)
**사용자 페르소나 정의**

- 주 사용자 프로필 (시니어, 자녀)
- 사용 시나리오
- 사용자 니즈 및 페인 포인트
- UX/UI 설계 근거

---

## 📂 관련 폴더

이 문서들과 함께 참고할 추가 리소스:

- [`../diagrams/`](../diagrams/) - Mermaid 다이어그램 파일 (9개)
- [`../figma-exports/`](../figma-exports/) - Figma 와이어프레임 JSON
- [`../figma-plugin/`](../figma-plugin/) - Figma 플러그인 코드
- [`../profile/`](../profile/) - 조직 프로필

---

## 🔗 루트 가이드 문서

프로젝트 루트에 있는 빠른 시작 가이드:

- [README.md](../README.md) - 프로젝트 메인 소개
- [QUICKSTART.md](../QUICKSTART.md) - 빠른 시작 가이드
- [FIGMA_GUIDE.md](../FIGMA_GUIDE.md) - Figma 플러그인 설치 가이드
- [WIREFRAME_SCREENS.md](../WIREFRAME_SCREENS.md) - 와이어프레임 화면 설명
- [DB스킬.md](../DB스킬.md) - 데이터베이스 스키마 및 ERD
- [SECURITY_GUIDELINES.md](../SECURITY_GUIDELINES.md) - 보안 및 문서 작성 가이드라인

---

**최종 수정일**: 2025-11-12
**문서 관리**: 뭐냑? 개발팀
