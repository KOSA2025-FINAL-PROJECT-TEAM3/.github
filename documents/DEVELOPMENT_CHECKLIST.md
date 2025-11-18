# 🎯 뭐냑? 개발 체크리스트

프로젝트 전체 진행 상황을 한눈에 확인하는 마스터 체크리스트

**최종 업데이트**: 2025-11-18
**전체 진행률**: 🟢 **78%** (Backend 98% + Frontend 45% + DevOps 10%)

---

## 📊 전체 진행 현황

| 영역 | 진행률 | 상태 | 담당 |
|------|--------|------|------|
| **Backend Core** | 98% | 🟢 거의 완료 | 팀원 2 |
| **Frontend** | 45% | 🟡 진행 중 | 팀원 1 |
| **DevOps** | 10% | 🔴 시작 단계 | 팀원 3 |
| **Documentation** | 90% | 🟢 거의 완료 | 전체 |
| **Testing** | 5% | 🔴 미착수 | 전체 |

---

## 🔥 이번 주 우선순위 (Week 4-5)

### Critical (필수)
- [ ] **Backend**: GlobalExceptionHandler 구현 (🔴 긴급)
- [ ] **Backend**: 보안 정보 환경 변수화 (🔴 긴급)
- [ ] **Frontend**: Medication 페이지 완성 (🟡 높음)
- [ ] **Frontend**: Family 페이지 완성 (🟡 높음)
- [ ] **통합**: Frontend ↔ Backend API 연동 테스트 (🟡 높음)

### High (중요)
- [ ] **Backend**: SecurityConfig 인증 활성화
- [ ] **Backend**: MyBatis Optional 이슈 리팩토링
- [ ] **Frontend**: Dashboard 통계 차트 연동
- [ ] **DevOps**: Docker Compose 초기 설정

### Medium (보통)
- [ ] **Backend**: Null Safety 검토
- [ ] **Frontend**: WebSocket 실시간 알림 준비
- [ ] **Documentation**: API 명세 최신화

---

## 🎯 Milestone 별 체크리스트

## Milestone 1: MVP Core ✅ (100% 완료)

### Backend
- [x] Spring Boot 프로젝트 생성
- [x] MySQL 연결 설정
- [x] MyBatis 설정
- [x] Clean Architecture 폴더 구조
- [x] 17개 Entity 생성
- [x] 9개 Repository Interface
- [x] MyBatis Mapper XML 작성

### Frontend
- [x] React 19 + Vite 개발 환경
- [x] Zustand 상태 관리 설정
- [x] React Router 라우팅 설정
- [x] Tailwind CSS 디자인 시스템
- [x] 기본 프로젝트 구조

---

## Milestone 2: 인증 시스템 ✅ (100% 완료)

### Backend
- [x] JWT 토큰 생성/검증
- [x] Kakao OAuth 2.0 연동
- [x] Refresh Token 관리
- [x] Spring Security 기본 설정
- [x] AuthController (회원가입, 로그인, 로그아웃)

### Frontend
- [x] 로그인 페이지
- [x] 회원가입 페이지
- [x] JWT 토큰 관리 (localStorage)
- [x] Axios Interceptor 설정
- [x] 역할 기반 접근 제어 (RBAC)
- [x] 역할 기반 네비게이션

---

## Milestone 3: 핵심 비즈니스 로직 ✅ (100% 완료 - Backend)

### Backend
- [x] 42개 DTO 정의
- [x] 14개 Service Interface
- [x] 15개 Service Implementation
  - [x] FamilyServiceImpl
  - [x] MedicationServiceImpl
  - [x] DietServiceImpl
  - [x] DiseaseServiceImpl
  - [x] NotificationServiceImpl
  - [x] OCRServiceImpl
  - [x] PillIdentificationServiceImpl
  - [x] ReportServiceImpl
  - [x] ChatServiceImpl
  - [x] WebSocketServiceImpl
  - [x] 기타 5개

### Frontend
- [x] Diet 페이지
- [x] Disease 페이지
- [x] Settings 페이지
- [ ] Medication 페이지 (🔄 70%)
- [ ] Family 페이지 (🔄 60%)
- [ ] Dashboard (🔄 40%)

---

## Milestone 4: API Layer ✅ (100% 완료 - Backend)

### Backend
- [x] 11개 REST Controller
  - [x] AuthController
  - [x] UserController
  - [x] FamilyController
  - [x] MedicationController
  - [x] MedicationScheduleController
  - [x] DietController
  - [x] DiseaseController
  - [x] NotificationController
  - [x] OCRController
  - [x] ReportController
  - [x] ChatController
- [x] 2개 WebSocket Endpoint
  - [x] WebSocketController
  - [x] ChatWebSocketHandler
- [x] Swagger API 문서화

### Frontend
- [x] API Client 인프라 구축
- [x] 마이크로서비스 URL 지원
- [x] 에러 핸들링 기본 구조
- [ ] 실제 API 연동 (🔄 30%)

---

## Milestone 5: 품질 보증 🔄 (60% 진행 중)

### Backend
- [x] CLAUDE.md AI 개발 가이드
- [ ] GlobalExceptionHandler 구현 (🔴 0%)
  - [ ] ResourceNotFoundException 핸들러
  - [ ] UnauthorizedException 핸들러
  - [ ] ValidationException 핸들러
  - [ ] 기타 Custom Exception 핸들러
- [ ] 보안 강화 (🔄 40%)
  - [ ] SecurityConfig 인증 활성화
  - [ ] 엔드포인트별 권한 설정
  - [ ] 보안 정보 환경 변수화
- [ ] 코드 품질 개선 (🔄 50%)
  - [ ] MyBatis Optional 이슈 리팩토링
  - [ ] Null Safety 검토 및 수정
  - [ ] 코드 리뷰 반영

### Frontend
- [x] 컴포넌트 구조 정립
- [x] 역할 상수화
- [ ] 에러 바운더리 구현
- [ ] 폴백 UI 구현
- [ ] 접근성 (a11y) 개선

---

## Milestone 6: Testing 🔴 (5% 시작 단계)

### Backend
- [ ] Service Layer 단위 테스트 (🔴 0%)
  - [ ] FamilyServiceImpl 테스트
  - [ ] MedicationServiceImpl 테스트
  - [ ] AuthServiceImpl 테스트
  - [ ] 기타 Service 테스트
- [ ] Controller 통합 테스트 (🔴 0%)
  - [ ] FamilyController 테스트
  - [ ] MedicationController 테스트
  - [ ] AuthController 테스트
- [ ] Repository 테스트 (🔴 0%)
  - [ ] MyBatis Mapper 테스트

### Frontend
- [ ] 컴포넌트 단위 테스트 (🔴 0%)
- [ ] 통합 테스트 (🔴 0%)
- [ ] E2E 테스트 (🔴 0%)

---

## Milestone 7: 성능 최적화 🔴 (0% 미착수)

### Backend
- [ ] N+1 쿼리 최적화
- [ ] 데이터베이스 인덱스 추가
- [ ] Redis 캐싱 전략
- [ ] API 응답 시간 최적화

### Frontend
- [ ] Code Splitting
- [ ] Lazy Loading
- [ ] 이미지 최적화
- [ ] 번들 사이즈 최적화

---

## Milestone 8: DevOps 🔴 (10% 시작 단계)

### Docker
- [ ] Backend Dockerfile (🔄 50%)
- [ ] Frontend Dockerfile
- [ ] Docker Compose 설정
  - [ ] MySQL
  - [ ] Redis
  - [ ] Backend
  - [ ] Frontend

### CI/CD
- [ ] GitHub Actions 워크플로우
  - [ ] Backend 빌드/테스트
  - [ ] Frontend 빌드/테스트
  - [ ] Docker 이미지 빌드
  - [ ] 자동 배포
- [ ] 환경별 설정 분리
  - [ ] Development
  - [ ] Staging
  - [ ] Production

### 모니터링
- [ ] Spring Boot Actuator 설정
- [ ] Prometheus 메트릭
- [ ] 로그 수집 (ELK Stack)
- [ ] 알림 설정 (Slack/Email)

---

## Milestone 9: 프로덕션 배포 🔴 (0% 미착수)

### 인프라
- [ ] AWS/GCP 계정 설정
- [ ] RDS MySQL 인스턴스
- [ ] ElastiCache Redis
- [ ] EC2/GKE 클러스터
- [ ] Load Balancer 설정
- [ ] SSL/TLS 인증서 (Let's Encrypt)

### 보안
- [ ] HTTPS 강제 적용
- [ ] CORS 설정 검토
- [ ] Rate Limiting
- [ ] DDoS 방어
- [ ] 보안 감사 로그

### 백업
- [ ] 데이터베이스 자동 백업
- [ ] 백업 복구 테스트
- [ ] 재해 복구 계획

---

## 📋 기능별 상세 체크리스트

### 가족 관리 (Family) 🟢 90%

#### Backend
- [x] 가족 그룹 생성
- [x] 가족 구성원 초대
- [x] 초대 수락/거절
- [x] 구성원 제거
- [x] 구성원 약 조회
- [x] 권한 검증 로직

#### Frontend
- [x] 가족 그룹 UI 기본 구조
- [ ] 가족 구성원 목록
- [ ] 초대 관리 UI
- [ ] 구성원 약 모니터링

---

### 약 관리 (Medication) 🟢 85%

#### Backend
- [x] 약 CRUD
- [x] 복약 스케줄 생성
- [x] 복약 체크
- [x] 복약 현황 조회
- [x] 약 재고 관리

#### Frontend
- [ ] 약 목록 UI
- [ ] 약 등록 폼
- [ ] 스케줄 캘린더
- [ ] 복약 체크 UI
- [ ] 재고 알림

---

### 식단 관리 (Diet) 🟡 75%

#### Backend
- [x] 식단 기록 CRUD
- [x] 약-음식 충돌 검사 룰 엔진
- [x] 경고 메시지 생성

#### Frontend
- [x] 식단 기록 페이지
- [ ] 약-음식 충돌 경고 UI
- [ ] 대체 음식 추천 UI

---

### 알림 (Notification) 🟡 70%

#### Backend
- [x] 알림 생성
- [x] 알림 조회
- [x] 알림 설정 관리
- [x] WebSocket 푸시

#### Frontend
- [ ] 알림 목록 UI
- [ ] 알림 설정 페이지
- [ ] 실시간 푸시 알림 (WebSocket)
- [ ] 브라우저 알림 (Notification API)

---

### OCR 처방전 🟡 65%

#### Backend
- [x] Google Vision API 연동
- [x] OCR 결과 파싱
- [x] 약 정보 자동 매칭

#### Frontend
- [ ] 파일 업로드 UI (드래그 드롭)
- [ ] OCR 결과 미리보기
- [ ] 수동 교정 UI
- [ ] 약 정보 자동 등록

---

### 리포트 (Report) 🟡 70%

#### Backend
- [x] 복약 순응도 계산
- [x] 통계 데이터 생성
- [x] PDF 리포트 생성

#### Frontend
- [ ] 리포트 조회 UI
- [ ] 통계 차트 (Chart.js/Recharts)
- [ ] PDF 다운로드
- [ ] 의료진 공유 기능

---

### 채팅 (Chat) 🟡 80%

#### Backend
- [x] WebSocket/STOMP 설정
- [x] 채팅 메시지 저장
- [x] 실시간 브로드캐스트

#### Frontend
- [ ] 채팅 UI
- [ ] 실시간 메시지 수신
- [ ] 메시지 히스토리
- [ ] 의사/AI 챗봇 연동

---

## 🐛 Critical Issues (해결 필수)

### Backend
1. **GlobalExceptionHandler 미구현** 🔴
   - **우선순위**: Critical
   - **담당**: 팀원 2
   - **기한**: Week 4
   - **설명**: Custom Exception 핸들러 없어 에러 응답 형식이 불일치

2. **보안 정보 하드코딩** 🔴
   - **우선순위**: Critical
   - **담당**: 팀원 2
   - **기한**: Week 4
   - **설명**: DB 비밀번호, JWT Secret 노출

3. **SecurityConfig 모든 요청 허용** 🔴
   - **우선순위**: High
   - **담당**: 팀원 2
   - **기한**: Week 5
   - **설명**: `.permitAll()` 설정으로 인증 우회 가능

### Frontend
4. **API 연동 미완성** 🟡
   - **우선순위**: High
   - **담당**: 팀원 1
   - **기한**: Week 5
   - **설명**: Mock 데이터 사용 중, 실제 API 연동 필요

5. **WebSocket 실시간 알림 미구현** 🟡
   - **우선순위**: High
   - **담당**: 팀원 1
   - **기한**: Week 6
   - **설명**: 실시간 알림 시스템 구현 필요

---

## 📅 주차별 계획

### Week 4 (현재)
- [ ] Backend: GlobalExceptionHandler 완성
- [ ] Backend: 보안 정보 환경 변수화
- [ ] Frontend: Medication 페이지 완성
- [ ] Frontend: Family 페이지 완성

### Week 5
- [ ] Backend: SecurityConfig 인증 활성화
- [ ] Backend: 단위 테스트 시작
- [ ] Frontend: Dashboard 완성
- [ ] 통합: API 연동 테스트

### Week 6
- [ ] Backend: 통합 테스트
- [ ] Frontend: WebSocket 실시간 알림
- [ ] DevOps: Docker Compose 설정
- [ ] 성능 최적화 시작

### Week 7
- [ ] 전체: 통합 테스트
- [ ] DevOps: CI/CD 파이프라인
- [ ] 배포: 스테이징 환경 배포
- [ ] 발표 자료 준비

---

## 🎓 학습 리소스

### Backend
- [ ] MyBatis 공식 문서 읽기
- [ ] Spring Security 심화 학습
- [ ] JUnit 5 테스트 작성법

### Frontend
- [ ] React 19 새 기능 학습
- [ ] WebSocket/STOMP 클라이언트 구현
- [ ] Chart.js 사용법

### DevOps
- [ ] Docker Compose 튜토리얼
- [ ] GitHub Actions 워크플로우
- [ ] AWS/GCP 배포 가이드

---

## 📊 진행률 계산

```
전체 진행률 = (완료된 체크박스 / 전체 체크박스) × 100

Backend: 180 / 184 = 98%
Frontend: 45 / 100 = 45%
DevOps: 2 / 20 = 10%
Testing: 1 / 20 = 5%
Documentation: 18 / 20 = 90%

전체 평균: (98 + 45 + 10 + 5 + 90) / 5 = 49.6%
가중 평균 (Backend 30%, Frontend 30%, DevOps 20%, Testing 10%, Docs 10%):
= 0.3×98 + 0.3×45 + 0.2×10 + 0.1×5 + 0.1×90
= 29.4 + 13.5 + 2 + 0.5 + 9
= 54.4% → 약 55%
```

**현재 실질 진행률: 55%**

---

## 📞 팀원 역할 분담

| 팀원 | 주 담당 | 부 담당 | 현재 작업 |
|------|---------|---------|-----------|
| **팀원 1** | Frontend | API 연동 | Medication, Family 페이지 |
| **팀원 2** | Backend | Testing | GlobalExceptionHandler, 보안 |
| **팀원 3** | DevOps | Database | Docker, CI/CD 준비 |

---

**최종 업데이트**: 2025-11-18
**다음 검토일**: 2025-11-20 (수요일)
**작성자**: 뭐냑? 개발팀
