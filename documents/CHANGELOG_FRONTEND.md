# Frontend Changelog

프론트엔드(Front Repository) 개발 변경사항 추적 문서

---

## [0.1.0] - 2025-11-17

### Added ✨

#### 핵심 페이지 구현 ([#12](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/12))
- **식단 관리 페이지** (Diet Management)
  - 식단 입력 및 관리 기능
  - 약-음식 충돌 경고 UI 기반 마련

- **질병 관리 페이지** (Disease Management)
  - 사용자 질병 정보 등록
  - 복용 중인 약과 질병 연계

- **설정 페이지** (Settings)
  - 프로필 설정
  - 알림 설정
  - 계정 관리

#### UI/UX 개선
- **Wireframe 페이지 스켈레톤** ([#14](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/14))
  - 34개 화면 컴포넌트 기본 구조 생성
  - 라우팅 설정 완료

#### 문서화
- OCR API 명세 추가 (2025-11-10)
- Chat 기능 명세 추가 (2025-11-10)
- Version C ERD 및 비교 문서 추가 (2025-11-10)

### Changed ♻️

#### 아키텍처 개선
- **마이크로서비스 URL 지원** ([#17](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/17))
  - API 클라이언트에 동적 base URL 설정 기능 추가
  - 환경 변수를 통한 각 마이크로서비스 엔드포인트 구성 지원
  - Auth, Medication, Family 등 개별 서비스별 URL 분리

- **사용자 역할 상수화** ([#15](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/15))
  - Signup 페이지의 하드코딩된 역할 문자열을 상수로 변경
  - `src/core/config/constants.js`에 `USER_ROLES` 정의
  - 타입 안정성 및 유지보수성 향상

#### 인프라 업그레이드
- **sass 1.94.0으로 업그레이드** ([#12](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/12))
- **데이터베이스 마이그레이션**: PostgreSQL → MySQL 8.0+ (2025-11-11)

### Fixed 🐛

#### 인증/인가 버그
- **역할 기반 네비게이션 수정** ([#17](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/17))
  - 로그인/가입 후 사용자 역할(노인/보호자)에 따른 페이지 이동 오류 해결
  - 역할 상수를 활용한 조건부 라우팅 로직 개선
  - 인증 후 리다이렉션 플로우 재정비

#### 문서 버그
- **README.md URL 링크 포맷 수정** (2025-11-12)
  - 외부 문서 링크가 GitHub에서 제대로 렌더링되지 않던 문제 해결
  - Markdown 링크 포맷 표준화

- **한글 인코딩 문제 해결** (2025-11-11)
  - 일부 문서 파일에서 한글이 깨져 보이던 문제 수정
  - UTF-8 인코딩 명시적 적용

### Documentation 📝

#### AI Agent 개발 가이드
- **CLAUDE.md 대폭 업데이트** ([#16](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/16))
  - 코드베이스 전체 분석 내용 추가
  - AI Agent를 위한 개발 규칙 및 컨벤션 정리
  - Do's and Don'ts 섹션 추가

#### 문서 구조 개선
- **문서 재구성** ([#13](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/pull/13))
  - AI Agent가 쉽게 참조할 수 있도록 문서 계층 구조 개선
  - docs/ 폴더 내 주요 명세서 정리

- **Chat API 명세 업데이트** (2025-11-11)
  - WebSocket 프로토콜 구현 사항 반영
  - 실시간 메시징 플로우 문서화

### Refactored ♻️

- **코드베이스 전체 네이밍 일관성 개선** (2025-11-11)
  - 컴포넌트, 함수, 변수명 일관성 확보
  - 컨벤션 문서 기준 적용

### Removed 🗑️

- **불필요한 문서 삭제** (2025-11-11)
  - AGENTS.md 삭제
  - 중복/구식 문서 제거

---

## 개발 현황 요약

### 완료된 마일스톤

#### Stage 1: 프로젝트 초기 설정 ✅
- React 19 + Vite 개발 환경 구축
- Zustand 상태 관리 설정
- React Router 라우팅 설정
- Tailwind CSS 스타일링 시스템

#### Stage 2: 인증 시스템 ✅
- 로그인/회원가입 페이지
- JWT 토큰 관리
- Axios Interceptor 설정
- 역할 기반 접근 제어 (RBAC)

#### Stage 3: 핵심 기능 페이지 구현 (진행 중)
- ✅ Diet 관리 페이지
- ✅ Disease 관리 페이지
- ✅ Settings 페이지
- 🔄 Medication 관리 페이지 (진행 중)
- 🔄 Family 관리 페이지 (진행 중)
- 🔄 Dashboard (진행 중)

#### API 연동 준비
- ✅ 마이크로서비스 URL 지원
- ✅ API 클라이언트 인프라 구축
- 🔄 실제 백엔드 API 연동 (대기 중)

### 현재 이슈

#### 1. AuthContext vs Zustand 구조 결정 필요
**상태**: 논의 중
**내용**: 문서에는 AuthContext 구조가 명시되어 있으나, 현재 구현은 Zustand만 사용 중. 팀 표준 결정 필요.

#### 2. OCR Stage 4 플로우 재구성 필요
**상태**: 백엔드 API 대기 중
**내용**: OCR 업로더, 미리보기, 수동 교정 UI 및 백엔드 연동 전략 수립 필요.

---

## 기술 부채 및 개선 계획

### 우선순위: 높음
- [ ] 실제 백엔드 API 연동 (Mock → Real API)
- [ ] WebSocket 실시간 동기화 구현
- [ ] 에러 바운더리 및 폴백 UI

### 우선순위: 중간
- [ ] 단위 테스트 및 통합 테스트 작성
- [ ] 접근성 (a11y) 개선
- [ ] 성능 최적화 (Code Splitting, Lazy Loading)

### 우선순위: 낮음
- [ ] Storybook 도입 (컴포넌트 문서화)
- [ ] E2E 테스트 (Playwright)
- [ ] PWA 지원

---

## 다음 스프린트 계획

### Week 5 (예정)
- Medication CRUD 완성
- Family 네트워크 기능 구현
- Dashboard 통계 차트 연동
- OCR 페이지 재설계

### Week 6 (예정)
- 실시간 알림 시스템 (WebSocket)
- 복약 순응도 리포트 생성
- 약-음식 충돌 경고 UI

### Week 7 (예정)
- 통합 테스트
- 버그 수정
- 성능 최적화
- 배포 준비

---

## 참고 링크

- **Frontend Repository**: [KOSA2025-FINAL-PROJECT-TEAM3/Front](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front)
- **Backend Repository**: [KOSA2025-FINAL-PROJECT-TEAM3/spring-boot](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/spring-boot)
- **Auth Service**: [KOSA2025-FINAL-PROJECT-TEAM3/auth-service](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/auth-service)
- **프로젝트 문서**: [.github Repository](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github)

---

**최종 업데이트**: 2025-11-18
**문서 버전**: 1.0
**관리자**: 뭐냑? 프론트엔드 팀
