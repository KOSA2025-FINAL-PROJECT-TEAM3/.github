# 🏥 뭐냑? (AMApill) - Team 3

> 가족 돌봄 네트워크 기반 약 관리 플랫폼
>
> 떨어져 있어도 부모님 건강을 지킬 수 있습니다

[![React](https://img.shields.io/badge/React-19-61dafb?logo=react)](https://react.dev/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4.7-6db33f?logo=springboot)](https://spring.io/projects/spring-boot)
[![Java](https://img.shields.io/badge/Java-21%20LTS-orange?logo=openjdk)](https://openjdk.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479a1?logo=mysql)](https://www.mysql.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)

---

## 👥 팀 소개

**KOSA 2025 Final Project - Team 3 (팀 삼조격~)**

우리는 한국소프트웨어인재개발원(KOSA) 2025년 최종 프로젝트를 진행하는 팀입니다.
실버 세대의 건강한 약 복용 관리를 위한 가족 돌봄 네트워크 플랫폼 **뭐냑?(AMApill)**를 개발하고 있습니다.

### 프로젝트 기간
- **시작일**: 2025년 11월 5일
- **종료일**: 2025년 12월 31일 (7주)
- **최종 발표**: 2025년 12월 31일

### 팀원 구성

| 역할 | 담당 기술 | GitHub |
|------|----------|--------|
| **Frontend Lead** | React 19, Vite, Hocuspocus, Y.js CRDT | [@팀원1](https://github.com/팀원1) |
| **Backend Lead + AI** | Spring Boot 3, Microservices, OCR, Kafka | [@팀원2](https://github.com/팀원2) |
| **Database + DevOps** | MySQL 8.0, PostgreSQL 16, Redis, Docker | [@팀원3](https://github.com/팀원3) |

---

## 🎯 프로젝트 소개

**뭐냑?**는 혼자 사시는 부모님의 약 복용을 자녀가 원격으로 관리하고 모니터링할 수 있는 **가족 돌봄 네트워크** 플랫폼입니다.

### 해결하는 문제

- 🏠 혼자 사시는 부모님이 약을 잘 안 드심
- 📱 자녀가 챙겨드리고 싶지만 물리적으로 멀리 떨어짐
- 👴 부모님은 복잡한 앱 사용이 어려움
- ⚠️ 기존 약 관리 앱은 개인용이며 가족 연동이 없음

### 핵심 차별점

| 기존 앱 (알약, 똑닥) | 뭐냑? |
|-------------------|---------|
| ❌ 개인 사용자만 | ✅ 시니어 + 자녀 양면 시장 |
| ❌ 가족 연동 없음 | ✅ 실시간 돌봄 네트워크 |
| ❌ 약-약 상호작용만 | ✅ **약-음식 충돌 자동 경고** |
| ❌ 수동 입력만 | ✅ **OCR 자동 인식** |
| ❌ 의료진 소통 없음 | ✅ 복약 순응도 리포트 |

---

## 💡 핵심 기능

### 1. 가족 돌봄 네트워크 (MVP 1순위)
- 자녀가 원격으로 부모님 약 스케줄 등록
- 실시간 복용 현황 모니터링 (Hocuspocus WebSocket)
- 약 미복용 시 자녀에게 즉시 알림

### 2. 약-음식 충돌 경고 (MVP 2순위)
- 룰 베이스 시스템으로 약-음식 상호작용 자동 검사
- 심각도별 경고 (높음/중간/낮음)
- 대체 음식 추천

### 3. 약봉지 OCR 자동 등록 (MVP 3순위)
- Google Vision API로 처방전 자동 인식
- Tesseract.js Fallback
- 약 정보 자동 파싱 및 등록

### 4. 알약 역검색
- 식약처 API 연동
- 모양, 색상, 각인으로 약 식별

### 5. 복약 순응도 리포트
- 주간/월간 복약 통계
- PDF 리포트 생성
- 의료진 공유 가능

---

## 🛠 기술 스택

### Frontend
- **Framework**: React 19 + Vite (JSX only)
- **실시간 동기화**: Hocuspocus + TipTap + Y.js CRDT
- **스타일링**: SCSS / CSS Modules

### Backend (Microservices Architecture)
- **Language**: Java 21 LTS (Virtual Threads, ZGC)
- **Framework**: Spring Boot 3.4.7
- **Cloud**: Spring Cloud 2024.0.2 (Moorgate)
- **보안**: Spring Security (JWT)
- **메시징**: Apache Kafka

#### Spring Cloud Components
- **API Gateway**: Spring Cloud Gateway (라우팅, 인증, 로드 밸런싱)
- **Service Discovery**: Eureka Server (서비스 등록/조회)
- **Config Server**: 중앙 설정 관리 (Git 기반)
- **Service Communication**: OpenFeign (마이크로서비스 간 통신)

#### Microservices
1. **Auth Service** (8081): 인증/인가, JWT 토큰 관리
2. **Medication Service** (8082): 약 관리, 복용 일정
3. **Family Service** (8083): 가족 네트워크, 권한 관리
4. **Diet Service** (8084): 식단 관리, 약-음식 충돌 검사
5. **Notification Service** (8085): 알림 발송
6. **OCR Service** (8086): 약봉지 OCR 처리

### Database (이중화 구조)
- **트랜잭션 DB**: MySQL 8.0 (사용자, 약, 가족, 식단)
- **실시간 동기화 DB**: PostgreSQL 16 (Hocuspocus Y.js CRDT)
- **캐싱**: Redis 7+

### External API
- **OCR**: Google Vision API / Tesseract.js
- **약 정보**: 식약처 의약품안전나라 API
- **알림**: 카카오톡 알림톡 (Phase 2)
- **워크플로우**: n8n Automation

---

## 📦 저장소

### 프로젝트 저장소

| 저장소 | 설명 | 링크 |
|--------|------|------|
| **Front** | React 프론트엔드 + 프로젝트 문서 | [KOSA2025-FINAL-PROJECT-TEAM3/Front](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front) |
| **Back** | Spring Boot 백엔드 | [KOSA2025-FINAL-PROJECT-TEAM3/Back](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Back) |
| **.github** | 조직 프로필 및 문서 아카이브 | [KOSA2025-FINAL-PROJECT-TEAM3/.github](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github) |

### 문서 위치

모든 프로젝트 문서와 다이어그램은 이 저장소(.github)에 보관되어 있습니다:

- 📖 **프로젝트 명세**: [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
- 📋 **MVP & DTO 명세**: [MVP_DTO_SPECIFICATION.md](../MVP_DTO_SPECIFICATION.md)
- 🗓️ **개발 로드맵**: [DEVELOPMENT_ROADMAP.md](../DEVELOPMENT_ROADMAP.md)
- 🏗️ **시스템 아키텍처**: [ARCHITECTURE.md](../ARCHITECTURE.md)
- 🐳 **마이크로서비스 셋업**: [MICROSERVICES_SETUP.md](../MICROSERVICES_SETUP.md)
- 📁 **소스 구조**: [SRC_STRUCTURE.md](../SRC_STRUCTURE.md)
- 🎨 **와이어프레임 가이드**: [WIREFRAME_SCREENS.md](../WIREFRAME_SCREENS.md)
- 📊 **다이어그램 파일**: [diagrams/](../diagrams/)
- 🎨 **Figma 와이어프레임**: [figma-exports/](../figma-exports/)
- 🔌 **Figma 플러그인**: [figma-plugin/](../figma-plugin/)

---

## 🎯 개발 현황

### Phase 1: 기획 및 설계 (Week 1-2) ✅ 완료
- ✅ 프로젝트 기획 및 명세 작성
- ✅ 시스템 아키텍처 설계
- ✅ 데이터베이스 스키마 설계 (ERD, DDL)
- ✅ API 엔드포인트 및 DTO 정의 (40개 이상)
- ✅ 와이어프레임 제작 (10개 화면)
- ✅ 기술 스택 확정

### Phase 2: 개발 (Week 3-5) 🚧 진행 예정
- [ ] Frontend 개발 (React)
- [ ] Backend 개발 (Spring Boot)
- [ ] 실시간 동기화 구현 (Hocuspocus)
- [ ] OCR 연동 (Google Vision)
- [ ] 약-음식 충돌 룰 엔진 구현

### Phase 3: 테스트 및 배포 (Week 6-7) ⏳ 대기 중
- [ ] 통합 테스트
- [ ] 성능 최적화
- [ ] CI/CD 파이프라인 구축
- [ ] 최종 발표 준비

---

## 🔒 보안 및 법적 고려사항

- **개인정보보호**: AES-256 암호화, HTTPS 강제
- **인증/인가**: JWT 기반 (Access 15분, Refresh 7일)
- **의료 정보 보호**: 명시적 동의 필수, 접근 로그 기록
- **약사법 준수**: 약 추천 금지, 정보 제공만
- **허위/과장 광고 금지**: 식약처 공식 정보만 표시

자세한 내용은 [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) 참조

---

## 🚀 빠른 시작

### Frontend 실행

```bash
# Front 저장소 클론
git clone https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front.git
cd Front

# 의존성 설치
npm install

# 개발 서버 시작
npm run dev
```

### Backend 실행

```bash
# Back 저장소 클론
git clone https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Back.git
cd Back

# Docker Compose로 전체 스택 실행
docker-compose up -d
```

자세한 설정 가이드는 [QUICKSTART.md](../QUICKSTART.md) 참조

---

## 📞 연락처

- **GitHub Organization**: [KOSA2025-FINAL-PROJECT-TEAM3](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3)
- **프로젝트 이슈**: [Front Issues](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/issues)
- **조직 가이드라인**: [checkme.md](../checkme.md)

---

## 🙏 감사의 말

- 식약처 의약품안전나라 공공 API
- Google Cloud Vision API
- Spring Boot & React Community
- KOSA 부트캠프 멘토님들

---

## 📝 License

이 프로젝트는 교육 목적으로 제작되었습니다.

---

**최종 수정일**: 2025-11-06
**작성자**: KOSA 2025 Team 3 (뭐냑? 개발팀)
**조직 모토**: 팀 삼조격~ 💪
