# 🏗️ 시스템 아키텍처 (현재 코드 기준)

AMApill(뭐냑?)은 **Gateway + Auth + Core** 3개 백엔드와
`docker-compose` 기반 인프라, 그리고 `k8s` 매니페스트로 구성됩니다.

---

## 1) 한눈에 보기

- 시스템 구성도: [`diagrams/01-system-architecture.mmd`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/diagrams/01-system-architecture.mmd)
- 주요 데이터 흐름: [`diagrams/02-data-flow.mmd`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/diagrams/02-data-flow.mmd)
- DB ERD: [`diagrams/07-database-erd-current.mmd`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/diagrams/07-database-erd-current.mmd)

---

## 2) 컴포넌트 책임

### 2.1 API Gateway (`spring-cloud-api-gateway`)

- 단일 진입점(`/api/**`, `/ws/**`)
- JWT 검증 및 `X-User-*` 헤더 주입
- Redis GET 응답 캐싱
- Kafka 요청/응답 로깅
- Resilience4j Circuit Breaker

### 2.2 Auth Service (`auth-service`)

- 로그인/회원가입/카카오 로그인
- JWT 발급/갱신/로그아웃
- 사용자 프로필(`/auth/users/**`)
- Refresh Token 저장(Redis)

### 2.3 Core Service (`spring-boot`)

Auth를 제외한 도메인을 단일 서비스로 제공:

- 가족/초대/알림 설정
- 약/처방전/복용 로그/순응도
- 식단/경고
- OCR
- 알림(SSE)
- 리포트
- 질병
- 가족 채팅(REST + WebSocket/STOMP)
- Voice
- 병원 예약

### 2.4 인프라 (`docker-compose`)

- MySQL (도메인 트랜잭션 데이터)
- Redis (캐시/세션/실시간 기능 일부)
- Kafka (이벤트 스트리밍)
- PostgreSQL(+pgvector) (LLM Guard 벡터 스토어)
- Nginx (로컬 프록시: `/api`, `/ws` → Gateway)

---

## 3) 인증/인가 아키텍처(헤더 주입)

핵심 원칙:

1. Gateway가 JWT를 검증한다.
2. 내부 서비스는 `X-User-*` 헤더를 신뢰한다.

Gateway는 다음 헤더를 주입합니다(대표):

- `X-User-Id` (필수)
- `X-User-Email`, `X-User-Name`, `X-User-Profile-Image`
- `X-User-Role`, `X-Customer-Role`
- `X-Token-Subject`, `X-Token-Type`
- `X-Request-Id`

Core는 `SecurityUtil`로 헤더를 해석하고,
Auth는 `GatewayUserInjectionFilter`로 `@AuthenticationPrincipal`을 구성합니다.

> SSE는 EventSource 제약 때문에 `token` 쿼리 파라미터를 허용하지만,
> “검증” 자체는 Gateway에서 수행해야 합니다.

---

## 4) 실시간 통신

### 4.1 WebSocket/STOMP

- 외부 진입: `/ws/**` (Gateway → Core)
- Core의 STOMP 엔드포인트: `/ws`
- 주용도: 가족 채팅 및 상태 동기화

### 4.2 SSE (Notifications)

- 외부 진입: `GET /api/notifications/subscribe?token=...`
- 장기 연결을 위해 Gateway 라우트에 `response-timeout` 설정

---

## 5) 데이터 저장소 설계

DB 스키마 근거는 `docker-compose/init-scripts`입니다.

- MySQL: 도메인 트랜잭션 데이터
- PostgreSQL(+pgvector): LLM Guard 벡터 스토어

자세한 내용:
- [`documents/DATABASE_SCHEMA_ANALYSIS.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/DATABASE_SCHEMA_ANALYSIS.md)

---

## 6) 배포 구성 (K8s)

`k8s/` 매니페스트 기준:

- `applications`: `auth-service`, `spring-boot`
- `apigateway`: `spring-cloud-api-gateway`
- `database`: MySQL/PostgreSQL/Redis + Admin 도구
- `middleware`: Kafka
- `core`: ingress-nginx, cloudflared, local-path storage

---

## 7) 버전/기술 스택(요약)

- Java: 21
- Spring Boot: 3.5.8
- Spring Cloud: 2025.0.0
- Spring AI: 1.1.0
- MySQL: 8.0
- Redis: 7
- Kafka: 7.5 (KRaft)
- PostgreSQL(+pgvector): 16 (docker-compose), 15 (k8s)

---

## 8) 개발자 온보딩

- 빠른 시작: [`QUICKSTART.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/QUICKSTART.md)
- 레포별 분석: [`documents/REPOSITORIES.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/REPOSITORIES.md)
- 라우팅/프로필: [`documents/MICROSERVICES_SETUP.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/MICROSERVICES_SETUP.md)
