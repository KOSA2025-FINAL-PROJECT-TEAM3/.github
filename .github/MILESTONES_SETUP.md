# 📅 마일스톤 설정 가이드

> 프로젝트 마일스톤을 자동으로 생성하는 가이드입니다.

## 📋 목차

- [마일스톤 구조](#마일스톤-구조)
- [설정 방법](#설정-방법)
  - [방법 1: gh CLI 사용 (권장)](#방법-1-gh-cli-사용-권장)
  - [방법 2: GitHub API 직접 사용](#방법-2-github-api-직접-사용)
  - [방법 3: 수동으로 웹에서 생성](#방법-3-수동으로-웹에서-생성)
- [마일스톤 목록](#마일스톤-목록)
- [FAQ](#faq)

---

## 마일스톤 구조

마일스톤은 **7주 개발 기간**을 다음과 같이 나눕니다:

| 마일스톤 | 기간 | 내용 |
|---------|------|------|
| ✅ Phase 1: 기획 및 설계 | Week 1-2 | 프로젝트 기획, 아키텍처 설계 (완료) |
| 🚀 Phase 2: MVP 개발 - Week 1 | Week 3 | Auth Service, 인프라 구축 |
| 💊 Phase 2: MVP 개발 - Week 2 | Week 4 | Medication & Family Service |
| 🍽️ Phase 2: MVP 개발 - Week 3 | Week 5 | Diet Service, OCR |
| 🔔 Phase 2: MVP 개발 - Week 4 | Week 6 | Notification, Dashboard |
| 🧪 Phase 3: 테스트 및 최적화 | Week 7-8 | 통합 테스트, 성능 개선 |
| 🚢 Phase 4: 배포 및 발표 준비 | Week 9-10 | CI/CD, 프로덕션 배포, 발표 |
| 🐛 Hotfix & Maintenance | 상시 | 긴급 버그 수정 |
| 📝 Documentation & Refactoring | 상시 | 문서화, 리팩토링 |
| 🌟 Phase 5: 추가 기능 | Phase 2 이후 | 카카오톡 알림톡, PDF 리포트 등 |

---

## 설정 방법

### 방법 1: gh CLI 사용 (권장)

**가장 간단하고 권장하는 방법입니다.**

#### 1. gh CLI 설치

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt-get install gh

# Windows (Scoop)
scoop install gh

# Windows (Chocolatey)
choco install gh
```

자세한 설치 방법: https://cli.github.com/

#### 2. GitHub 인증

```bash
gh auth login
```

화면의 지시에 따라 로그인하세요.

#### 3. 마일스톤 생성

**Front 저장소에 마일스톤 생성:**
```bash
cd .github
./.github/scripts/setup-milestones-gh.sh Front
```

**Back 저장소에 마일스톤 생성:**
```bash
./.github/scripts/setup-milestones-gh.sh Back
```

**둘 다 생성:**
```bash
./.github/scripts/setup-milestones-gh.sh Front
./.github/scripts/setup-milestones-gh.sh Back
```

#### 4. 확인

- Front: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/milestones
- Back: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Back/milestones

---

### 방법 2: GitHub API 직접 사용

**gh CLI 없이 GitHub API를 직접 호출하는 방법입니다.**

#### 1. Personal Access Token 생성

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token (classic)** 클릭
3. 토큰 이름: `milestone-setup`
4. 권한 선택:
   - ✅ `repo` (Full control of private repositories)
5. **Generate token** 클릭
6. 생성된 토큰 복사 (다시 볼 수 없으니 안전한 곳에 저장!)

#### 2. 환경변수 설정

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

#### 3. 마일스톤 생성

**Front 저장소:**
```bash
cd .github
GITHUB_TOKEN=ghp_xxx ./.github/scripts/setup-milestones-api.sh Front
```

**Back 저장소:**
```bash
GITHUB_TOKEN=ghp_xxx ./.github/scripts/setup-milestones-api.sh Back
```

#### 4. 토큰 삭제 (보안)

```bash
unset GITHUB_TOKEN
```

⚠️ **보안 주의:**
- 토큰은 절대 코드에 하드코딩하지 마세요
- 토큰이 노출되면 즉시 폐기하세요
- 사용 후 환경변수에서 삭제하세요

---

### 방법 3: 수동으로 웹에서 생성

**스크립트를 사용하지 않고 GitHub 웹에서 직접 생성하는 방법입니다.**

#### 1. 저장소 이동

- Front: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/milestones
- Back: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Back/milestones

#### 2. 마일스톤 생성

1. **New milestone** 버튼 클릭
2. 아래 정보 입력 (`.github/milestones.json` 참조)
3. **Create milestone** 클릭

각 마일스톤 정보는 아래 [마일스톤 목록](#마일스톤-목록) 섹션 참조

---

## 마일스톤 목록

### ✅ Phase 1: 기획 및 설계

- **기한**: 2025-11-12
- **상태**: Closed (완료)
- **내용**: 프로젝트 기획, 시스템 아키텍처 설계, 데이터베이스 스키마, API 명세서 작성, 와이어프레임 제작

---

### 🚀 Phase 2: MVP 개발 - Week 1

- **기한**: 2025-11-19
- **상태**: Open
- **내용**:
  - Auth Service 구현 (회원가입, 로그인, JWT)
  - User CRUD API
  - Spring Cloud Gateway 설정
  - Eureka Server 구축
  - React 기본 라우팅 및 Auth 화면
  - MySQL 초기 스키마 적용

**관련 이슈 예시:**
- `[AUTH] JWT 토큰 발급 및 검증 구현`
- `[INFRA] Eureka Server 구축`
- `[FRONTEND] 로그인/회원가입 화면 구현`

---

### 💊 Phase 2: MVP 개발 - Week 2

- **기한**: 2025-11-26
- **상태**: Open
- **내용**:
  - Medication Service 구현
  - 약 등록/수정/삭제 API
  - Family Service 구현
  - 가족 네트워크 초대/수락
  - 실시간 동기화 (Hocuspocus 기본 연동)
  - 약 관리 화면 구현

**관련 이슈 예시:**
- `[MEDICATION] 약 등록 API 구현`
- `[FAMILY] 가족 초대 기능 구현`
- `[FRONTEND] 약 관리 화면 구현`

---

### 🍽️ Phase 2: MVP 개발 - Week 3

- **기한**: 2025-12-03
- **상태**: Open
- **내용**:
  - Diet Service 구현
  - 약-음식 충돌 룰 엔진
  - OCR Service 구현 (Google Vision API)
  - 약봉지 자동 인식 기능
  - 식단 관리 화면
  - 충돌 경고 UI

**관련 이슈 예시:**
- `[DIET] 약-음식 충돌 검사 룰 엔진 구현`
- `[OCR] Google Vision API 연동`
- `[FRONTEND] 식단 관리 화면 구현`

---

### 🔔 Phase 2: MVP 개발 - Week 4

- **기한**: 2025-12-10
- **상태**: Open
- **내용**:
  - Notification Service 구현
  - Kafka 이벤트 기반 알림
  - 대시보드 화면 (시니어/자녀)
  - 복약 현황 모니터링
  - 알림 설정 UI
  - 실시간 알림 표시

**관련 이슈 예시:**
- `[NOTIFICATION] Kafka 이벤트 기반 알림 구현`
- `[FRONTEND] 대시보드 화면 구현`
- `[FRONTEND] 실시간 알림 표시 기능`

---

### 🧪 Phase 3: 테스트 및 최적화

- **기한**: 2025-12-17
- **상태**: Open
- **내용**:
  - E2E 테스트 작성
  - API 통합 테스트
  - 프론트엔드 단위 테스트
  - 성능 프로파일링 및 최적화
  - 버그 수정
  - 코드 리팩토링
  - 보안 점검

**관련 이슈 예시:**
- `[TEST] E2E 테스트 작성`
- `[PERFORMANCE] API 응답 시간 최적화`
- `[SECURITY] 보안 취약점 점검`

---

### 🚢 Phase 4: 배포 및 발표 준비

- **기한**: 2025-12-31
- **상태**: Open
- **내용**:
  - Docker Compose 프로덕션 설정
  - CI/CD 파이프라인 구축
  - 프로덕션 환경 배포
  - 최종 발표 자료 준비
  - 데모 시나리오 작성
  - 발표 리허설

**관련 이슈 예시:**
- `[DEVOPS] CI/CD 파이프라인 구축`
- `[DEVOPS] 프로덕션 배포`
- `[DOCS] 최종 발표 자료 작성`

---

### 🐛 Hotfix & Maintenance

- **기한**: 없음 (상시)
- **상태**: Open
- **내용**: 개발 중 발견된 긴급 버그나 Critical 이슈를 처리합니다.

**사용 예시:**
- Critical 버그 발견 시 즉시 처리
- 프로덕션 환경 긴급 패치
- 보안 취약점 긴급 수정

---

### 📝 Documentation & Refactoring

- **기한**: 없음 (상시)
- **상태**: Open
- **내용**:
  - API 문서 보완
  - 코드 주석 추가
  - README 업데이트
  - 리팩토링
  - 코드 리뷰 반영

**사용 예시:**
- 문서 개선 이슈
- 코드 리팩토링
- 기술 부채 해결

---

### 🌟 Phase 5: 추가 기능 (선택사항)

- **기한**: 2026-01-31 (여유 있게)
- **상태**: Open
- **내용**:
  - 카카오톡 알림톡 연동
  - 복약 순응도 리포트 (PDF)
  - 알약 역검색 기능 (식약처 API)
  - 통계 및 분석 화면
  - 다국어 지원
  - PWA 모바일 앱

**참고**: MVP 완성 후 시간이 허락하면 구현

---

## FAQ

### Q1. 마일스톤은 어디에 생성하나요?

**A**: 각 저장소별로 생성해야 합니다.
- Front 저장소: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/milestones
- Back 저장소: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Back/milestones

Organization 레벨에서는 마일스톤을 설정할 수 없습니다.

---

### Q2. 마일스톤을 수정하고 싶어요

**A**: 두 가지 방법이 있습니다:

**방법 1: GitHub 웹에서 수정**
1. 저장소 → Issues → Milestones
2. 수정할 마일스톤 클릭
3. Edit milestone
4. 내용 수정 후 Save changes

**방법 2: JSON 파일 수정 후 재실행**
1. `.github/milestones.json` 파일 수정
2. 기존 마일스톤은 웹에서 수동 삭제 또는 수정
3. 스크립트 재실행 (새로운 마일스톤만 생성됨)

---

### Q3. 스크립트 실행 시 "이미 존재합니다" 오류가 나요

**A**: 정상입니다. 이미 생성된 마일스톤은 건너뛰고 새로운 것만 생성됩니다.

---

### Q4. Issue를 마일스톤에 어떻게 연결하나요?

**A**: Issue 생성 또는 수정 시 우측 사이드바에서 **Milestone** 선택

또는 Issue 목록에서:
1. Issue 체크박스 선택
2. 상단 Mark as 드롭다운 → Milestone 선택

---

### Q5. 마일스톤 진행률은 어떻게 확인하나요?

**A**:
- Milestone 페이지에서 자동으로 진행률(%) 표시
- 진행률 = (완료된 이슈 수 / 전체 이슈 수) × 100

---

### Q6. 마일스톤을 삭제하려면?

**A**:
1. 저장소 → Issues → Milestones
2. 삭제할 마일스톤 우측 Delete 버튼
3. 확인

⚠️ 주의: 삭제하면 연결된 이슈들의 마일스톤 정보가 사라집니다 (이슈는 삭제되지 않음)

---

### Q7. 팀원들이 마일스톤에 접근할 수 있나요?

**A**: 네! 저장소에 접근 권한이 있는 모든 팀원이:
- 마일스톤 조회 가능
- Issue를 마일스톤에 연결 가능
- Write 권한이 있다면 마일스톤 수정/삭제 가능

---

### Q8. 마일스톤 기한을 놓치면 어떻게 되나요?

**A**:
- GitHub가 자동으로 빨간색으로 표시 (경고)
- 기능적으로는 문제 없음
- 기한 연장이 필요하면 마일스톤 수정

---

## 📞 문의

마일스톤 설정에 문제가 있다면:
- Issue 생성: https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/issues
- 템플릿: `❓ 질문 / 도움 요청` 선택

---

**최종 수정일**: 2025-11-06
**작성자**: KOSA 2025 Team 3
