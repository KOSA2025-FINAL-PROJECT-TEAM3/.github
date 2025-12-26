---
title: 프로젝트 상세 문서 (현재 코드 기준)
last_updated: 2025-12-13
---

# 🧾 프로젝트 상세 문서 (현재 코드 기준)

이 문서는 **뭐냑? (AMApill)** 프로젝트의 현재 코드/설정 상태를 기준으로,
서비스 구성, 데이터 구조, 실행/배포 흐름을 한 문서에서 빠르게 파악할 수 있도록 정리합니다.

---

## 1) 프로젝트 개요

- **목적**: 가족 돌봄 네트워크 기반 원격 복약 관리 플랫폼
- **핵심 가치**: 시니어 복약 관리 + 보호자 모니터링 + 약/음식 상호작용 경고
- **현 구현 기준**: `Front`, `spring-cloud-api-gateway`, `auth-service`, `spring-boot`, `docker-compose`, `k8s`

---

## 2) 시스템 구성 요약

**클라이언트 → (Nginx) → API Gateway → Auth/Core → DB/Redis/Kafka**

- **Gateway**가 JWT를 검증하고 `X-User-*` 헤더 주입
- 내부 서비스는 JWT를 직접 파싱하지 않음
- SSE는 Gateway에서 장시간 연결 허용

---

## 3) 레포지토리 구성

| 레포지토리 | 역할 | 기본 포트(로컬) | 비고 |
|---|---|---:|---|
| `Front` | React 19 + Vite SPA | `5173` | `/api`, `/ws` 프록시 가능 |
| `spring-cloud-api-gateway` | 단일 진입점 | `8080` | JWT 검증/라우팅/캐싱 |
| `auth-service` | 인증/프로필 | `8081` | `/auth/**`, `/auth/users/**` |
| `spring-boot` | Core 서비스 | `8082` | Swagger 제공 |
| `docker-compose` | 로컬 인프라 | - | DB init scripts 포함 |
| `k8s` | K8s 배포 리소스 | - | 네임스페이스 분리 운영 |

상세 분석 문서:
- `documents/repositories/spring-cloud-api-gateway.md`
- `documents/repositories/auth-service.md`
- `documents/repositories/spring-boot-core.md`
- `documents/repositories/docker-compose.md`
- `documents/repositories/k8s-manifests.md`

---

## 4) 서비스 책임 분리

### 4.1 API Gateway
- 라우팅: `/api/**`, `/ws/**`
- 인증: JWT 검증 후 헤더 주입
- 캐싱: Redis 기반 GET 캐싱
- 장애 격리: Resilience4j

### 4.2 Auth Service
- 회원가입/로그인/로그아웃
- JWT 발급/갱신(Refresh 포함)
- Kakao OAuth 연동
- 사용자 프로필 관리

### 4.3 Core Service (spring-boot)
- 가족 네트워크, 약/복약, 식단, OCR, 알림, 리포트
- 가족 채팅(WebSocket/STOMP + Kafka)
- 질병 정보 CRUD, 병원 예약
- Voice(음성 명령)

---

## 5) 데이터 저장소 구조 (init scripts 기준)

### 5.1 MySQL (트랜잭션)
- 인증/사용자: `users`, `kakao_tokens`
- 처방전/약/복약: `prescriptions`, `medications`, `medication_schedules`, `medication_logs`, `medication_adherence_daily`
- 가족 네트워크: `family_groups`, `family_members`, `family_invites`, `family_notification_settings`
- 식단/경고: `diet_logs`, `diet_warnings`
- 질병/연관: `diseases`, `disease_medication_relations`, `disease_warning_relations`, `disease_audit_logs`
- 병원 예약: `hospital_appointments`, `appointment_reminders`, `appointment_reminder_deliveries`
- 알림/채팅: `notifications`, `notification_settings`, `family_chat_message`
- 보안/감사: `security_audit_logs`, `abuse_audit_log`, `access_logs`

### 5.2 PostgreSQL (+pgvector)
- `vector_store` (embedding 저장)

스키마 근거:
- `docker-compose/init-scripts/mysql/*.sql`
- `docker-compose/init-scripts/postgresql/*.sql`

---

## 6) 실행 흐름 (로컬 Dev 기준)

1. `docker-compose`로 인프라 실행
2. Gateway/Auth/Core를 IDE에서 실행
3. `http://localhost:8080/api/...` 또는 `http://localhost/api/...` 호출

헬스체크:
```
curl http://localhost:8080/actuator/health
curl http://localhost:8081/actuator/health
curl http://localhost:8082/actuator/health
```

---

## 7) 배포 구조 (K8s)

- `k8s/`에서 배포 리소스를 관리
- `applications`: `auth-service`, `spring-boot`
- `apigateway`: `spring-cloud-api-gateway`
- `database`: MySQL/PostgreSQL/Redis + Admin 도구
- `middleware`: Kafka
- `core`: ingress-nginx, cloudflared

---

## 8) 보안/운영 원칙

- 문서에 민감정보(패스워드/키/토큰) 금지
- 환경 변수는 키 이름만 기록
- JWT 검증은 Gateway 단일 책임
- DB 변경은 init scripts 기준으로 관리

---

## 9) 관련 문서

- `documents/ARCHITECTURE.md`
- `documents/MICROSERVICES_SETUP.md`
- `documents/REPOSITORIES.md`
- `documents/DATABASE_SCHEMA_ANALYSIS.md`

