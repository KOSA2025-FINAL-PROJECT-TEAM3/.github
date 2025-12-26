# spring-boot(Core) 분석

## 1) 책임(역할)

Auth를 제외한 **대부분의 비즈니스 도메인**을 단일 Spring Boot 서비스로 제공합니다.
코드 기준으로 다음 도메인 패키지가 존재합니다.

- appointment, chat, diet, disease, family, interaction, medication, notification,
  ocr, report, voice, security

## 2) 실행/포트

- 기본 포트: `8082`
- Swagger UI: `GET /swagger-ui.html`
- OpenAPI: `GET /v3/api-docs`
- Health: `GET /actuator/health`

## 3) API 베이스 경로(컨트롤러 기준)

Gateway가 `StripPrefix=1`로 `/api`를 제거하는 구조입니다.
Core 내부 기준 기본 경로는 아래와 같습니다.

| 도메인 | Base Path | 비고 |
|---|---|---|
| Family | `/family` | 그룹/멤버/초대 관련 |
| Family Invite | `/family/invites` | 인증 필요 |
| Family Public Invite | `/family/public/invites` | 공개 초대 플로우 |
| Family Notification Settings | `/family/{familyGroupId}/members/{targetUserId}/notification-settings` | 멤버 알림 설정 |
| Medication | `/medications` | 약 CRUD |
| Medication Logs | `/medications/logs` | 복용 로그 |
| Prescriptions | `/prescriptions` | 처방전 |
| Adherence | `/adherence` | 복약 순응도 |
| Diet | `/diet` | 식단 로그/경고 |
| Disease | `/disease` | 질병 관리 |
| Symptom Search | `/medications/search/symptoms` | 증상 기반 검색 |
| OCR | `/ocr` | 처방전 OCR |
| Notifications | `/notifications` | 알림 조회/읽음/삭제/SSE |
| Notification Settings | `/notifications/settings` | 알림 설정 |
| Reports | `/reports` | 리포트 |
| Chat (REST) | `/family-chat` | 가족 채팅 REST |
| Appointments | `/appointments` | 병원 예약 |
| Voice | `/voice` | 음성 명령 처리 |
| Security/Admin | `/admin/abuse` | 내부용 관리 |
| Dev | `/dev/kafka` | 개발 테스트용 |

## 4) 실시간 통신

- WebSocket/STOMP: `/ws` (핸드셰이크 시 `X-User-Id` 헤더 사용)
- SSE: `GET /notifications/subscribe` (Gateway 경유 시 `/api/notifications/subscribe`)

## 5) 인증 연동

- Gateway가 JWT를 검증하고 `X-User-*` 헤더를 주입합니다.
- Core는 `SecurityUtil`로 헤더를 해석합니다.
- SSE는 EventSource 제약으로 `token` 쿼리 파라미터를 허용하지만,
  **검증은 Gateway에서 수행**합니다.

## 6) 데이터 저장소/인프라 의존성

- MySQL: 트랜잭션 데이터 (JPA + MyBatis 병행)
- Redis: 캐시/세션/실시간 기능 일부
- Kafka: 이벤트 발행/소비
- PostgreSQL(+pgvector): LLM Guard 벡터 스토어

## 7) 외부 연동(키 필요)

문서에는 “키 이름”만 기록합니다.

- `OPENAI_API_KEY` (Spring AI)
- `GOOGLE_VISION_API_KEY` (OCR)
- `DRUGINFO_API_SERVICE_KEY` (식약처 API)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_S3_BUCKET`

## 8) 주요 환경 변수

- DB: `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`
- Redis: `SPRING_DATA_REDIS_HOST`, `SPRING_DATA_REDIS_PORT`, `SPRING_DATA_REDIS_PASSWORD`
- Kafka: `SPRING_KAFKA_BOOTSTRAP_SERVERS`
- JWT: `JWT_SECRET`, `JWT_ACCESS_TOKEN_EXPIRATION`, `JWT_REFRESH_TOKEN_EXPIRATION`
- Kakao: `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`, `KAKAO_REDIRECT_URI`
- Front/Auth URL: `FRONTEND_BASE_URL`, `AUTH_SERVICE_URL`
- pgvector: `PGVECTOR_JDBC_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

