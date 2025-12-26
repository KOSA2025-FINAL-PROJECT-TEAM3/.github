# 뭐냑? 프론트엔드 컴포넌트 정의서 (현재 코드 기준)

> React 19 + Vite + JSX Architecture

---

## 🎯 개요

### 기술 스택
- **Framework**: React 19 (JSX only)
- **번들러**: Vite 5
- **상태 관리**: Zustand + React Query
- **스타일링**: MUI + Emotion
- **실시간 통신**: STOMP WebSocket + SSE
- **폼 관리**: React Hook Form + Zod
- **HTTP 클라이언트**: Axios

---

## 📂 프로젝트 구조

`readme/documents/SRC_STRUCTURE.md`의 구조 요약을 기준으로 합니다.

핵심 디렉토리:

- `src/core`: 환경 설정, API 클라이언트, 인터셉터, 라우팅 유틸
- `src/features`: 도메인별 페이지/컴포넌트
- `src/shared/components`: 공통 UI (layout, mui, toast)
- `src/styles`: base.css, theme.js

---

## 🧩 Feature 모듈(폴더 기준)

- `appointment`, `auth`, `chat`, `dashboard`, `diet`, `disease`, `family`,
  `medication`, `notification`, `ocr`, `places`, `report`, `search`, `settings`, `voice`

각 모듈은 `components/`, `pages/`, `hooks/`, `store/` 등의 하위 구조를 사용합니다.

---

## 🧱 공통 컴포넌트 라이브러리

`src/shared/components`:

- `layout/`: AppShell, MainLayout, Header, Navigation 등
- `mui/`: AppButton, AppDialog, RoundedCard 등 MUI 래퍼
- `toast/`: Toast, ToastContainer
- 공통 에러 처리: `ErrorBoundary`, `ErrorFallback`

---

## 🔄 상태 관리

- **Zustand**: 전역 상태 관리
- **React Query**: 서버 상태 및 캐싱

---

## 🔌 API 연동

- Axios 기반 `httpClient` 사용
- 환경 변수는 `src/core/config/environment.config.js`에서 관리
- 기본 API 베이스: `VITE_API_BASE_URL` 또는 `http://localhost:8080`

---

## 🧭 라우팅 구조

- 라우팅 정의: `src/core/config/routes.config.js`
- 보호 경로: `ROUTE_META.protected`
- WebSocket 엔드포인트: `/ws`

---

## ✅ 참고

세부 컴포넌트 트리/Props 명세는 코드가 단일 근거입니다.
문서에 없는 상세 구조는 해당 모듈의 `components/`와 `pages/`를 확인하세요.

