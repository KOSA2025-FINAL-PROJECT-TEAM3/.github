# 🧩 마이크로서비스 구성 & 라우팅 (Dev 기준)

이 문서는 `.github` 조직 문서 기준으로, **실제 레포 코드/설정**(Gateway/Auth/Core + docker-compose)을 기반으로 현재 구성을 설명합니다.

관련 문서:
- 레포 분석 인덱스: [`documents/REPOSITORIES.md`](./REPOSITORIES.md)
- 전체 아키텍처: [`documents/ARCHITECTURE.md`](./ARCHITECTURE.md)

---

## 1) 서비스 구성(현재 구현)

| 구분 | 서비스 | 포트(로컬) | 핵심 책임 |
|---|---|---:|---|
| Entry | API Gateway (`spring-cloud-api-gateway`) | `8080` | 인증(JWT) + 라우팅 + 캐싱 + Circuit Breaker |
| Auth | Auth Service (`auth-service`) | `8081` | 로그인/회원가입, Kakao OAuth, JWT 발급/갱신, 사용자 프로필 |
| Core | Core Service (`spring-boot`) | `8082` | 가족/약/식단/OCR/알림/리포트/질병/채팅/Voice 등 도메인 |
| Infra | MySQL/Redis/Kafka/PostgreSQL (`docker-compose`) | - | DB/캐시/메시징/벡터스토어 |

> `docker-compose` 레포에는 “향후 서비스 분리”를 전제로 한 `family-service` 등 다수 서비스 정의가 포함되어 있습니다.  
> 현재 레포 구성(3개 백엔드 + docker-compose) 기준으로는 **Core(8082) 단일 도메인 서비스**가 “현 구현”입니다.

---

## 2) 외부 진입점과 프록시

로컬 개발에서는 다음 2가지 진입점을 모두 사용할 수 있습니다.

1) Gateway 직접 호출: `http://localhost:8080`  
2) Nginx(80) 경유 호출: `http://localhost`  

`docker-compose/nginx.conf` 기준으로:

- `/api/**` → `host.docker.internal:8080` (Gateway)
- `/ws/**` → `host.docker.internal:8080` (Gateway WebSocket)

---

## 3) Gateway 라우팅 규칙(Dev 프로필)

`spring-cloud-api-gateway/src/main/resources/application-dev.yaml` 기준:

- `/api/auth/**` → `http://localhost:8081` (Auth Service) + `StripPrefix=1`
- `/api/{family,family-chat,prescriptions,medications,diet,ocr,chat,search,disease,counsel,notifications,reports,voice}/**`
  → `http://localhost:8082` (Core Service) + `StripPrefix=1`
- `/ws/**` → `http://localhost:8082` (Core WebSocket) (StripPrefix 없음)
- SSE: `/api/notifications/subscribe`는 `response-timeout: 3600s`

Core 서비스는 내부적으로 `/family`, `/medications`, `/diet` 같은 경로를 사용하며, Gateway가 `/api`를 제거해서 전달합니다.

---

## 4) 인증/인가 방식(헤더 주입)

### 4.1 Gateway가 JWT를 검증한다

Gateway `GatewayJwtAuthenticationFilter`는 (인증 제외 경로를 제외하고) Access Token을 검증한 뒤, 내부 서비스로 다음 헤더를 주입합니다.

- `X-User-Id` (필수)
- `X-User-Email`
- `X-User-Name` (UTF-8 URL 인코딩)
- `X-User-Profile-Image` (UTF-8 URL 인코딩)
- `X-User-Role`, `X-Customer-Role`
- `X-Token-Subject`, `X-Token-Type`
- `X-Request-Id`

### 4.2 내부 서비스는 JWT를 파싱하지 않는다

- Core: `SecurityUtil`이 `X-User-*` 헤더로 사용자 컨텍스트를 구성
- Auth: `GatewayUserInjectionFilter`가 `X-User-Id`를 `@AuthenticationPrincipal`로 주입

> 이 구조의 장점: 내부 서비스 코드에서 JWT 파싱 로직 제거 → 구현 단순화/일관성 확보  
> 전제 조건: Gateway 앞단(또는 Ingress)에서 토큰 검증을 반드시 보장

---

## 5) 실시간 통신

### 5.1 WebSocket/STOMP

- 외부: `/ws/**` (Gateway를 통해 Core로 프록시)
- 채팅/실시간 상태 업데이트는 Core(WebSocket) + Kafka 연계를 사용

### 5.2 SSE (Notifications)

- 외부: `GET /api/notifications/subscribe?token=...`
- EventSource API 제약 때문에 토큰을 쿼리로 받을 수 있으며, **검증은 Gateway**가 수행합니다.

---

## 6) 로컬 개발 권장 플로우

1. `docker-compose`로 인프라만 실행(MySQL/PostgreSQL/Redis/Kafka/Nginx)
2. IDE에서 Gateway/Auth/Core를 각각 실행
3. 호출은 `http://localhost:8080/api/...` 또는 `http://localhost/api/...` 사용

빠른 시작: [`QUICKSTART.md`](../QUICKSTART.md)

---

## 7) 환경 변수(민감정보 제외)

문서에는 “키 이름”만 기록합니다.

- 공통: `JWT_SECRET`, `REDIS_*`, `KAFKA_*`
- Auth: `SPRING_DATASOURCE_*`, `SPRING_DATA_REDIS_*`, `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`, `KAKAO_REDIRECT_URI`
- Core: `OPENAI_API_KEY`, `GOOGLE_VISION_API_KEY`, S3 관련 키/버킷, 공공데이터 API 키 등
