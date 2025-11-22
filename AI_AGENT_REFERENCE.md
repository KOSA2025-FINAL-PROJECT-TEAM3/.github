# 🤖 AI Agent Quick Reference

> Claude Code, Cursor, Windsurf, Cline 등 MCP Agent를 위한 핵심 정보
> **Last Updated**: 2025-11-22
> **Architecture**: MSA + Clean Architecture

---

## 📋 프로젝트 핵심 정보

| 항목 | 정보 |
|------|------|
| **프로젝트명** | AMApill (뭐냑?) - Family Care Network Medication Management Platform |
| **목적** | 가족 간 원격 복약 관리 및 약물-음식 상호작용 경고 플랫폼 |
| **프로젝트 기간** | 2025-11-05 ~ 2025-12-31 (7주 개발 + 최종 발표) |
| **팀** | KOSA 2025 Final Project Team 3 (3명) |
| **저장소 구조** | 3개 독립 저장소 (Frontend / Backend / Documentation) |

---

## 🏗️ 아키텍처 개요

### Repository 구조
```
KOSA2025-FINAL-PROJECT-TEAM3/
├── Front/          # React 19 + Vite + Hocuspocus (실시간 동기화)
├── Back/           # Spring Boot 3.4 Microservices (6개 서비스)
└── .github/        # 📍 현재 위치 - 통합 문서 및 다이어그램 저장소
```

### 기술 스택

#### Frontend
- **프레임워크**: React 19 + Vite
- **상태 관리**: Zustand
- **실시간 동기화**: Hocuspocus + Y.js CRDT
- **라우팅**: React Router v6
- **스타일링**: SCSS/CSS Modules, Tailwind CSS (선택 사항)
- **WebSocket**: STOMP (가족 네트워크 채팅)
- **개발 서버**: `npm run dev` → `http://localhost:5173`

#### Backend (Microservices)
- **언어**: Java 21 LTS (Virtual Threads, ZGC)
- **프레임워크**: Spring Boot 3.4.7 + Spring Cloud 2024.0.2 (Moorgate)
- **ORM**: MyBatis 3.0.3 (JPA 대신 사용)
- **AI/Vector**: Spring AI 1.0.3 (Redis Vector Store)
- **MSA 구조**:
  1. **Auth Service** (8081) - JWT 인증, 사용자 관리
  2. **Core Service** (8082) - 약/가족/식단/알림 통합 서비스
- **MSA 인증 흐름**:
  ```
  Client → Nginx Gateway → Auth Service (JWT 검증)
                        → Core Service (X-User-* 헤더로 사용자 정보 전달)
  ```
- **전달 헤더**: X-User-Id, X-User-Email, X-User-Name, X-User-Role, X-Customer-Role
- **인프라**: Nginx Gateway, Spring Cloud (선택)
- **메시징**: Apache Kafka
- **서비스 통신**: OpenFeign / REST

#### Database & Cache
- **MySQL 8.0**: 트랜잭션 데이터 (사용자, 복약, 가족)
- **PostgreSQL 16**: 실시간 동기화 상태 (Hocuspocus Y.js)
- **Redis 7+**: 세션 토큰 및 캐싱

#### 외부 API
- Google Vision API (OCR, Tesseract.js 폴백)
- 식약처 API (약안전나라)
- Kakao 알림 API (Phase 2)

---

## 📖 문서 읽기 순서 (AI Agent 권장)

AI Agent가 프로젝트를 이해하기 위한 **필수 문서 읽기 순서**입니다.

### 1단계: 프로젝트 개요 파악 (5분)
| 순서 | 문서 경로 | 설명 |
|------|-----------|------|
| 1️⃣ | `/README.md` | 프로젝트 소개, 핵심 기능, 저장소 링크 |
| 2️⃣ | `/QUICKSTART.md` | 5분 Docker Compose 환경 구축 가이드 |
| 3️⃣ | `/profile/README.md` | 팀 구성 및 조직 프로필 |

### 2단계: 요구사항 및 명세 이해 (20분)
| 순서 | 문서 경로 | 설명 |
|------|-----------|------|
| 4️⃣ | `/documents/PROJECT_SPECIFICATION.md` | **핵심 문서** - 전체 요구사항, 기술 스택 결정 이유, 법적 고려사항 (75KB) |
| 5️⃣ | `/documents/페르소나설정.md` | 사용자 페르소나 (시니어, 보호자) 및 시나리오 |
| 6️⃣ | `/WIREFRAME_SCREENS.md` | 10개 화면 UI/UX 명세 |

### 3단계: 시스템 아키텍처 이해 (30분)
| 순서 | 문서 경로 | 설명 |
|------|-----------|------|
| 7️⃣ | `/documents/ARCHITECTURE.md` | **필독** - 시스템 설계 및 9개 Mermaid 다이어그램 참조 (27KB) |
| 8️⃣ | `/diagrams/01-system-architecture.mmd` | 전체 마이크로서비스 토폴로지 |
| 9️⃣ | `/diagrams/02-data-flow.mmd` | 실시간 동기화 시퀀스 (시니어 ↔ 보호자) |
| 🔟 | `/diagrams/07-database-erd-v6.2.mmd` | **최신 ERD** (v6.2) |

### 4단계: API 및 데이터 구조 (15분)
| 순서 | 문서 경로 | 설명 |
|------|-----------|------|
| 1️⃣1️⃣ | `/documents/MVP_DTO_SPECIFICATION.md` | **API 필수** - 40+ DTO, 엔드포인트 명세 (19KB) |
| 1️⃣2️⃣ | `/documents/CHAT_API_SPECIFICATION.md` | WebSocket 프로토콜 (가족 채팅) |
| 1️⃣3️⃣ | `/DB스킬.md` | 데이터베이스 ERD 및 DDL 스크립트 |

### 5단계: 개발 환경 및 규칙 (10분)
| 순서 | 문서 경로 | 설명 |
|------|-----------|------|
| 1️⃣4️⃣ | `/documents/MICROSERVICES_SETUP.md` | Docker Compose로 6개 서비스 구동 (14KB) |
| 1️⃣5️⃣ | `/documents/CONVENTIONS.md` | **필수** - Git 전략, 커밋 규칙, 네이밍 컨벤션 |
| 1️⃣6️⃣ | `/documents/SRC_STRUCTURE.md` | SOLID + AOP 아키텍처 패턴 (40KB) |
| 1️⃣7️⃣ | `/SECURITY_GUIDELINES.md` | KISA 보안 코딩, JWT, 암호화 표준 |

### 6단계: 개발 일정 및 계획 (5분)
| 순서 | 문서 경로 | 설명 |
|------|-----------|------|
| 1️⃣8️⃣ | `/documents/DEVELOPMENT_ROADMAP.md` | 7주 개발 타임라인 (Gantt 차트) |
| 1️⃣9️⃣ | `/diagrams/08-development-timeline.mmd` | 마일스톤 시각화 |

### 추가 참고 자료 (필요시)
| 문서 경로 | 설명 |
|-----------|------|
| `/FIGMA_GUIDE.md` | Figma 플러그인 설치 가이드 |
| `/figma-plugin/INSTALL.md` | 커스텀 Figma 플러그인 (자동 React 컴포넌트 생성) |
| `/diagrams/03-drug-food-interaction.mmd` | 약물-음식 상호작용 감지 로직 |
| `/diagrams/04-family-network.mmd` | 가족 네트워크 구조 (WebSocket) |
| `/diagrams/05-ocr-pipeline.mmd` | 처방전 인식 파이프라인 |
| `/diagrams/06-notification-system.mmd` | Kafka 기반 알림 시스템 |
| `/diagrams/09-tech-stack.mmd` | 기술 스택 마인드맵 |

---

## 🌿 Git 브랜치 전략

```
main (production-ready)
 ↑
develop (통합 브랜치)
 ↑
feature/#이슈번호-기능설명-개발자명
```

### 예시
```bash
feature/#12-medication-list-jihoon
feature/#23-family-network-somin
feature/#34-ocr-integration-minjae
```

### 브랜치 생성 명령
```bash
git checkout -b feature/#이슈번호-기능설명-개발자명
```

---

## 💬 커밋 메시지 규칙

### 형식
```
emoji Type: Brief description

Detailed explanation (optional)

Relates: #이슈번호
```

### 커밋 타입 및 이모지
| Type | Emoji | 설명 | 예시 |
|------|-------|------|------|
| **Feat** | ✨ | 새로운 기능 추가 | `✨ Feat: Add medication reminder push notification` |
| **Fix** | 🐛 | 버그 수정 | `🐛 Fix: Resolve drug interaction API timeout` |
| **Docs** | 📝 | 문서 수정 | `📝 Docs: Update API endpoint in README` |
| **Style** | 💄 | 코드 포맷팅 (기능 변경 없음) | `💄 Style: Apply Prettier formatting` |
| **Refactor** | ♻️ | 코드 리팩토링 | `♻️ Refactor: Extract OCR service logic` |
| **Test** | ✅ | 테스트 추가/수정 | `✅ Test: Add unit tests for Family Service` |
| **Chore** | 🔧 | 빌드 스크립트, 설정 변경 | `🔧 Chore: Update Docker Compose config` |
| **Perf** | ⚡ | 성능 개선 | `⚡ Perf: Optimize database query in Medication Service` |
| **CI** | 👷 | CI/CD 파이프라인 | `👷 CI: Add GitHub Actions workflow` |
| **Revert** | ⏪ | 이전 커밋 되돌리기 | `⏪ Revert: Undo changes to notification service` |

### 커밋 예시
```bash
git commit -m "✨ Feat: Add real-time medication sync with Hocuspocus

Implement Y.js CRDT integration for conflict-free
collaborative editing between senior and caregiver.

Relates: #45"
```

---

## 🔗 외부 저장소 링크

| 저장소 | 용도 | URL |
|--------|------|-----|
| **Front** | React 프론트엔드 + 프로젝트 문서 | `https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front` |
| **Back** | Spring Boot 마이크로서비스 백엔드 | `https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Back` |
| **.github** (현재) | 조직 프로필, 문서 아카이브, 다이어그램 | `https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github` |

---

## 🚀 빠른 시작 명령어

### Frontend (React + Vite)
```bash
cd Front/
npm install
npm run dev  # http://localhost:5173
```

### Backend (Docker Compose - 6개 서비스)
```bash
cd Back/
docker-compose up -d

# 서비스 확인
docker ps

# 로그 확인
docker-compose logs -f [service-name]
```

### 데이터베이스 접속
```bash
# MySQL
mysql -h localhost -P 3306 -u root -p

# PostgreSQL
psql -h localhost -p 5432 -U postgres -d amapill_sync

# Redis
redis-cli -h localhost -p 6379
```

---

## 📦 주요 디렉토리 구조 (.github)

```
/home/user/.github/
├── README.md                           # 프로젝트 소개
├── QUICKSTART.md                       # 5분 셋업 가이드
├── FIGMA_GUIDE.md                      # Figma 플러그인 가이드
├── WIREFRAME_SCREENS.md                # UI/UX 화면 명세 (10개)
├── DB스킬.md                           # 데이터베이스 ERD 가이드
├── SECURITY_GUIDELINES.md              # KISA 보안 코딩
│
├── documents/                          # 📁 상세 명세서 (11개)
│   ├── PROJECT_SPECIFICATION.md        # ⭐ 핵심 요구사항 (75KB)
│   ├── ARCHITECTURE.md                 # ⭐ 시스템 설계 (27KB)
│   ├── MICROSERVICES_SETUP.md          # Docker Compose 설정
│   ├── MVP_DTO_SPECIFICATION.md        # ⭐ API 엔드포인트 (19KB)
│   ├── DEVELOPMENT_ROADMAP.md          # 개발 타임라인
│   ├── FRONTEND_COMPONENTS_SPECIFICATION.md
│   ├── CONVENTIONS.md                  # ⭐ Git/커밋 규칙
│   ├── CHAT_API_SPECIFICATION.md       # WebSocket 프로토콜
│   ├── SRC_STRUCTURE.md                # SOLID + AOP 패턴 (40KB)
│   └── 페르소나설정.md                 # 사용자 시나리오
│
├── diagrams/                           # 📁 Mermaid 다이어그램 (11개)
│   ├── 01-system-architecture.mmd      # 전체 토폴로지
│   ├── 02-data-flow.mmd                # 실시간 동기화
│   ├── 03-drug-food-interaction.mmd    # 상호작용 감지
│   ├── 04-family-network.mmd           # 가족 네트워크
│   ├── 05-ocr-pipeline.mmd             # OCR 파이프라인
│   ├── 06-notification-system.mmd      # Kafka 알림
│   ├── 07-database-erd-v6.2.mmd        # ⭐ 최신 ERD (v6.2)
│   ├── 08-development-timeline.mmd     # Gantt 차트
│   └── 09-tech-stack.mmd               # 기술 스택
│
├── figma-exports/                      # Figma 와이어프레임 내보내기
│   ├── original/
│   └── v2/
│
├── figma-plugin/                       # 커스텀 Figma 플러그인
│   ├── code.js / code.ts               # 플러그인 구현
│   ├── ui.html                         # 플러그인 UI
│   ├── manifest.json
│   ├── INSTALL.md                      # 설치 가이드
│   └── create-plugin-zip.sh            # 자동화 스크립트
│
├── profile/
│   └── README.md                       # 조직 프로필
│
└── .github/
    ├── ISSUE_TEMPLATE/                 # GitHub 이슈 템플릿
    ├── PULL_REQUEST_TEMPLATE.md        # PR 템플릿
    └── milestones.json                 # 마일스톤 정의
```

---

## 🎯 AI Agent 작업 시 주의사항

### ✅ 해야 할 것
1. **문서 우선 읽기**: 코드 작성 전 `PROJECT_SPECIFICATION.md`, `ARCHITECTURE.md`, `CONVENTIONS.md` 필독
2. **ERD 참조**: DB 스키마 변경 시 `diagrams/07-database-erd-v6.2.mmd` 확인
3. **API 명세 준수**: 새 엔드포인트는 `MVP_DTO_SPECIFICATION.md` 형식 따르기
4. **보안 가이드 준수**: `SECURITY_GUIDELINES.md`의 KISA 보안 코딩 표준 적용
5. **커밋 규칙 준수**: 이모지 + Type 형식 사용
6. **브랜치 전략 준수**: `feature/#이슈-설명-개발자` 형식
7. **MyBatis 규칙 준수**: Model은 POJO로 생성 (@Entity 사용 안 함), Repository는 @Mapper 인터페이스
8. **MSA 인증 사용**: Controller에서 `SecurityUtil`로 X-User-* 헤더에서 사용자 정보 추출

### ❌ 하지 말아야 할 것
1. **문서 경로 변경 금지**: 외부에서 참조 중 (링크 깨짐 방지)
2. **기존 링크 변경 금지**: 문서 내 링크는 순서만 변경 가능, URL 변경 불가
3. **임의 기술 스택 변경 금지**: `PROJECT_SPECIFICATION.md`의 기술 결정 사항은 팀 합의 필요
4. **ERD 직접 수정 금지**: 데이터베이스 스키마는 팀 검토 후 변경
5. **단독 main 브랜치 푸시 금지**: 반드시 PR 리뷰 후 머지

### 🔍 디버깅 체크리스트
- [ ] 서비스 간 통신 실패 → Eureka Discovery 등록 확인
- [ ] WebSocket 연결 실패 → STOMP/Hocuspocus 엔드포인트 확인
- [ ] 실시간 동기화 안 됨 → Y.js 상태 및 PostgreSQL 연결 확인
- [ ] 약물-음식 상호작용 안 됨 → 식약처 API 키 및 Diet Service 로그 확인
- [ ] OCR 실패 → Google Vision API 할당량 및 Tesseract 폴백 로직 확인

---

## 📞 질문 및 지원

| 문의 사항 | 참고 문서 |
|-----------|-----------|
| 프로젝트 전체 개요 | `/README.md`, `/documents/PROJECT_SPECIFICATION.md` |
| 시스템 아키텍처 | `/documents/ARCHITECTURE.md` |
| API 엔드포인트 | `/documents/MVP_DTO_SPECIFICATION.md` |
| 개발 환경 구축 | `/QUICKSTART.md`, `/documents/MICROSERVICES_SETUP.md` |
| Git/커밋 규칙 | `/documents/CONVENTIONS.md` |
| 보안 표준 | `/SECURITY_GUIDELINES.md` |
| UI/UX 디자인 | `/WIREFRAME_SCREENS.md`, `/FIGMA_GUIDE.md` |
| 데이터베이스 | `/DB스킬.md`, `/diagrams/07-database-erd-v5.mmd` |

---

## 🏷️ 태그 및 라벨

GitHub 이슈/PR에서 사용하는 라벨:

| 라벨 | 용도 |
|------|------|
| `enhancement` | 새로운 기능 |
| `bug` | 버그 수정 |
| `documentation` | 문서 업데이트 |
| `frontend` | React 프론트엔드 |
| `backend` | Spring Boot 백엔드 |
| `database` | DB 스키마 변경 |
| `security` | 보안 관련 |
| `performance` | 성능 최적화 |
| `devops` | Docker, CI/CD |
| `urgent` | 긴급 처리 필요 |

---

## 📚 추가 학습 자료

### 핵심 기술 스택 공식 문서
- [React 19 공식 문서](https://react.dev/)
- [Vite 공식 문서](https://vitejs.dev/)
- [Hocuspocus (Y.js WebSocket Server)](https://tiptap.dev/hocuspocus)
- [Spring Boot 3.4 문서](https://spring.io/projects/spring-boot)
- [Spring Cloud 2024.0.2 (Moorgate)](https://spring.io/projects/spring-cloud)
- [Apache Kafka 공식 문서](https://kafka.apache.org/documentation/)

### 아키텍처 패턴
- **Microservices**: `/documents/ARCHITECTURE.md` 참조
- **SOLID + AOP**: `/documents/SRC_STRUCTURE.md` 참조
- **CRDT (Y.js)**: [Y.js 공식 문서](https://docs.yjs.dev/)
- **Event-Driven Architecture**: Kafka + Spring Cloud Stream

---

**✨ 이 문서는 AI Agent가 프로젝트를 빠르게 이해하고 효율적으로 작업할 수 있도록 작성되었습니다.**

**📍 경로 및 링크는 외부 참조를 위해 고정되어 있으므로 변경하지 마세요.**
