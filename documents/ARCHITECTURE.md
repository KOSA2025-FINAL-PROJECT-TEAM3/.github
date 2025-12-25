# 🏗️ 시스템 아키텍처 (Dev 기준)

AMApill(뭐냑?)은 “가족 돌봄 네트워크 기반 약 관리 플랫폼”이며, Dev 기준으로 **Gateway + Auth + Core** 3개 백엔드 레포지토리와 `docker-compose` 인프라 레포지토리를 중심으로 구성됩니다.

---

## 1) 한눈에 보기

- 시스템 구성도: [`diagrams/01-system-architecture.mmd`](../diagrams/01-system-architecture.mmd)
- 주요 데이터 흐름: [`diagrams/02-data-flow.mmd`](../diagrams/02-data-flow.mmd)
- DB ERD(최신 v7.0): [`diagrams/07-database-erd-v7.mmd`](../diagrams/07-database-erd-v7.mmd)

---

## 2) 컴포넌트 책임

### 2.1 API Gateway (`spring-cloud-api-gateway`)

- 단일 진입점(`/api/**`, `/ws/**`)
- JWT(Access Token) 검증
- `X-User-*` 헤더 주입(내부 서비스는 JWT를 직접 파싱하지 않음)
- Redis 기반 GET 응답 캐싱(경로별 TTL)
- Circuit Breaker(Resilience4j)
- Kafka 이벤트 로깅(요청/응답/에러)

### 2.2 Auth Service (`auth-service`)

- 로그인/회원가입
- Kakao OAuth 로그인
- JWT 발급/갱신
- 사용자 프로필(`/users/me`)
- Refresh Token 저장(Redis)

### 2.3 Core Service (`spring-boot`)

Auth를 제외한 도메인을 단일 서비스로 제공(현 구현 기준):

- 가족/초대/알림 설정
- 처방전/약/스케줄/복용 로그/순응도
- 식단 로그/분석/경고
- OCR(동기 + 비동기 Job)
- 알림(SSE 구독/히스토리)
- 리포트(복약 순응도)
- 질병(관리/약 연관/PDF)
- 가족 채팅(REST + WebSocket/STOMP + Kafka)
- Voice(음성 명령 텍스트 처리)

### 2.4 인프라 (`docker-compose`)

- MySQL (도메인 트랜잭션 데이터)
- Redis (캐시/토큰/실시간 기능 일부)
- Kafka (이벤트 스트리밍)
- PostgreSQL(+pgvector) (벡터 스토어/AI 보안 용도)
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

Core는 `SecurityUtil`로 헤더를 해석하고, Auth는 `GatewayUserInjectionFilter`로 `@AuthenticationPrincipal`을 구성합니다.

> 주의: SSE는 EventSource 제약 때문에 `token` 쿼리 파라미터를 허용하지만, “검증” 자체는 Gateway에서 수행해야 합니다.

---

## 4) 실시간 통신

### 4.1 WebSocket/STOMP

- 외부 진입: `/ws/**` (Gateway를 통해 Core로 프록시)
- 가족 채팅/상태 동기화 등 실시간 기능에 사용
- Kafka 연계로 메시지 브로드캐스트/확장 가능 구조를 마련

### 4.2 SSE (Notifications)

- 외부 진입: `GET /api/notifications/subscribe?token=...`
- 장기 연결이므로 Gateway 라우트에 `response-timeout`을 길게 설정

---

## 5) 데이터 저장소 설계(Dev)

DB 스키마 근거는 `docker-compose/init-scripts`입니다.

- MySQL: `users`, `prescriptions`, `medications`, `family_*`, `diet_*`, `notifications` 등
- PostgreSQL(+pgvector): `vector_store`

자세한 내용:

- [`documents/DATABASE_SCHEMA_ANALYSIS.md`](./DATABASE_SCHEMA_ANALYSIS.md)

---

## 6) AI/보안(현 코드 기준)

Core 서비스에는 다음 성격의 기능이 포함됩니다.

- Spring AI(OpenAI) 기반 의도/답변 생성
- 입력 통제(LLM Guard): 도메인별 정책/길이 제한/캐시/벡터 기반 “스마트 가드” 등

문서에는 키/토큰의 실제 값을 기록하지 않습니다(환경 변수로 관리).

---

## 7) 버전/기술 스택(요약)

- Java: 21
- Spring Boot: 3.5.8 (Core/Gateway 기준)
- Spring Cloud: 2025.0.0 (Gateway)
- MySQL: 8.0
- Redis: 7
- Kafka: KRaft 모드
- PostgreSQL: 16 (+pgvector)

---

## 8) 개발자 온보딩

- 빠른 시작: [`QUICKSTART.md`](../QUICKSTART.md)
- 레포별 분석: [`documents/REPOSITORIES.md`](./REPOSITORIES.md)
- 라우팅/프로필: [`documents/MICROSERVICES_SETUP.md`](./MICROSERVICES_SETUP.md)
