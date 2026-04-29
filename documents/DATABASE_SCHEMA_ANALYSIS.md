# 🗄️ 데이터베이스 스키마(Dev) - 근거/요약

이 문서는 “현재 개발 환경에서 실제로 사용되는 DB 스키마의 근거가 무엇인지”를 명확히 하고,
테이블 구성을 빠르게 파악할 수 있도록 요약합니다.

---

## 1) Source of Truth (가장 중요)

Dev 기준 DB 스키마의 단일 근거는 **`docker-compose/init-scripts`**입니다.

- MySQL DDL: `docker-compose/init-scripts/mysql/*.sql`
- PostgreSQL DDL: `docker-compose/init-scripts/postgresql/*.sql`

---

## 2) 데이터 저장소 구성

### 2.1 MySQL (트랜잭션/도메인 데이터)

주요 테이블(Dev init scripts 기준):

- 인증/사용자: `users`, `kakao_tokens`
- 처방전/약/복약: `prescriptions`, `medications`, `medication_schedules`, `medication_logs`, `medication_adherence_daily`
- 가족 네트워크: `family_groups`, `family_members`, `family_invites`, `family_notification_settings`
- 식단/경고: `diet_logs`, `diet_warnings`
- 질병/연관: `diseases`, `disease_medication_relations`, `disease_warning_relations`, `disease_audit_logs`
- 병원 예약: `hospital_appointments`, `appointment_reminders`, `appointment_reminder_deliveries`
- 알림: `notifications`, `notification_settings`
- 채팅: `family_chat_message`
- 보안/감사: `security_audit_logs`, `abuse_audit_log`, `access_logs`

### 2.2 PostgreSQL (+pgvector)

- `vector_store` (embedding 저장)

용도 예시:

- LLM Guard 시드/유사도 검색
- 향후 RAG/추천 등 확장 기반

---

## 3) 관계(ERD 관점 요약)

MySQL에는 일부 FK가 정의되어 있으며, 일부는 서비스 간 참조로 남겨둡니다.

ERD는 다음 다이어그램을 최신 기준으로 봅니다:

- [`diagrams/07-database-erd-current.mmd`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/diagrams/07-database-erd-current.mmd)

---

## 4) 운영/개발 주의사항 (문서 범위)

- 문서에는 DB 계정/패스워드/접속 문자열의 “실제 값”을 기록하지 않습니다.
- DB 스키마 변경은 init scripts 단위로 관리하는 것을 권장합니다.

