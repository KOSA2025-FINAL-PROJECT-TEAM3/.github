# spring-cloud-api-gateway 분석

## 1) 책임(역할)

- **단일 진입점**: `/api/**` REST, `/ws/**` WebSocket을 백엔드로 라우팅
- **JWT 인증**: Access Token 검증 후 `X-User-*`, `X-Token-*` 헤더 주입
- **응답 캐싱**: Redis 기반 GET 응답 본문 캐싱(경로별 TTL)
- **장애 격리**: Resilience4j Circuit Breaker 설정(서비스별 정책)
- **요청/응답 이벤트**: Kafka 기반 로깅(필터/이벤트 생산자)

## 2) 실행/포트

- 기본 포트: `8080`
- Health: `GET /actuator/health`

## 3) 라우팅 규칙(중요)

Gateway 라우팅은 프로필별로 정의됩니다.

- `src/main/resources/application-dev.yaml` (로컬 개발):  
  - `/api/auth/**` → `http://localhost:8081` (StripPrefix=1)
  - 그 외 대부분 `/api/*` → `http://localhost:8082` (StripPrefix=1)
  - `/ws/**` → `http://localhost:8082` (WebSocket, StripPrefix 없음)
  - SSE: `/api/notifications/subscribe`는 `response-timeout: 3600s`

- `src/main/resources/application-docker.yaml` (도커 환경):  
  - `/api/auth/**` → `http://auth-service:8081`
  - `/api/{family,medications,diet,ocr,chat,search,disease,counsel,notifications,reports}/**` → 각 서비스로 분리 라우팅

> 현재 레포 구성(3개 서비스 + docker-compose) 기준으로는 **dev 프로필(8082 단일 Core 라우팅)**이 “현 구현”과 가장 일치합니다.  
> docker 프로필은 **향후 서비스 분리(예: family-service 등)**를 전제로 합니다.

## 4) 인증 흐름(요약)

- GlobalFilter(`GatewayJwtAuthenticationFilter`)가 다음을 수행:
  - 인증 제외 경로를 제외하고 JWT 검증
  - 성공 시 `X-User-Id`, `X-User-Email`, `X-User-Name(UTF-8 인코딩)`, `X-User-Role`, `X-Customer-Role` 등 헤더 주입
  - SSE는 EventSource 제약 때문에 `token` 쿼리 파라미터도 허용

내부 서비스는 `SecurityUtil`(Core) 또는 `GatewayUserInjectionFilter`(Auth)가 헤더를 신뢰해 사용자 컨텍스트를 구성합니다.

## 5) 환경 변수(문서화 범위)

민감 값은 문서에 기록하지 않습니다. “어떤 키가 필요한지”만 정리합니다.

- `JWT_SECRET` (Base64): Gateway JWT 서명키
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- `KAFKA_BOOTSTRAP` 또는 `SPRING_KAFKA_BOOTSTRAP_SERVERS`

