# 🏥 뭐냑? (AMApill)

> 가족 돌봄 네트워크 기반 약 관리 플랫폼
>
> 떨어져 있어도 부모님 건강을 지킬 수 있습니다

[![React](https://img.shields.io/badge/React-19-61dafb?logo=react)](https://react.dev/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4.7-6db33f?logo=springboot)](https://spring.io/projects/spring-boot)
[![Java](https://img.shields.io/badge/Java-21%20LTS-orange?logo=openjdk)](https://openjdk.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479a1?logo=mysql)](https://www.mysql.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [핵심 기능](#-핵심-기능)
- [기술 스택](#-기술-스택)
- [시작하기](#-시작하기)
- [문서 가이드](#-문서-가이드)
- [팀 정보](#-팀-정보)

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
- 실시간 복용 현황 모니터링 (Spring WebSocket/STOMP)
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
- **실시간 통신**: STOMP WebSocket Client
- **스타일링**: SCSS / CSS Modules

### Backend (Microservices Architecture)
- **Language**: Java 21 LTS
- **Framework**: Spring Boot 3.4.7
- **Cloud**: Spring Cloud 2024.0.2 (API Gateway, Eureka, Config Server)
- **보안**: Spring Security (JWT)
- **메시징**: Apache Kafka

**6개 마이크로서비스**: Auth, Medication, Family, Diet, Notification, OCR

### Database
- **메인 DB**: MySQL 8.0 (트랜잭션 데이터)
- **동기화 DB**: PostgreSQL 16 (실시간 협업 - 선택)
- **캐싱**: Redis 7+ (세션, 토큰)

### External API
- **OCR**: Google Vision API / Tesseract.js
- **약 정보**: 식약처 의약품안전나라 API

**상세 정보**: [ARCHITECTURE.md](./documents/ARCHITECTURE.md) | [MICROSERVICES_SETUP.md](./documents/MICROSERVICES_SETUP.md)

---

## 🚀 시작하기

### 빠른 실행 (5분)

```bash
# 1. 저장소 클론
git clone https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front.git
cd Front

# 2. Docker Compose로 전체 스택 실행
docker-compose up -d

# 3. Frontend 개발 서버 시작
npm install
npm run dev
```

**접속**: http://localhost:5173

### 상세 가이드

- **빠른 시작**: [QUICKSTART.md](./QUICKSTART.md)
- **마이크로서비스 설정**: [MICROSERVICES_SETUP.md](./documents/MICROSERVICES_SETUP.md)
- **개발 로드맵**: [DEVELOPMENT_ROADMAP.md](./documents/DEVELOPMENT_ROADMAP.md)

---

## 📚 문서 가이드

### 🚀 빠른 시작 가이드

| 문서 | 설명 |
|------|------|
| [QUICKSTART.md](./QUICKSTART.md) | 5분 안에 프로젝트 시작하기 - 설치부터 실행까지 |
| [FIGMA_GUIDE.md](./FIGMA_GUIDE.md) | Figma 플러그인 설치 및 와이어프레임 가져오기 |
| [WIREFRAME_SCREENS.md](./WIREFRAME_SCREENS.md) | 10개 화면 구성 및 기능 설명 |
| [DB스킬.md](./DB스킬.md) | 데이터베이스 스키마, ERD, DDL 가이드 |
| [SECURITY_GUIDELINES.md](./SECURITY_GUIDELINES.md) | 보안 및 문서 작성 가이드라인 (KISA Secure Coding 준수) |

### 📖 상세 명세서 및 설계 문서

모든 상세 명세서는 [`documents/`](./documents/) 폴더에서 확인할 수 있습니다:

| 카테고리 | 문서 | 설명 |
|---------|------|------|
| **프로젝트 기획** | [PROJECT_SPECIFICATION.md](./documents/PROJECT_SPECIFICATION.md) | 전체 요구사항, 기능 정의, 기술 스택 |
| | [MVP_DTO_SPECIFICATION.md](./documents/MVP_DTO_SPECIFICATION.md) | MVP 우선순위, API 엔드포인트, DTO (40개+) |
| | [CHAT_API_SPECIFICATION.md](./documents/CHAT_API_SPECIFICATION.md) | 채팅/상담 API, WebSocket 프로토콜 |
| | [DEVELOPMENT_ROADMAP.md](./documents/DEVELOPMENT_ROADMAP.md) | 7주 개발 일정, 마일스톤 |
| **아키텍처** | [ARCHITECTURE.md](./documents/ARCHITECTURE.md) | 시스템 구조, Mermaid 다이어그램 9개 |
| | [MICROSERVICES_SETUP.md](./documents/MICROSERVICES_SETUP.md) | 마이크로서비스 구성, Docker Compose |
| | [SRC_STRUCTURE.md](./documents/SRC_STRUCTURE.md) | 소스 구조, SOLID 원칙, AOP 패턴 |
| | [FRONTEND_COMPONENTS_SPECIFICATION.md](./documents/FRONTEND_COMPONENTS_SPECIFICATION.md) | 컴포넌트 트리, Props 명세, 라우팅 |
| **개발 규칙** | [CONVENTIONS.md](./documents/CONVENTIONS.md) | Git 전략, 커밋 규칙, 네이밍 컨벤션 |
| **페르소나** | [페르소나설정.md](./documents/페르소나설정.md) | 사용자 페르소나, 시나리오 |

📂 **[전체 명세서 모음 보기 →](./documents/)**

### 📊 다이어그램 및 리소스

| 폴더 | 내용 |
|------|------|
| [`diagrams/`](./diagrams/) | Mermaid 다이어그램 9개 (시스템 구조, ERD, Gantt 차트 등) |
| [`figma-exports/`](./figma-exports/) | Figma 와이어프레임 JSON (10개 화면) |
| [`figma-plugin/`](./figma-plugin/) | Figma 플러그인 코드 |

---

## 📁 프로젝트 구조

```
.github/
├── documents/             # 📚 상세 명세서 및 설계 문서
│   ├── PROJECT_SPECIFICATION.md
│   ├── ARCHITECTURE.md
│   ├── MICROSERVICES_SETUP.md
│   └── ... (기타 명세서)
├── diagrams/              # 📊 Mermaid 다이어그램 파일 (9개)
├── figma-exports/         # 🎨 Figma JSON 와이어프레임
├── figma-plugin/          # 🔌 Figma 플러그인 코드
├── profile/               # 👥 조직 프로필
├── README.md              # 📖 프로젝트 메인 소개
├── QUICKSTART.md          # 🚀 빠른 시작 가이드
├── FIGMA_GUIDE.md         # 🎨 Figma 가이드
├── WIREFRAME_SCREENS.md   # 📱 화면 설명
├── DB스킬.md              # 🗄️ 데이터베이스 가이드
└── SECURITY_GUIDELINES.md # 🔒 보안 가이드라인
```

자세한 디렉토리 구조는 [SRC_STRUCTURE.md](./documents/SRC_STRUCTURE.md) 참조

---

## 🎯 개발 현황

### 완료된 작업
- ✅ 프로젝트 기획 및 명세 작성
- ✅ 시스템 아키텍처 설계
- ✅ 데이터베이스 스키마 설계 (ERD, DDL)
- ✅ API 엔드포인트 및 DTO 정의
- ✅ 와이어프레임 제작 (10개 화면)
- ✅ 기술 스택 확정

### 진행 예정
- [ ] Frontend 개발 (React)
- [ ] Backend 개발 (Spring Boot)
- [ ] 실시간 동기화 구현 (Hocuspocus)
- [ ] OCR 연동 (Google Vision)
- [ ] 약-음식 충돌 룰 엔진 구현
- [ ] 통합 테스트 및 배포

---

## 🔒 보안 및 법적 고려사항

- **개인정보보호**: AES-256 암호화, HTTPS 강제
- **인증/인가**: JWT 기반 (Access 15분, Refresh 7일)
- **의료 정보 보호**: 명시적 동의 필수, 접근 로그 기록
- **약사법 준수**: 약 추천 금지, 정보 제공만
- **허위/과장 광고 금지**: 식약처 공식 정보만 표시

자세한 내용은 [PROJECT_SPECIFICATION.md](./documents/PROJECT_SPECIFICATION.md) 참조

---

## 👥 팀 정보

### KOSA 2025 Final Project - Team 3

**프로젝트 기간**: 2025년 11월 5일 ~ 2025년 12월 31일 (7주)

**발표일**: 2025년 12월 31일

### 역할 분담

- **팀원 1**: Frontend Lead (React, Hocuspocus)
- **팀원 2**: Backend Lead + AI (Spring Boot, OCR, Kafka)
- **팀원 3**: Database + DevOps (MySQL, Redis, CI/CD)

---

## 📞 연락처

- **GitHub Repository**: [KOSA2025-FINAL-PROJECT-TEAM3/Front](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front)
- **Backend Repository**: [KOSA2025-FINAL-PROJECT-TEAM3/spring-boot](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/spring-boot)

---

## 📝 License

이 프로젝트는 교육 목적으로 제작되었습니다.

---

## 🙏 감사의 말

- 식약처 의약품안전나라 공공 API
- Google Cloud Vision API
- Spring Boot & React Community
- KOSA 부트캠프 멘토님들

---

**최종 수정일**: 2025-11-05
**문서 버전**: 2.0
**작성자**: 뭐냑? 개발팀
