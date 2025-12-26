# auth-service 분석

## 1) 책임(역할)

- 회원가입/로그인/카카오 로그인
- JWT 발급/갱신/로그아웃
- 역할 선택(고객 역할)
- 딥링크 토큰 → 세션 토큰 전환
- 계정 재활성화
- 내 프로필 조회/수정/이미지 업로드/비활성화
- (내부용) 카카오 토큰 조회 API

## 2) 실행/포트

- 기본 포트: `8081` (`server.port`)
- Health: `GET /actuator/health`

## 3) API 엔드포인트(코드 기준)

### AuthController (`/auth`)
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

> `KakaoTokenController`는 Gateway 경유 호출을 위해 `/api/auth/kakao/**` 경로도 허용합니다.

## 4) 인증 방식(헤더 주입)

- `GatewayUserInjectionFilter`가 `X-User-Id` 헤더를 읽어 인증 주체를 구성합니다.
- JWT 검증은 **Gateway 단에서 수행**하는 것을 전제로 합니다.
- `JwtAuthenticationFilter`는 현재 SecurityConfig에서 비활성화되어 있습니다.

## 5) 데이터 저장소

- MySQL: JPA 사용 (`spring-boot-starter-data-jpa`)
- Redis: Refresh Token 저장 등 (`spring-boot-starter-data-redis`)
- Kafka: 의존성 포함(이벤트/로깅 목적)

## 6) 환경 변수(문서화 범위)

민감 값은 기록하지 않고 **키 이름만** 정리합니다.

- MySQL: `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`
- Redis: `SPRING_DATA_REDIS_HOST`, `SPRING_DATA_REDIS_PORT`, `SPRING_DATA_REDIS_PASSWORD`
- JWT: `JWT_SECRET`
- Kakao: `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`, `KAKAO_REDIRECT_URI`
- AWS S3: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_S3_BUCKET`
- Kafka: `SPRING_KAFKA_BOOTSTRAP_SERVERS` (환경에 따라 사용)

