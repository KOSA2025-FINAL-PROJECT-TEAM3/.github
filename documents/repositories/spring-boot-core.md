# spring-boot(Core) 분석

## 1) 책임(역할)

Auth Service를 제외한 **대부분의 비즈니스 도메인**을 단일 Spring Boot 서비스로 제공하는 “Core 서비스”입니다.

- 가족(그룹/멤버/초대/알림 설정)
- 약(처방전/약/스케줄/복용 로그/순응도)
- 식단(로그/분석/경고)
- OCR(처방전 스캔/비동기 Job)
- 알림(SSE 구독/히스토리)
- 리포트(복약 순응도 리포트)
- 질병(CRUD/약 연관/내보내기)
- 가족 채팅(REST + WebSocket/STOMP + Kafka 연계)
- Voice(음성 명령 텍스트 처리)

## 2) 실행/포트

- 기본 포트: `8082`
- Swagger UI: `GET /swagger-ui.html`
- OpenAPI: `GET /v3/api-docs`
- Health: `GET /actuator/health`

## 3) API 베이스 경로(대표)

Gateway에서 `StripPrefix=1`을 사용하는 경우, 외부 호출(`/api/...`)이 Core 내부에서는 다음과 같이 매핑됩니다.

- 외부: `/api/family/**` → 내부: `/family/**`
- 외부: `/api/medications/**` → 내부: `/medications/**`
- 외부: `/api/prescriptions/**` → 내부: `/prescriptions/**`
- 외부: `/api/diet/**` → 내부: `/diet/**`
- 외부: `/api/ocr/**` → 내부: `/ocr/**`
- 외부: `/api/notifications/**` → 내부: `/notifications/**`
- 외부: `/api/reports/**` → 내부: `/reports/**`
- 외부: `/api/disease/**` → 내부: `/disease/**`
- 외부: `/api/family-chat/**` → 내부: `/family-chat/**`
- 외부: `/api/voice/**` → 내부: `/voice/**`

## 4) 인증 연동(헤더 기반)

- Gateway가 JWT를 검증하고 `X-User-*` 헤더를 주입합니다.
- Core는 `SecurityUtil`로 `X-User-Id` 등을 추출해 사용자 컨텍스트를 구성합니다.
- SSE 구독은 EventSource 제약 때문에 `token` 쿼리 파라미터를 받을 수 있으나, **실제 인증은 Gateway에서 수행**하고 Core는 `X-User-Id`를 신뢰합니다.

## 5) 데이터 저장소/인프라 의존성

- MySQL(Init Scripts 기준):
  - 처방전/약/복약: `prescriptions`, `medications`, `medication_schedules`, `medication_logs`, `medication_adherence_daily`
  - 가족 네트워크: `family_groups`, `family_members`, `family_invites`, `family_notification_settings`
  - 식단/경고: `diet_logs`, `diet_warnings`
  - 질병/연관: `diseases`, `disease_medication_relations`, `disease_warning_relations`, `disease_audit_logs`
  - 병원 예약: `hospital_appointments`, `appointment_reminders`, `appointment_reminder_deliveries`
  - 알림/채팅: `notifications`, `notification_settings`, `family_chat_message`
- Redis: 캐시/토큰/실시간 기능 일부(구현에 따라)
- Kafka: 채팅/알림 등 이벤트 발행/소비
- PostgreSQL(+pgvector): AI/보안 벡터 스토어 등(설정 기반)

## 6) 외부 연동(키 필요)

문서에는 “키 이름”만 기록합니다.

- `OPENAI_API_KEY` (Spring AI)
- `GOOGLE_VISION_API_KEY` (OCR)
- S3 업로드 관련 키/버킷(환경 변수로 분리 권장)
- 공공데이터(식약처) API 키(환경 변수로 분리 권장)
