# 🏥 뭐냑? (AMApill)

> 가족 돌봄 네트워크 기반 약 관리 플랫폼

[![React](https://img.shields.io/badge/React-19.1.1-61dafb?logo=react)](https://react.dev/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.8-6db33f?logo=springboot)](https://spring.io/projects/spring-boot)
[![Spring Cloud](https://img.shields.io/badge/Spring%20Cloud-2025.0.0-6db33f)](https://spring.io/projects/spring-cloud)
[![Java](https://img.shields.io/badge/Java-21%20LTS-orange?logo=openjdk)](https://openjdk.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479a1?logo=mysql)](https://www.mysql.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?logo=postgresql)](https://www.postgresql.org/)

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [핵심 기능](#-핵심-기능)
- [기술 스택](#-기술-스택)
- [시작하기](#-시작하기)
- [문서 가이드](#-문서-가이드)
- [프로젝트 구조](#-프로젝트-구조)
- [현재 코드 기준 모듈](#-현재-코드-기준-모듈)

---

## 🎯 프로젝트 소개

**뭐냑?**는 혼자 사시는 부모님의 약 복용을 자녀가 원격으로 관리하고 모니터링할 수 있는
**가족 돌봄 네트워크** 플랫폼입니다.

---

## 💡 핵심 기능 (코드 기준)

- 가족 네트워크(그룹/초대/멤버 관리)
- 약 관리(처방전, 스케줄, 복용 로그, 순응도)
- 식단 로그 및 약-음식 경고
- OCR 기반 처방전 등록
- 알림(SSE) 및 알림 설정
- 리포트(복약 순응도 등)
- 질병 관리 및 증상 기반 검색
- 가족 채팅(REST + WebSocket/STOMP)
- Voice 명령 처리
- 병원 예약/리마인드

---

## 🛠 기술 스택

### Frontend
- **Framework**: React 19 + Vite
- **상태 관리**: Zustand + React Query
- **스타일링**: MUI + Emotion
- **실시간**: STOMP WebSocket, SSE

### Backend
- **Language**: Java 21
- **Framework**: Spring Boot 3.5.8
- **Gateway**: Spring Cloud Gateway 2025.0.0
- **AI**: Spring AI 1.1.0
- **DB/ORM**: JPA + MyBatis
- **Messaging/Cache**: Kafka, Redis

### Database
- **MySQL**: 트랜잭션 데이터
- **PostgreSQL + pgvector**: LLM Guard 벡터 스토어

---

## 🚀 시작하기

빠른 시작은 다음 문서를 참고하세요.

- **빠른 시작**: [QUICKSTART.md](./QUICKSTART.md)
- **마이크로서비스 설정**: [MICROSERVICES_SETUP.md](./documents/MICROSERVICES_SETUP.md)

---

## 📚 문서 가이드

### 🚀 빠른 시작 가이드

| 문서 | 설명 |
|------|------|
| [QUICKSTART.md](./QUICKSTART.md) | 로컬 실행 가이드 |
| [FIGMA_GUIDE.md](./FIGMA_GUIDE.md) | Figma 플러그인 가이드 (아카이브됨) |
| [WIREFRAME_SCREENS.md](./WIREFRAME_SCREENS.md) | 와이어프레임 문서 (아카이브됨) |
| [DB스킬.md](./DB스킬.md) | DB 관련 문서 (아카이브됨) |
| [SECURITY_GUIDELINES.md](./SECURITY_GUIDELINES.md) | 보안 문서 가이드 |

### 📖 상세 문서

- 전체 문서 인덱스: [`documents/README.md`](./documents/README.md)

---

## 📁 프로젝트 구조

```
Front/                      # 프론트엔드
spring-cloud-api-gateway/   # API Gateway
auth-service/               # 인증 서비스
spring-boot/                # Core 서비스
docker-compose/             # 로컬 인프라
k8s/                        # Kubernetes 매니페스트
readme/                     # 프로젝트 문서
```

---

## ✅ 현재 코드 기준 모듈

### Backend (spring-boot)
- appointment, chat, diet, disease, family, interaction, medication,
  notification, ocr, report, voice, security

### Frontend (Front/src/features)
- appointment, auth, chat, dashboard, diet, disease, family, medication,
  notification, ocr, places, report, search, settings, voice

