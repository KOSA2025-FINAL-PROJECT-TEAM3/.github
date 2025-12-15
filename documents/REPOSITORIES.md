# 🗂️ 레포지토리별 분석 (Dev 기준)

이 문서는 **실제 레포지토리 코드/설정**을 기준으로 “현재 무엇이 구현되어 있고, 어떻게 연결되는지”를 빠르게 파악하기 위한 요약본입니다.  
세부 분석은 아래 개별 문서를 참고하세요.

## 대상 레포지토리

| 레포지토리 | 역할 | 기본 포트(로컬) | 비고 |
|---|---|---:|---|
| `Front` | Web SPA (React 19 + Vite) | `5173` | `/api`, `/ws`를 Gateway로 프록시 |
| `spring-cloud-api-gateway` | 단일 진입점(라우팅/인증/캐싱/CB) | `8080` | `/api/**`, `/ws/**` 처리 |
| `auth-service` | 인증/인가, JWT 발급/갱신, 사용자 프로필 | `8081` | `/auth/**`, `/users/**` |
| `spring-boot` | Core 서비스(가족/약/식단/OCR/알림/리포트/질병/채팅/Voice) | `8082` | Swagger 제공 |
| `docker-compose` | 로컬 인프라(MySQL/Redis/Kafka 등) + 선택 서비스 | - | DB init scripts 포함 |

## 개별 분석 문서

- [spring-cloud-api-gateway](./repositories/spring-cloud-api-gateway.md)
- [auth-service](./repositories/auth-service.md)
- [spring-boot(Core)](./repositories/spring-boot-core.md)
- [docker-compose](./repositories/docker-compose.md)

## 현재 아키텍처 한줄 요약

- **Client(Front) → (Nginx) → API Gateway → (Auth Service/Core Service) → DB/Redis/Kafka**  
- Gateway가 **JWT(Access Token) 검증** 후 `X-User-*` 헤더를 주입하고, 내부 서비스는 JWT를 직접 파싱하지 않는 구조를 사용합니다.
