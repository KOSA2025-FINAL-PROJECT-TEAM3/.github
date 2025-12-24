# docker-compose 분석

## 1) 목적

로컬에서 **DB/캐시/메시징 등 인프라**를 빠르게 띄우고, 필요 시 Gateway/Auth 및 (향후) 도메인 서비스를 컨테이너로 함께 실행할 수 있는 구성입니다.

## 2) 기본 구성(항상 실행되는 서비스)

`docker-compose.yml`에서 profile 없이 기본으로 실행되는 인프라:

- MySQL `3306`
- PostgreSQL(+pgvector) `5432`
- Redis `6379`
- Kafka(KRaft) `9092`
- Nginx `80` (SPA 정적서빙 + `/api/`, `/ws/`를 Gateway로 프록시)
- phpMyAdmin `8888`
- redis-commander `8889`

## 3) 선택 구성(프로필 기반)

- `--profile full`: Gateway/Auth 및 (향후) 분리 서비스, n8n, hocuspocus 등을 포함한 “풀스택”
  - `api-gateway:8080` (profile: `full`, `services`)
  - `auth-service:8081` (profile: `full`)
  - `family-service` 등 다수 서비스는 현재 “미구현/분리 예정” 상태로 주석/프로필로 관리

## 4) DB 초기화(근거 DDL)

DB 스키마는 아래 init script가 **단일 근거(source of truth)** 입니다.

- MySQL: `docker-compose/init-scripts/mysql/*.sql`
  - 대표 테이블: `users`, `kakao_tokens`, `prescriptions`, `medications`, `medication_schedules`, `medication_logs`, `medication_adherence_daily`, `family_groups`, `family_members`, `family_invites`, `diet_logs`, `diet_warnings`, `notifications`, `notification_settings`, `family_chat_message`, `diseases`, `disease_medication_relations`, `hospital_appointments`, `appointment_reminders`, `appointment_reminder_deliveries`, `security_audit_logs`, `abuse_audit_log`, `access_logs`
- PostgreSQL: `docker-compose/init-scripts/postgresql/*.sql`
  - `vector_store` 등(LLM Guard/임베딩 용도)

## 5) 로컬 권장 실행 시나리오

- 인프라만 띄우고(Compose) 서비스는 IDE에서 실행: 개발 속도/디버깅에 유리
- Nginx는 `/api/`를 `host.docker.internal:8080`으로 프록시하므로, 로컬에서 Gateway만 띄워도 브라우저 호출 흐름이 단순해집니다.
