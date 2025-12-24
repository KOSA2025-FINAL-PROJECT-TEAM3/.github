# auth-service 분석

## 1) 책임(역할)

- 회원가입/로그인
- Kakao OAuth 로그인
- JWT 발급/갱신(Refresh Token 포함)
- 사용자 프로필 조회/수정/비활성화
- 로그아웃(Refresh Token 삭제 + 민감 API 보호를 위한 블랙리스트/필터 연계)
- (내부용) Kakao Token 조회 API 제공

## 2) 실행/포트

- 기본 포트: `8081`
- Health: `GET /actuator/health`

## 3) API 엔드포인트(핵심)

- `POST /auth/signup`
- `POST /auth/login`
- `POST /auth/kakao-login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/deeplink/resolve`

- `GET /users/me`
- `PUT /users/me`
- `DELETE /users/me`

- `GET /auth/kakao/token/{userId}`
- `GET /auth/kakao/token/{userId}/exists`

## 4) 인증 방식(구조적 특징)

- `GatewayUserInjectionFilter`가 `X-User-Id` 헤더를 읽어 `@AuthenticationPrincipal Long userId`로 주입합니다.
- 즉, **실 서비스에서는 Gateway가 JWT를 검증하고 헤더를 주입**해주는 것을 전제로 합니다.

> 주의: 현재 Gateway 라우팅에는 `/api/users/**`가 포함되어 있지 않으므로, “프로필 API를 Gateway로 노출할지” 여부는 설계 결정이 필요합니다.  
> (선택지) `spring-cloud-api-gateway`에 `/api/users/** → auth-service` 라우트 추가 또는 Nginx에서 `/users/**` 프록시 추가

## 5) 데이터 저장소

- MySQL(Init Scripts 기준): `users`, `kakao_tokens`
- Redis: Refresh Token 저장(구현 구조에 따라 Key/TTL)

## 6) 환경 변수(문서화 범위)

- MySQL 접속 정보(`SPRING_DATASOURCE_*`)
- Redis 접속 정보(`SPRING_DATA_REDIS_*`)
- `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`, `KAKAO_REDIRECT_URI`
- `JWT_SECRET`(발급/검증용)
