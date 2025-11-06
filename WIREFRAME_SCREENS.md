# 실버케어 와이어프레임 - 전체 화면 목록

## 📱 MVP 핵심 화면 (Phase 1)

### 🔐 인증 (Auth)
1. **로그인 페이지** - `05-login`
2. **회원가입 페이지** - `06-signup`
3. **역할 선택 (시니어/보호자)** - `07-role-selection`

### 🏠 대시보드 (Dashboard)
4. **시니어 대시보드** - `01-dashboard-senior` ✅
5. **보호자 대시보드** - `02-dashboard-caregiver` ✅

### 💊 약 관리 (Medication)
6. **약 관리 메인** - `03-medications` ✅
7. **약 등록 폼 (OCR 버튼 포함)** - `08-medication-add`
8. **약 상세 정보** - `09-medication-detail`
9. **약 편집** - `10-medication-edit`
10. **약 리뷰/후기** - `10-medication-reviews` 🆕

### 📷 처방전 스캔 (OCR)
11. **처방전 스캔** - `11-prescription-scan`
12. **OCR 결과 확인/수정** - `12-ocr-result`

### 🔍 알약 검색 (Pill Search)
13. **알약 역검색** - `13-pill-search`
14. **검색 결과** - `14-pill-result`
15. **약 상세 모달** - `15-pill-detail-modal`

### 🔬 증상 검색 & 질병 관리 (🆕 신규 기능)
16. **증상 검색** - `16-symptom-search` 🆕
17. **의심 질환 결과** - `17-suspected-disease` 🆕
18. **약국 상담 추천** - `18-pharmacy-advice` 🆕
19. **내 질병 관리** - `19-my-diseases` 🆕
20. **질병별 기피 음식/약** - `20-disease-restrictions` 🆕

### 🍽️ 식단 & 충돌 경고 (Diet)
21. **식단 입력** - `21-meal-input`
22. **음식 충돌 경고** - `22-food-warning`
23. **대체 음식 제안** - `23-alternative-suggestion`
24. **병원 공식 식단 자료** - `24-hospital-diet-resources` 🆕

### 👨‍👩‍👧 가족 관리 (Family)
25. **가족 관리 메인** - `04-family` ✅
26. **가족 초대** - `26-family-invite`
27. **가족 구성원 상세** - `27-family-member-detail`

### 💬 약사 채팅 (🆕 신규 기능)
28. **약사 채팅 메인** - `28-pharmacist-chat` 🆕
29. **채팅방 목록** - `29-chat-rooms` 🆕
30. **약사와 1:1 대화** - `30-chat-conversation` 🆕

### 📊 리포트 (Report)
31. **복약 순응도 리포트** - `31-adherence-report`
32. **주간 통계** - `32-weekly-stats`

### 🔔 알림 (Notifications)
33. **알림 목록** - `33-notifications`
34. **알림 상세** - `34-notification-detail`

### ⚙️ 설정 (Settings)
35. **설정 메인** - `35-settings`
36. **프로필 편집** - `36-profile-edit`
37. **알림 설정** - `37-notification-settings`
38. **내 약 관리 (설정)** - `38-my-medications-settings` 🆕
39. **내 질병 관리 (설정)** - `39-my-diseases-settings` 🆕

---

## 🔄 프로토타입 플로우 (Prototype Flows)

### 메인 플로우
```
로그인 → 역할 선택 → 대시보드 (시니어/보호자)
```

### 시니어 플로우
```
시니어 대시보드 → 약 관리 → 약 복용 체크
시니어 대시보드 → 가족 → 가족 구성원 확인
시니어 대시보드 → 알림 → 알림 확인
```

### 보호자 플로우
```
보호자 대시보드 → 약 관리 → 약 원격 등록
보호자 대시보드 → 약 관리 → 복용 현황 모니터링
보호자 대시보드 → 리포트 → 주간 통계
보호자 대시보드 → 가족 → 가족 초대
```

### 약 등록 플로우
```
약 관리 → 약 등록 → 처방전 스캔 → OCR 결과 → 저장 완료
약 관리 → 약 등록 → 알약 검색 → 검색 결과 → 선택 → 저장
약 관리 → 약 등록 → 수동 입력 → 저장
```

### 식단 입력 플로우
```
대시보드 → 식단 입력 → 자동 충돌 체크 → 경고 없음 → 저장
대시보드 → 식단 입력 → 충돌 발견 → 경고 표시 → 대체 제안 → 저장/취소
```

### 가족 네트워크 플로우
```
가족 관리 → 가족 초대 → 초대 링크 생성 → 공유
가족 관리 → 구성원 선택 → 상세 정보 → 역할 변경
```

---

## 📋 대시보드 상세 기능 명세

### 시니어 대시보드 (`01-dashboard-senior`)
1. **카메라 버튼** (OCR 인식 화면으로 이동)
2. **피해야 할 음식** 목록
3. **복용 중인 약** 목록 (복용 체크 기능)
4. **관리해야 하는 질환** 목록
5. **약 먹는 스케줄** 타임라인
6. **오늘의 식단** 입력/확인

### 보호자 대시보드 (`02-dashboard-caregiver`)
1. **시니어 상태 관리** (실시간 복약 현황)
2. **시니어 설정 관리** (원격 약 등록/수정)
3. **알림 센터** (미복용 알림, 충돌 경고)
4. **가족 구성원** 목록
5. **주간 복약 순응도** 차트
6. **빠른 액션** (약 등록, 가족 초대)

---

## 🎨 디자인 요구사항

### 공통 요소
- **Header**: 로고, 사용자 이름, 알림 아이콘
- **Navigation**: 홈, 약 관리, 가족, 설정
- **Footer**: 저작권, 이용약관, 개인정보처리방침

### 색상 시스템
- Primary (성공): `#4CAF50` (초록)
- Secondary (정보): `#2196F3` (파랑)
- Warning (주의): `#FF9800` (주황)
- Danger (위험): `#F44336` (빨강)
- Accent: `#E91E63` (핑크)

### 타이포그래피
- H1: 32px Bold
- H2: 24px Bold
- Body Large: 20px Regular
- Body Medium: 16px Regular
- Body Small: 14px Regular
- Caption: 12px Regular

### 간격 시스템 (8px Grid)
- xs: 4px
- sm: 8px
- md: 16px
- lg: 20px
- xl: 30px
- 2xl: 40px

---

## ✅ 구현 우선순위

### 🔥 Phase 1 (Week 1-2) - 필수 핵심
- [x] 로그인
- [x] 회원가입
- [x] 시니어 대시보드
- [x] 보호자 대시보드
- [x] 약 관리 메인
- [x] 약 등록 (기본)
- [x] 가족 관리

### ⭐ Phase 2 (Week 3-4) - 차별화 기능
- [ ] 처방전 OCR 스캔
- [ ] 알약 역검색
- [ ] 식단 입력 & 충돌 경고
- [ ] 실시간 동기화 (Hocuspocus)

### 💎 Phase 3 (Week 5-6) - 고도화
- [ ] 복약 순응도 리포트
- [ ] 알림 시스템
- [ ] 설정 페이지
- [ ] PDF 다운로드

---

## 📐 화면 크기
- **Desktop**: 1200px x 800px
- **Mobile**: 375px x 667px (추후)
- **Tablet**: 768px x 1024px (추후)

---

**작성일**: 2025-11-05
**버전**: 1.0
**상태**: 진행중
