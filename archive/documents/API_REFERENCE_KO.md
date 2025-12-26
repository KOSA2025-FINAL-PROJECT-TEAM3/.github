# 📘 API Reference (현재 코드 기준)

> 이 문서는 **코드에 존재하는 라우트(베이스 경로)**를 정리한 요약본입니다.
> 상세 Request/Response는 Core Swagger(`/swagger-ui.html`)를 기준으로 합니다.

---

## 1) 공통 진입점

- Gateway: `http://localhost:8080`
- Nginx(로컬): `http://localhost`

Gateway는 `/api/**` 요청을 내부 서비스로 라우팅하며 `/api`를 제거합니다.
SSE 구독은 EventSource 제약으로 `token` 쿼리 파라미터를 허용합니다.

---

## 2) Auth Service (`auth-service`)

**Base**: `/auth` (Gateway 경유 시 `/api/auth/**`)

### AuthController
- `POST /auth/login`
- `POST /auth/signup`
- `POST /auth/kakao-login`
- `POST /auth/select-role`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/deeplink/resolve`
- `POST /auth/users/reactivate`

### UserController (`/auth/users`)
- `GET /auth/users/me`
- `PUT /auth/users/me`
- `POST /auth/users/me/image` (multipart)
- `DELETE /auth/users/me`

### KakaoTokenController (`/auth/kakao`)
- `GET /auth/kakao/token/{userId}`
- `GET /auth/kakao/token/{userId}/exists`

---

## 3) Core Service (`spring-boot`)

**Base**: Gateway 경유 시 `/api/**` → Core 내부 `/**`

### 주요 베이스 경로

- `/family`
- `/family/invites`
- `/family/public/invites`
- `/family/{familyGroupId}/members/{targetUserId}/notification-settings`
- `/medications`
- `/medications/logs`
- `/prescriptions`
- `/adherence`
- `/diet`
- `/disease`
- `/medications/search/symptoms`
- `/ocr`
- `/notifications`
- `/notifications/settings`
- `/notifications/subscribe` (SSE)
- `/reports`
- `/family-chat`
- `/appointments`
- `/voice`
- `/admin/abuse` (내부용)

### WebSocket/STOMP

- WebSocket 엔드포인트: `/ws`
- STOMP Prefix: `/app`, `/topic`

---

## 4) 상세 API 확인 방법

- Core Swagger: `GET /swagger-ui.html`
- OpenAPI: `GET /v3/api-docs`

