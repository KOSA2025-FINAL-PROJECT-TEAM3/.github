# AMApill Frontend Project Structure

## 📐 Architecture Overview

프론트엔드 전용 프로젝트 구조입니다. React 19 + Vite + JSX 아키텍처를 사용합니다.

### 기술 스택
- **Framework**: React 19 (JSX only)
- **번들러**: Vite 5
- **상태 관리**: Zustand + React Query
- **스타일링**: MUI + Emotion (CSS 기반 테마)
- **HTTP 클라이언트**: Axios
- **실시간 통신**: STOMP WebSocket + SSE

---

## 📁 Frontend Structure (Front/src)

```
src/
├── main.jsx
├── App.jsx
├── assets/
├── constants/
├── core/
│   ├── config/              # API/환경/라우팅 설정
│   ├── hooks/               # 공통 훅
│   ├── interceptors/        # Axios 인터셉터
│   ├── routing/             # 라우팅 유틸
│   ├── services/api/        # API 클라이언트
│   └── utils/               # 로깅/헬퍼
├── devtools/
├── features/                # 도메인별 모듈
├── hooks/
├── pages/
│   ├── errors/
│   └── more/
├── shared/
│   ├── components/
│   │   ├── layout/
│   │   ├── mui/
│   │   └── toast/
│   └── stores/
├── styles/
│   ├── base.css
│   └── theme.js
├── types/
└── utils/
```

---

## 📦 API 클라이언트 목록 (`src/core/services/api`)

- `ApiClient.js`
- `httpClient.js`
- `authApiClient.js`
- `userApiClient.js`
- `familyApiClient.js`
- `familyChatApiClient.js`
- `publicInviteApiClient.js`
- `medicationApiClient.js`
- `medicationLogApiClient.js`
- `prescriptionApiClient.js`
- `dietApiClient.js`
- `diseaseApiClient.js`
- `searchApiClient.js`
- `ocrApiClient.js`
- `notificationApiClient.js`
- `notificationSettingsApiClient.js`
- `reportApiClient.js`
- `appointmentApiClient.js`
- `voiceApiClient.js`

---

## 🧩 Features 모듈(폴더 기준)

- `appointment`
- `auth`
- `chat`
- `dashboard`
- `diet`
- `disease`
- `family`
- `medication`
- `notification`
- `ocr`
- `places`
- `report`
- `search`
- `settings`
- `voice`

---

## 📝 File Naming Conventions

- **Components**: PascalCase + `.jsx`
- **Hooks**: `use` prefix + `.js`
- **Stores (Zustand)**: camelCase + `Store` suffix + `.js`
- **API Clients**: camelCase + `ApiClient` suffix + `.js`
- **Utils**: camelCase + `.js`

---

## 🚀 Key Takeaways

1. **Feature-based Modules**: 도메인별 모듈로 구조화
2. **Zustand + React Query**: 상태/서버 데이터 분리
3. **API Clients**: 기능별 API 클라이언트 분리
4. **Shared Components**: `shared/components`에서 재사용

