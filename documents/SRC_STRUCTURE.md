# AMApill Frontend Project Structure

## 📐 Architecture Overview

프론트엔드 전용 프로젝트 구조입니다. React 19 + Vite + JSX 아키텍처를 사용합니다.

### 기술 스택
- **Framework**: React 19 (JSX only, NO TypeScript)
- **번들러**: Vite 5
- **상태 관리**: Zustand (전역 상태) + React Query (서버 상태)
- **스타일링**: **MUI 7.3.5 + Emotion** (Tailwind/Sass 제거됨)
- **HTTP 클라이언트**: Axios
- **실시간 통신**: STOMP WebSocket (채팅) + SSE(EventSource, 알림)
- **폼 관리**: React Hook Form + Zod
- **날짜 처리**: date-fns

---

## 🎨 Frontend Structure (React + JSX)

```
src/
├── main.jsx                         # Application entry point
├── App.jsx                          # Root component
│
├── core/                            # Core utilities (DI principle)
│   ├── config/
│   │   ├── api.config.js           # API base URL, timeout
│   │   ├── routes.config.js        # Route definitions
│   │   ├── constants.js            # Global constants
│   │   └── environment.config.js   # Environment settings
│   │
│   ├── services/api/               # API 클라이언트 (16개 도메인 + 공통)
│   │   ├── ApiClient.js            # 추상 클래스 (Mock 지원)
│   │   ├── httpClient.js           # Axios 래퍼
│   │   ├── authApiClient.js        # 로그인/회원가입/Kakao OAuth
│   │   ├── medicationApiClient.js  # 약 CRUD
│   │   ├── medicationLogApiClient.js # 복용 로그
│   │   ├── prescriptionApiClient.js # 처방전
│   │   ├── familyApiClient.js      # 가족 관리
│   │   ├── publicInviteApiClient.js # 공개 초대/수락
│   │   ├── familyChatApiClient.js  # 가족 채팅(REST)
│   │   ├── dietApiClient.js        # 식단 관리
│   │   ├── diseaseApiClient.js     # 질병 관리
│   │   ├── searchApiClient.js      # 약/증상 검색
│   │   ├── ocrApiClient.js         # 처방전 OCR
│   │   ├── chatApiClient.js        # 채팅
│   │   ├── reportApiClient.js      # 순응도 리포트
│   │   ├── notificationApiClient.js # 알림(SSE)
│   │   ├── notificationSettingsApiClient.js # 알림 설정
│   │   └── voiceApiClient.js       # Voice
│   │
│   ├── interceptors/               # Request/Response interceptors
│   │   ├── authInterceptor.js      # JWT token injection
│   │   └── errorInterceptor.js     # Global error handling
│   │
│   ├── routing/
│   │   ├── PrivateRoute.jsx        # Route protection
│   │   └── navigation.js           # Navigation utilities
│   │
│   └── utils/                      # Utility functions
│       ├── formatting.js           # 데이터 포맷팅
│       ├── validation.js           # 유효성 검증
│       ├── errorHandler.js         # 에러 핸들링
│       └── stringUtils.js          # 문자열 유틸
│
├── features/                        # Feature-based modules (14개)
│   │
│   ├── auth/                        # 인증 (Login, Signup, RoleSelection, KakaoCallback)
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── SignupForm.jsx
│   │   │   ├── KakaoLoginButton.jsx
│   │   │   └── RoleSelector.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── store/
│   │   │   └── authStore.js        # Zustand store
│   │   └── pages/
│   │       ├── LoginPage.jsx
│   │       ├── SignupPage.jsx
│   │       ├── RoleSelectionPage.jsx
│   │       └── KakaoCallbackPage.jsx
│   │
│   ├── dashboard/                   # 대시보드 (SeniorDashboard, CaregiverDashboard)
│   │   ├── components/
│   │   │   ├── senior/
│   │   │   │   ├── TodayMedicationChecklist.jsx
│   │   │   │   ├── AvoidFoodList.jsx
│   │   │   │   ├── DiseaseList.jsx
│   │   │   │   └── MedicationScheduleTimeline.jsx
│   │   │   └── caregiver/
│   │   │       ├── SeniorStatusCard.jsx
│   │   │       ├── AlertCenter.jsx
│   │   │       ├── WeeklyAdherenceChart.jsx
│   │   │       └── QuickActionButtons.jsx
│   │   └── pages/
│   │       ├── SeniorDashboard.jsx
│   │       └── CaregiverDashboard.jsx
│   │
│   ├── medication/                  # 약 관리
│   │   ├── components/
│   │   │   ├── MedicationList.jsx
│   │   │   ├── MedicationCard.jsx
│   │   │   ├── MedicationForm.jsx
│   │   │   ├── MedicationDetailModal.jsx
│   │   │   ├── ScheduleInput.jsx
│   │   │   └── InventoryTracker.jsx
│   │   ├── hooks/
│   │   │   ├── useMedications.js
│   │   │   ├── useMedicationLogs.js
│   │   │   └── useMedicationSchedule.js
│   │   ├── store/
│   │   │   └── medicationStore.js
│   │   └── pages/
│   │       ├── MedicationListPage.jsx
│   │       ├── MedicationAddPage.jsx
│   │       └── MedicationDetailPage.jsx
│   │
│   ├── family/                      # 가족 관리
│   │   ├── components/
│   │   │   ├── FamilyGroupCard.jsx
│   │   │   ├── FamilyMemberCard.jsx
│   │   │   ├── InviteMemberForm.jsx
│   │   │   └── MemberRoleSelector.jsx
│   │   ├── hooks/
│   │   │   ├── useFamily.js
│   │   │   └── useFamilySync.js
│   │   ├── context/
│   │   │   └── FamilyContext.jsx
│   │   └── pages/
│   │       └── FamilyManagementPage.jsx
│   │
│   ├── diet/                        # 식단 관리
│   │   ├── components/
│   │   │   ├── MealInputForm.jsx
│   │   │   ├── MealHistory.jsx
│   │   │   ├── FoodConflictWarning.jsx
│   │   │   └── AlternativeSuggestion.jsx
│   │   ├── hooks/
│   │   │   ├── useDiet.js
│   │   │   └── useConflictCheck.js
│   │   └── pages/
│   │       └── DietLogPage.jsx
│   │
│   ├── disease/                     # 질병 관리
│   │   ├── components/
│   │   │   ├── SymptomSearchInput.jsx
│   │   │   ├── SuspectedDiseaseCard.jsx
│   │   │   ├── DiseaseRestrictionsList.jsx
│   │   │   └── PharmacyRecommendation.jsx
│   │   ├── hooks/
│   │   │   └── useDiseases.js
│   │   └── pages/
│   │       ├── SymptomSearchPage.jsx
│   │       ├── SuspectedDiseasePage.jsx
│   │       ├── MyDiseasesPage.jsx
│   │       └── DiseaseRestrictionsPage.jsx
│   │
│   ├── search/                      # 검색
│   │   ├── components/
│   │   │   ├── PillSearchForm.jsx
│   │   │   ├── PillSearchResult.jsx
│   │   │   └── PillDetailModal.jsx
│   │   ├── hooks/
│   │   │   └── useSearch.js
│   │   └── pages/
│   │       └── PillSearchPage.jsx
│   │
│   ├── ocr/                         # 처방전 스캔
│   │   ├── components/
│   │   │   ├── ImageUploader.jsx
│   │   │   ├── OCRResultPreview.jsx
│   │   │   └── ManualCorrection.jsx
│   │   ├── hooks/
│   │   │   └── useOCR.js
│   │   └── pages/
│   │       └── PrescriptionScanPage.jsx
│   │
│   ├── chat/                        # 채팅
│   │   ├── components/
│   │   │   ├── ChatRoomList.jsx
│   │   │   ├── ChatRoomCard.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   └── ChatInput.jsx
│   │   ├── hooks/
│   │   │   └── useChat.js
│   │   └── pages/
│   │       ├── PharmacistChatListPage.jsx
│   │       └── ChatConversationPage.jsx
│   │
│   ├── counsel/                     # 상담
│   │   ├── components/
│   │   │   └── CounselBookingForm.jsx
│   │   ├── hooks/
│   │   │   └── useCounsel.js
│   │   └── pages/
│   │       └── CounselBookingPage.jsx
│   │
│   ├── notification/                # 알림
│   │   ├── components/
│   │   │   ├── NotificationBell.jsx
│   │   │   ├── NotificationList.jsx
│   │   │   └── NotificationItem.jsx
│   │   ├── hooks/
│   │   │   └── useNotifications.js
│   │   └── pages/
│   │       └── NotificationListPage.jsx
│   │
│   ├── report/                      # 리포트
│   │   ├── components/
│   │   │   ├── AdherenceChart.jsx
│   │   │   ├── WeeklyTrendChart.jsx
│   │   │   └── PDFDownloadButton.jsx
│   │   ├── hooks/
│   │   │   └── useAdherenceReport.js
│   │   └── pages/
│   │       └── AdherenceReportPage.jsx
│   │
│   └── settings/                    # 설정
│       ├── components/
│       │   ├── SettingsMenu.jsx
│       │   ├── ProfileEditForm.jsx
│       │   └── NotificationSettings.jsx
│       └── pages/
│           ├── SettingsPage.jsx
│           ├── ProfileEditPage.jsx
│           └── NotificationSettingsPage.jsx
│
├── shared/                          # Shared components
│   └── components/
│       ├── ErrorBoundary.jsx        # Error handling
│       ├── ErrorFallback.jsx        # Error UI
│       │
│       ├── layout/
│       │   ├── MainLayout.jsx
│       │   ├── Header.jsx
│       │   └── BottomNavigation.jsx  # (Sidebar, Footer 없음)
│       │
│       ├── ui/
│       │   ├── Button.jsx
│       │   ├── Card.jsx
│       │   ├── Input.jsx
│       │   ├── Modal.jsx
│       │   ├── Icon.jsx
│       │   ├── BackButton.jsx        # 뒤로가기 버튼
│       │   ├── FAB.jsx               # Floating Action Button
│       │   ├── MenuGroup.jsx         # 메뉴 그룹
│       │   ├── QuickActions.jsx      # 빠른 액션 버튼
│       │   └── Tabs.jsx              # 탭 컴포넌트
│       │
│       └── toast/                    # (feedback/ 대신 toast/)
│           ├── Toast.jsx
│           ├── ToastContainer.jsx
│           └── toastStore.js         # Toast 상태 관리
│
├── mocks/                           # Mock 데이터 (13개)
│   ├── mockMedications.js           # 약 샘플 데이터
│   ├── mockFamily.js                # 가족 그룹/멤버
│   ├── mockDiet.js                  # 식단 로그
│   ├── mockDiseases.js              # 질병 데이터베이스
│   ├── mockSymptoms.js              # 증상 검색 데이터
│   ├── mockNotifications.js         # 알림 메시지
│   ├── mockFoodWarnings.js          # 약-음식 상호작용
│   ├── mockChats.js                 # 채팅 메시지
│   ├── mockChat.js                  # 단일 채팅 데이터
│   ├── mockPillDetails.js           # 알약 외형 데이터
│   ├── mockReports.js               # 순응도 통계
│   ├── mockSearchResults.js         # 검색 결과
│   └── mockOcr.js                   # OCR 결과 샘플
│
├── routing/
│   ├── AppRouter.jsx
│   ├── PrivateRoute.jsx
│   ├── PublicRoute.jsx
│   └── routes.js
│
├── assets/
│   ├── images/
│   ├── icons/
│   └── fonts/
│
└── styles/
    ├── main.scss
    ├── variables.scss
    ├── mixins.scss
    ├── reset.scss
    └── components/
        ├── _button.scss
        ├── _form.scss
        └── _card.scss
```

---

## 📦 API 클라이언트 목록 (19개)

| 파일명 | 담당 기능 |
|--------|----------|
| `ApiClient.js` | 추상 클래스 (Mock 지원) |
| `httpClient.js` | Axios 래퍼 |
| `authApiClient.js` | 로그인/회원가입/Kakao OAuth |
| `medicationApiClient.js` | 약 CRUD |
| `familyApiClient.js` | 가족 관리 |
| `dietApiClient.js` | 식단 관리 |
| `diseaseApiClient.js` | 질병 관리 |
| `searchApiClient.js` | 약/증상 검색 |
| `ocrApiClient.js` | 처방전 OCR |
| `chatApiClient.js` | 채팅 |
| `counselApiClient.js` | 상담 예약 |
| `reportApiClient.js` | 순응도 리포트 |
| `notificationApiClient.js` | 알림 |

---

## 📁 Mock 데이터 파일 목록 (13개)

| 파일명 | 내용 |
|--------|------|
| `mockMedications.js` | 약 샘플 데이터 |
| `mockFamily.js` | 가족 그룹/멤버 |
| `mockDiet.js` | 식단 로그 |
| `mockDiseases.js` | 질병 데이터베이스 |
| `mockSymptoms.js` | 증상 검색 데이터 |
| `mockNotifications.js` | 알림 메시지 |
| `mockFoodWarnings.js` | 약-음식 상호작용 |
| `mockChats.js` | 채팅 메시지 |
| `mockChat.js` | 단일 채팅 데이터 |
| `mockPillDetails.js` | 알약 외형 데이터 |
| `mockReports.js` | 순응도 통계 |
| `mockSearchResults.js` | 검색 결과 |
| `mockOcr.js` | OCR 결과 샘플 |

---

## 🗂️ Features 모듈 요약 (13개)

| Feature | 설명 | 주요 페이지 |
|---------|------|------------|
| `auth` | 인증 | Login, Signup, RoleSelection, KakaoCallback |
| `dashboard` | 대시보드 | SeniorDashboard, CaregiverDashboard |
| `medication` | 약 관리 | MedicationList, MedicationAdd, MedicationDetail |
| `family` | 가족 관리 | FamilyManagement |
| `diet` | 식단 관리 | DietLog |
| `disease` | 질병 관리 | SymptomSearch, SuspectedDisease, MyDiseases |
| `search` | 검색 | PillSearch |
| `ocr` | 처방전 스캔 | PrescriptionScan |
| `chat` | 채팅 | PharmacistChatList, ChatConversation |
| `counsel` | 상담 | CounselBooking |
| `notification` | 알림 | NotificationList, SSE 연동 |
| `report` | 리포트 | AdherenceReport |
| `settings` | 설정 | Settings, ProfileEdit, NotificationSettings |
| `voice` | 음성 명령 **(NEW)** | VoiceAssistant, useVoiceRecognition |

---

## 📝 File Naming Conventions

### Frontend (JavaScript/JSX)
- **Components**: PascalCase + `.jsx`
  - `MedicationList.jsx`, `LoginForm.jsx`
- **Hooks**: camelCase + `use` prefix + `.js`
  - `useMedication.js`, `useAuth.js`
- **Stores (Zustand)**: camelCase + `Store` suffix + `.js`
  - `authStore.js`, `medicationStore.js`
- **API Clients**: camelCase + `ApiClient` suffix + `.js`
  - `authApiClient.js`, `medicationApiClient.js`
- **Utils**: camelCase + `.js`
  - `formatting.js`, `validation.js`
- **Constants**: UPPER_SNAKE_CASE
  - `API_ENDPOINTS`, `ERROR_CODES`

---

## 🚀 Key Takeaways

1. **Feature-based Modules**: auth, dashboard, medication 등 13개 기능별 모듈
2. **Zustand for State**: 전역 상태 관리는 Zustand 사용
3. **React Query for Server State**: 서버 데이터는 React Query로 관리
4. **API Clients**: 12개의 기능별 API 클라이언트
5. **Mock Data**: 13개의 Mock 데이터 파일로 개발 지원
6. **Shared Components**: 재사용 가능한 UI 컴포넌트

---

**Version**: 3.0
**Last Updated**: 2025-12-13
**Author**: AMApill Development Team
