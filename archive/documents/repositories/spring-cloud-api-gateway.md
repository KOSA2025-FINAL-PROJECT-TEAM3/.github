# spring-cloud-api-gateway 분석

## 1) 책임(역할)

- 단일 진입점: `/api/**` REST, `/ws/**` WebSocket
- JWT 검증 후 `X-User-*`, `X-Token-*` 헤더 주입
- Redis 기반 GET 응답 캐싱
- Kafka 요청/응답 로깅
- Resilience4j Circuit Breaker 설정

## 2) 실행/포트

- 기본 포트: `8080`
- Health: `GET /actuator/health`

## 3) 라우팅 규칙

### 개발(`application-dev.yaml`)

- `/api/auth/**` → `http://localhost:8081` (Auth)
- `/api/appointments/**` → `http://localhost:8082`
- `/api/family/**` → `http://localhost:8082`
- `/api/family-chat/**` → `http://localhost:8082`
- `/api/prescriptions/**` → `http://localhost:8082`
- `/api/medications/**` → `http://localhost:8082`
- `/api/diet/**` → `http://localhost:8082`
- `/api/ocr/**` → `http://localhost:8082`
- `/api/chat/**` → `http://localhost:8082`
- `/api/search/**` → `http://localhost:8082`
- `/api/disease/**` → `http://localhost:8082`
- `/api/counsel/**` → `http://localhost:8082`
- `/api/notifications/**` → `http://localhost:8082`
- `/api/reports/**` → `http://localhost:8082`
- `/api/voice/**` → `http://localhost:8082`
- `/ws/**` → `http://localhost:8082` (WebSocket)
- SSE: `/api/notifications/subscribe`는 `response-timeout: 3600s`

### 운영(`application-prod.yaml`)

- K8s 서비스 DNS로 분리 라우팅(예: `auth-service`, `family-service`, `medication-service` 등)

### K8s 배포(`k8s/applications/spring-cloud-api-gateway/configmap.yaml`)

- `apigateway` 네임스페이스 사용
- `/api/auth/**` → `auth-service.applications.svc.cluster.local:8081`
- `/api/**` → `spring-boot.applications.svc.cluster.local:8082`
- `/ws/**` → `ws://spring-boot.applications.svc.cluster.local:8082`

## 4) 인증 흐름(요약)

`GatewayJwtAuthenticationFilter`가 다음을 수행합니다.

- 인증 제외 경로:
  - `/ws`
  - `/api/auth/login`, `/api/auth/signup`, `/api/auth/kakao-login`, `/api/auth/refresh`
  - `/api/auth/deeplink/resolve`
  - `/api/auth/users/reactivate`
  - `/api/family/public/invites`
  - `/actuator/health`, `/health`
- SSE 구독(`/api/notifications/subscribe`)은 쿼리 파라미터 `token` 허용
- 성공 시 헤더 주입:
  - `X-User-Id`, `X-User-Email`, `X-User-Name`, `X-User-Profile-Image`
  - `X-User-Role`, `X-Customer-Role`
  - `X-Token-Subject`, `X-Token-Type`, `X-Request-Id`

## 5) 글로벌 필터(코드 기준)

- `GatewayJwtAuthenticationFilter` (order: -10)
- `KafkaLoggingFilter` (order: 0)
- `CacheableResponseFilter` (order: 1)

GET 응답 캐시는 Redis에 저장되며, 경로에 따라 TTL이 다르게 적용됩니다.

## 6) 환경 변수(문서화 범위)

- JWT: `JWT_SECRET`
- Redis: `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- Kafka: `KAFKA_BOOTSTRAP` 또는 `SPRING_KAFKA_BOOTSTRAP_SERVERS`

