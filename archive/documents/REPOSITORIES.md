# 🗂️ 레포지토리별 분석 (현재 코드 기준)

이 문서는 **실제 코드/설정**을 기준으로 “무엇이 구현되어 있고, 어떻게 연결되는지”를 요약합니다.
상세 분석은 아래 개별 문서를 참고하세요.

## 대상 레포지토리

| 레포지토리 | 역할 | 기본 포트(로컬) | 비고 |
|---|---|---:|---|
| `Front` | Web SPA (React 19 + Vite) | `5173` | `/api`, `/ws`를 Gateway로 프록시 가능 |
| `spring-cloud-api-gateway` | 단일 진입점(라우팅/인증/캐싱/CB) | `8080` | `/api/**`, `/ws/**` 처리 |
| `auth-service` | 인증/인가, JWT 발급/갱신, 프로필 | `8081` | `/auth/**`, `/auth/users/**` |
| `spring-boot` | Core 서비스(도메인 통합) | `8082` | Swagger 제공 |
| `docker-compose` | 로컬 인프라 + 선택 서비스 | - | DB init scripts 포함 |
| `k8s` | K8s 매니페스트 | - | 클러스터 배포 리소스 |

## 개별 분석 문서

- [spring-cloud-api-gateway](./repositories/spring-cloud-api-gateway.md)
- [auth-service](./repositories/auth-service.md)
- [spring-boot(Core)](./repositories/spring-boot-core.md)
- [docker-compose](./repositories/docker-compose.md)
- [k8s](./repositories/k8s-manifests.md)

## 백엔드 서비스 요약

| 서비스 | 레포지토리 | 로컬 포트 | 설명 |
|---|---|---:|---|
| API Gateway | `spring-cloud-api-gateway` | `8080` | 단일 진입점, JWT 검증, 라우팅/캐싱 |
| Auth Service | `auth-service` | `8081` | 인증/인가, JWT 발급/갱신, 프로필 |
| Core Service | `spring-boot` | `8082` | 가족/약/식단/OCR/알림/리포트 등 |

## 레포 구조 요약

| 레포지토리 | 주요 디렉토리 | 비고 |
|---|---|---|
| `spring-cloud-api-gateway` | `src`, `gradle`, `Dockerfile` | 라우팅/인증 필터 및 설정 |
| `auth-service` | `src`, `docker`, `k8s`, `Dockerfile` | 인증/프로필 도메인 |
| `spring-boot` | `src`, `docs`, `references`, `Dockerfile` | Core 비즈니스 도메인 |
| `docker-compose` | `docker-compose.yml`, `init-scripts`, `nginx.conf` | 로컬 인프라 구성 |
| `k8s` | `applications`, `core`, `database`, `middleware` | 클러스터 배포 리소스 |

## 현재 아키텍처 한줄 요약

- **Client(Front) → (Nginx) → API Gateway → (Auth/Core) → DB/Redis/Kafka**
- Gateway가 **JWT(Access Token) 검증** 후 `X-User-*` 헤더를 주입하고,
  내부 서비스는 JWT를 직접 파싱하지 않는 구조를 사용합니다.

