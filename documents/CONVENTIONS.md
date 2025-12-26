# 🧭 개발 컨벤션 (코드 기준)

이 문서는 **현재 코드 구조에서 확인되는 패턴**을 정리한 최소 규칙입니다.
새 코드도 동일한 레이어링/경로 규칙을 따르는 것을 전제로 합니다.

---

## 1) 레포/모듈 구성

- `Front/` : React + Vite 프론트엔드
- `spring-boot/` : Core 서비스 (비즈니스 도메인)
- `auth-service/` : 인증 서비스
- `spring-cloud-api-gateway/` : API Gateway
- `docker-compose/` : 로컬 인프라
- `k8s/` : Kubernetes 매니페스트

---

## 2) Backend 패키지 레이어링 (spring-boot)

도메인별로 아래 레이어를 기본 구조로 사용합니다.

- `domain/<도메인>/api` : Controller (`@RestController`)
- `domain/<도메인>/application` : Service/DTO
- `domain/<도메인>/domain` : Entity/Model/Enum
- `domain/<도메인>/infrastructure` 또는 `domain/<도메인>/infra` : Persistence/외부 연동
- `global/` : 공통 설정, 보안, 예외, 로깅 등

예시:
- `com.amapill.backend.domain.chat.api.FamilyChatRestController`
- `com.amapill.backend.domain.chat.application.service.FamilyChatService`
- `spring-boot/src/main/resources/mappers/chat/ChatMessageMapper.xml`

---

## 3) DTO/Validation

- 요청 DTO는 `jakarta.validation`을 사용 (`@NotNull`, `@NotBlank`, `@Size` 등)
- Controller에서 `@Valid`로 검증 수행
- Lombok(`@Data`, `@Builder`, `@RequiredArgsConstructor`) 패턴을 유지

---

## 4) Persistence

- **JPA + MyBatis 병행**
  - JPA: 엔티티 기반 ORM
  - MyBatis: 동적 SQL/성능 민감 쿼리
- MyBatis XML 위치: `spring-boot/src/main/resources/mappers/**/*.xml`
- Mapper 인터페이스는 `*Mapper` 네이밍을 사용

---

## 5) API/실시간 통신 규칙

- REST는 컨트롤러 기준 Base Path를 사용
- Gateway는 `/api` 프리픽스를 제거(StripPrefix=1)
- WebSocket/STOMP
  - Endpoint: `/ws`
  - Send Prefix: `/app`
  - Subscribe Prefix: `/topic`

---

## 6) Frontend 구조/네이밍

- 경로 alias (Vite): `@`, `@features`, `@shared`, `@core` 등
- 도메인 기능은 `src/features/<domain>`에 위치
- 공통 UI/레이아웃은 `src/shared`
- API 클라이언트/환경 설정은 `src/core`

자세한 구조는 `readme/documents/SRC_STRUCTURE.md`를 기준으로 합니다.

---

## 7) 환경 설정 파일

- Front: `Front/.env` (템플릿: `Front/.env.template`)
- Core: `spring-boot/src/main/resources/application.properties`
- Auth: `auth-service/src/main/resources/application-*.yml`
- Gateway: `spring-cloud-api-gateway/src/main/resources/application-dev.yaml`
- Infra: `docker-compose/.env`

기존 설정은 환경 변수 기반 구성이므로, 신규 값도 동일한 패턴을 따릅니다.
