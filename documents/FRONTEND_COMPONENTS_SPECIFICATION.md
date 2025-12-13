# 뭐냑? 프론트엔드 컴포넌트 정의서

> Frontend Components Specification for AMApill Platform
>
> React 19 + Vite + JSX Architecture

---

## 📋 목차

1. [개요](#-개요)
2. [프로젝트 구조](#-프로젝트-구조)
3. [화면별 컴포넌트 트리](#-화면별-컴포넌트-트리)
4. [공통 컴포넌트 라이브러리](#-공통-컴포넌트-라이브러리)
5. [상태 관리](#-상태-관리)
6. [API 연동](#-api-연동)
7. [라우팅 구조](#-라우팅-구조)
8. [컴포넌트 Props 명세](#-컴포넌트-props-명세)

---

## 🎯 개요

### 기술 스택
- **Framework**: React 19 (JSX only, NO TypeScript)
- **번들러**: Vite
- **상태 관리**: Zustand (전역 상태) + React Query (서버 상태)
- **스타일링**: **MUI 7.3.5** (SCSS/Tailwind에서 점진적 전환 중)
- **폼 관리**: React Hook Form
- **날짜 처리**: date-fns
- **HTTP 클라이언트**: Axios

### 디자인 시스템
- **화면 크기**: 1200px × 800px (Desktop First)
- **그리드**: 8px 기반
- **색상**: Green (#4CAF50), Blue (#2196F3), Red (#F44336), Orange (#FF9800)
- **폰트**: Inter (Bold, SemiBold, Regular, Medium)
- **코너 반경**: 12px (카드), 8px (버튼)

---

## 📂 프로젝트 구조

```
src/
├── main.jsx                      # Entry point
├── App.jsx                       # Root component
│
├── core/                         # Core utilities
│   ├── config/
│   │   ├── api.config.js
│   │   ├── routes.config.js
│   │   ├── constants.js
│   │   └── environment.config.js
│   │
│   ├── services/api/             # API 클라이언트 (19개)
│   │   ├── ApiClient.js          # 추상 클래스 (Mock 지원)
│   │   ├── httpClient.js         # Axios 래퍼
│   │   ├── authApiClient.js      # 로그인/회원가입/Kakao OAuth
│   │   ├── medicationApiClient.js
│   │   ├── familyApiClient.js
│   │   ├── dietApiClient.js
│   │   ├── diseaseApiClient.js
│   │   ├── searchApiClient.js
│   │   ├── ocrApiClient.js       # OCR API 클라이언트
│   │   ├── chatApiClient.js
│   │   ├── counselApiClient.js
│   │   ├── reportApiClient.js
│   │   ├── notificationApiClient.js
│   │   └── voiceApiClient.js     # 음성 명령 API
│   │
│   ├── interceptors/
│   │   ├── authInterceptor.js
│   │   └── errorInterceptor.js
│   │
│   ├── routing/
│   │   ├── PrivateRoute.jsx
│   │   └── navigation.js
│   │
│   └── utils/
│       ├── formatting.js
│       ├── validation.js
│       ├── errorHandler.js
│       └── stringUtils.js
│
├── features/                     # Feature modules (14개)
│   ├── auth/
│   │   ├── components/
│   │   │   ├── KakaoLoginButton.jsx
│   │   │   └── RoleSelector.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── store/
│   │   │   └── authStore.js      # Zustand Store
│   │   └── pages/
│   │       ├── LoginPage.jsx
│   │       ├── SignupPage.jsx
│   │       ├── RoleSelectionPage.jsx
│   │       └── KakaoCallbackPage.jsx
│   │
│   ├── dashboard/
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
│   ├── medication/
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
│   │   └── pages/
│   │       ├── MedicationListPage.jsx
│   │       ├── MedicationAddPage.jsx
│   │       └── MedicationDetailPage.jsx
│   │
│   ├── ocr/
│   │   ├── components/
│   │   │   ├── ImageUploader.jsx
│   │   │   ├── OCRResultPreview.jsx
│   │   │   └── ManualCorrection.jsx
│   │   ├── hooks/
│   │   │   └── useOCR.js
│   │   └── pages/
│   │       └── PrescriptionScanPage.jsx
│   │
│   ├── diet/
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
│   ├── family/
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
│   ├── disease/
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
│   ├── search/
│   │   ├── components/
│   │   │   ├── PillSearchForm.jsx
│   │   │   ├── PillSearchResult.jsx
│   │   │   └── PillDetailModal.jsx
│   │   ├── hooks/
│   │   │   └── useSearch.js
│   │   └── pages/
│   │       └── PillSearchPage.jsx
│   │
│   ├── chat/
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
│   ├── counsel/
│   │   ├── components/
│   │   │   └── CounselBookingForm.jsx
│   │   ├── hooks/
│   │   │   └── useCounsel.js
│   │   └── pages/
│   │       └── CounselBookingPage.jsx
│   │
│   ├── report/
│   │   ├── components/
│   │   │   ├── AdherenceChart.jsx
│   │   │   ├── WeeklyTrendChart.jsx
│   │   │   └── PDFDownloadButton.jsx
│   │   ├── hooks/
│   │   │   └── useAdherenceReport.js
│   │   └── pages/
│   │       └── AdherenceReportPage.jsx
│   │
│   ├── settings/
│   │   ├── components/
│   │   │   ├── SettingsMenu.jsx
│   │   │   ├── ProfileEditForm.jsx
│   │   │   └── NotificationSettings.jsx
│   │   └── pages/
│   │       ├── SettingsPage.jsx
│   │       ├── ProfileEditPage.jsx
│   │       └── NotificationSettingsPage.jsx
│   │
│   └── notification/
│       ├── components/
│       │   ├── NotificationBell.jsx
│       │   ├── NotificationList.jsx
│       │   └── NotificationItem.jsx
│       ├── hooks/
│       │   └── useNotifications.js
│       └── pages/
│           └── NotificationListPage.jsx
│
├── features/voice/               # 음성 명령 (신규)
│   ├── components/
│   │   ├── VoiceAssistant.jsx
│   │   └── VoiceVisualizer.jsx
│   ├── hooks/
│   │   └── useVoiceRecognition.js
│   └── store/
│       └── voiceStore.js
│
├── shared/                       # Shared components
│   └── components/
│       ├── ErrorBoundary.jsx
│       ├── ErrorFallback.jsx
│       │
│       ├── layout/
│       │   ├── MainLayout.jsx
│       │   ├── Header.jsx
│       │   └── BottomNavigation.jsx
│       │
│       ├── ui/
│       │   ├── Button.jsx
│       │   ├── Card.jsx
│       │   ├── Input.jsx
│       │   ├── Modal.jsx
│       │   ├── Icon.jsx
│       │   ├── BackButton.jsx
│       │   ├── FAB.jsx
│       │   ├── MenuGroup.jsx
│       │   ├── QuickActions.jsx
│       │   └── Tabs.jsx
│       │
│       └── toast/
│           ├── Toast.jsx
│           ├── ToastContainer.jsx
│           └── toastStore.js
│
├── mocks/                        # Mock 데이터 (13개)
│   ├── mockMedications.js
│   ├── mockFamily.js
│   ├── mockDiet.js
│   ├── mockDiseases.js
│   ├── mockSymptoms.js
│   ├── mockNotifications.js
│   ├── mockFoodWarnings.js
│   ├── mockChats.js
│   ├── mockChat.js
│   ├── mockPillDetails.js
│   ├── mockReports.js
│   ├── mockSearchResults.js
│   └── mockOcr.js
│
├── routing/
│   ├── AppRouter.jsx
│   ├── PrivateRoute.jsx
│   ├── PublicRoute.jsx
│   └── routes.js
│
└── styles/
    ├── main.scss
    ├── variables.scss
    ├── mixins.scss
    └── components/
```

---

## 🌲 화면별 컴포넌트 트리

### 1. 인증 (Auth)

#### 01. 카카오 로그인 (`/login`)
```
LoginPage
└── MainLayout (no nav)
    ├── Header
    └── KakaoLoginButton
        └── Button (variant="kakao")
```

#### 02. 역할 선택 (`/role-selection`)
```
RoleSelectionPage
└── MainLayout (no nav)
    ├── Header
    └── RoleSelector
        ├── Card (senior)
        └── Card (caregiver)
```

---

### 2. 대시보드 (Dashboard)

#### 03. 시니어 대시보드 (`/dashboard/senior`)
```
SeniorDashboard
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    │   └── NotificationBell
    ├── FAB (OCR 스캔)
    ├── AvoidFoodList
    │   └── Card[]
    ├── TodayMedicationChecklist
    │   └── MedicationCheckItem[]
    │       ├── Card
    │       └── CheckboxButton
    ├── DiseaseList
    │   └── Tabs
    ├── MedicationScheduleTimeline
    │   └── TimelineItem[]
    └── BottomNavigation
```

#### 04. 보호자 대시보드 (`/dashboard/caregiver`)
```
CaregiverDashboard
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    │   └── NotificationBell
    ├── SeniorStatusCard
    │   ├── Avatar
    │   └── StatusBadge
    ├── AlertCenter
    │   └── Card[]
    ├── FamilyMemberList
    │   └── FamilyMemberCard[]
    ├── WeeklyAdherenceChart
    │   └── BarChart
    ├── QuickActions
    │   ├── Button (약 등록)
    │   └── Button (가족 초대)
    └── BottomNavigation
```

---

### 3. 약 관리 (Medication)

#### 05. 약 관리 메인 (`/medications`)
```
MedicationListPage
└── MainLayout (BottomNav: 약관리 활성화)
    ├── Header
    │   └── Button (+ 약 등록)
    ├── Input (검색)
    ├── Tabs
    │   ├── Tab (전체)
    │   ├── Tab (복용 중)
    │   └── Tab (종료)
    ├── MedicationList
    │   └── MedicationCard[]
    │       ├── Card
    │       ├── InventoryTracker
    │       └── MenuGroup
    │           ├── Button (편집)
    │           └── Button (삭제)
    └── BottomNavigation
```

#### 06. 약 등록 (`/medications/add`)
```
MedicationAddPage
└── MainLayout (BottomNav: 약관리 활성화)
    ├── Header
    │   └── BackButton
    ├── Tabs
    │   ├── Tab (OCR 스캔)
    │   ├── Tab (알약 검색)
    │   └── Tab (수동 입력)
    ├── [Tab Content]
    │   ├── ImageUploader (OCR)
    │   ├── PillSearchForm (검색)
    │   └── MedicationForm (수동)
    └── BottomNavigation
```

---

### 4. OCR 및 알약 검색

#### 11. 처방전 스캔 (`/prescription/scan`)
```
PrescriptionScanPage
└── MainLayout (no nav during scan)
    ├── Header
    │   └── BackButton
    ├── ImageUploader
    │   ├── DragDropZone
    │   ├── FileInput
    │   └── PreviewImage
    └── Button (스캔 시작)
```

#### 13. 알약 역검색 (`/pill/search`)
```
PillSearchPage
└── MainLayout (BottomNav: 약관리 활성화)
    ├── Header
    │   └── BackButton
    ├── PillSearchForm
    │   ├── Input (모양)
    │   ├── Input (색상)
    │   ├── Input (앞면 각인)
    │   └── Input (뒷면 각인)
    ├── Button (검색)
    ├── PillSearchResult[]
    │   └── PillCard[]
    │       ├── Card
    │       ├── Image (알약 사진)
    │       └── InfoSection
    └── BottomNavigation
```

---

### 5. 식단 관리 (Diet)

#### 21. 식단 입력 (`/diet/log`)
```
DietLogPage
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    │   └── BackButton
    ├── MealInputForm
    │   ├── Input (식사 구분)
    │   ├── Input (음식 이름)
    │   └── Button (추가)
    ├── MealHistory
    │   └── Card[]
    └── BottomNavigation
```

---

### 6. 가족 관리 (Family)

#### 07. 가족 관리 (`/family`)
```
FamilyManagementPage
└── MainLayout (BottomNav: 가족 활성화)
    ├── Header
    │   └── Button (+ 가족 초대)
    ├── FamilyGroupCard
    │   ├── Card
    │   ├── GroupName
    │   └── CreatedBy
    ├── FamilyMemberList
    │   └── FamilyMemberCard[]
    │       ├── Card
    │       ├── Avatar
    │       ├── InfoSection
    │       └── MenuGroup
    │           ├── Button (상세)
    │           └── Button (제거)
    └── BottomNavigation
```

---

### 7. 증상 검색 & 질병 관리 (Disease)

#### 11. 증상 검색 (`/symptom/search`)
```
SymptomSearchPage
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    ├── SymptomSearchInput
    │   ├── Input (증상 입력)
    │   └── Button (검색)
    ├── QuickActions (인기 증상)
    └── BottomNavigation
```

---

### 8. 약사 채팅 (Pharmacist Chat)

#### 09. 약사 채팅 목록 (`/chat/pharmacist`)
```
PharmacistChatListPage
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    │   └── Button (+ 새 상담)
    ├── ChatRoomList
    │   └── ChatRoomCard[]
    │       ├── Card
    │       ├── PharmacistAvatar
    │       └── InfoSection
    └── BottomNavigation
```

#### 10. 약사 1:1 대화 (`/chat/:roomId`)
```
ChatConversationPage (No Bottom Nav)
└── MainLayout
    ├── Header
    │   ├── BackButton
    │   └── PharmacistInfo
    ├── ChatMessageList
    │   └── ChatMessage[]
    │       ├── Avatar (상대방)
    │       └── MessageBubble
    └── ChatInput
        ├── TextArea
        └── Button (전송)
```

---

### 9. 리포트 (Report)

#### 21. 복약 순응도 리포트 (`/report/adherence`)
```
AdherenceReportPage
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    │   └── PDFDownloadButton
    ├── DateRangePicker
    ├── Card (전체 순응도)
    ├── AdherenceChart
    └── BottomNavigation
```

---

### 10. 알림 (Notifications)

#### 33. 알림 목록 (`/notifications`)
```
NotificationListPage
└── MainLayout (BottomNav: 홈 활성화)
    ├── Header
    │   └── Button (모두 읽음)
    ├── Tabs
    │   ├── Tab (전체)
    │   ├── Tab (약 복용)
    │   ├── Tab (식단 경고)
    │   └── Tab (가족 알림)
    ├── NotificationList
    │   └── NotificationItem[]
    │       ├── Card
    │       ├── Icon (type별)
    │       └── InfoSection
    └── BottomNavigation
```

---

### 11. 설정 (Settings)

#### 08. 설정 메인 (`/settings`)
```
SettingsPage
└── MainLayout (BottomNav: 설정 활성화)
    ├── Header
    ├── ProfileSection
    │   ├── Avatar
    │   ├── Name
    │   └── Email
    ├── MenuGroup
    │   ├── MenuItem (프로필 편집)
    │   ├── MenuItem (알림 설정)
    │   ├── MenuItem (내 약 관리)
    │   ├── MenuItem (내 질병 관리)
    │   ├── MenuItem (개인정보처리방침)
    │   ├── MenuItem (이용약관)
    │   └── MenuItem (로그아웃)
    └── BottomNavigation
```

---

---

### 12. 음성 명령 (Voice)

#### 99. 음성 비서 (Global Overlay)
```
VoiceAssistant (App.jsx Level)
├── MicrophoneButton (FAB)
├── VoiceVisualizer (Listening State)
└── ResultFeedback (Toast/Modal)
```

---

## 🧩 공통 컴포넌트 라이브러리

### UI 기본 컴포넌트 (10개)

#### Button
```jsx
// src/shared/components/ui/Button.jsx
<Button
  variant="primary|secondary|danger|kakao|outline"
  size="sm|md|lg"
  fullWidth={boolean}
  disabled={boolean}
  loading={boolean}
  onClick={function}
  icon={ReactNode}
>
  children
</Button>
```

#### Input
```jsx
// src/shared/components/ui/Input.jsx
<Input
  type="text|password|email|number|tel|date|time"
  placeholder={string}
  value={string}
  onChange={function}
  error={string}
  disabled={boolean}
  icon={ReactNode}
  fullWidth={boolean}
/>
```

#### Card
```jsx
// src/shared/components/ui/Card.jsx
<Card
  variant="default|outlined|elevated"
  padding="sm|md|lg"
  onClick={function}
  hoverable={boolean}
>
  children
</Card>
```

#### Modal
```jsx
// src/shared/components/ui/Modal.jsx
<Modal
  isOpen={boolean}
  onClose={function}
  size="sm|md|lg|xl"
  closeOnOverlay={boolean}
  title={string}
>
  children
</Modal>
```

#### Icon
```jsx
// src/shared/components/ui/Icon.jsx
<Icon
  name={string}
  size="sm|md|lg"
  color={string}
/>
```

#### BackButton
```jsx
// src/shared/components/ui/BackButton.jsx
<BackButton
  onClick={function}
  to={string}
/>
```

#### FAB (Floating Action Button)
```jsx
// src/shared/components/ui/FAB.jsx
<FAB
  icon={ReactNode}
  onClick={function}
  position="bottom-right|bottom-left"
/>
```

#### MenuGroup
```jsx
// src/shared/components/ui/MenuGroup.jsx
<MenuGroup>
  <MenuItem icon={Icon} label="메뉴 1" onClick={function} />
  <MenuItem icon={Icon} label="메뉴 2" onClick={function} />
</MenuGroup>
```

#### QuickActions
```jsx
// src/shared/components/ui/QuickActions.jsx
<QuickActions>
  <QuickActionButton icon={Icon} label="액션 1" onClick={function} />
  <QuickActionButton icon={Icon} label="액션 2" onClick={function} />
</QuickActions>
```

#### Tabs
```jsx
// src/shared/components/ui/Tabs.jsx
<Tabs
  activeTab={string}
  onChange={function}
  items={[{key, label}]}
/>
```

---

### 레이아웃 컴포넌트

#### MainLayout
```jsx
// src/shared/components/layout/MainLayout.jsx
<MainLayout
  showBottomNav={boolean}
  showHeader={boolean}
>
  children
</MainLayout>
```

#### Header
```jsx
// src/shared/components/layout/Header.jsx
<Header>
  <HeaderLeft>
    <BackButton />
  </HeaderLeft>
  <HeaderCenter>
    <PageTitle />
  </HeaderCenter>
  <HeaderRight>
    <NotificationBell />
  </HeaderRight>
</Header>
```

#### BottomNavigation
```jsx
// src/shared/components/layout/BottomNavigation.jsx
<BottomNavigation activeTab="home|medications|family|settings">
  <NavItem icon={HomeIcon} label="홈" to="/dashboard" />
  <NavItem icon={PillIcon} label="약관리" to="/medications" />
  <NavItem icon={FamilyIcon} label="가족" to="/family" />
  <NavItem icon={SettingsIcon} label="설정" to="/settings" />
</BottomNavigation>
```

---

### Toast 컴포넌트

#### Toast
```jsx
// src/shared/components/toast/Toast.jsx
<Toast
  type="success|info|warning|error"
  message={string}
  duration={number}
  onClose={function}
/>
```

#### ToastContainer
```jsx
// src/shared/components/toast/ToastContainer.jsx
<ToastContainer position="top-right|top-center|bottom-right" />
```

#### toastStore (Zustand)
```javascript
// src/shared/components/toast/toastStore.js
import { create } from 'zustand'

export const useToastStore = create((set) => ({
  toasts: [],
  addToast: (toast) => set((state) => ({
    toasts: [...state.toasts, { id: Date.now(), ...toast }]
  })),
  removeToast: (id) => set((state) => ({
    toasts: state.toasts.filter(t => t.id !== id)
  }))
}))

// Usage
export const toast = {
  success: (message) => useToastStore.getState().addToast({ type: 'success', message }),
  error: (message) => useToastStore.getState().addToast({ type: 'error', message }),
  info: (message) => useToastStore.getState().addToast({ type: 'info', message }),
  warning: (message) => useToastStore.getState().addToast({ type: 'warning', message })
}
```

---

### 피드백 컴포넌트

#### ErrorBoundary
```jsx
// src/shared/components/ErrorBoundary.jsx
<ErrorBoundary fallback={<ErrorFallback />}>
  children
</ErrorBoundary>
```

#### ErrorFallback
```jsx
// src/shared/components/ErrorFallback.jsx
<ErrorFallback
  error={Error}
  resetErrorBoundary={function}
/>
```

---

## 🔄 상태 관리

### Zustand Store 구조

#### authStore (인증)
```javascript
// src/features/auth/store/authStore.js
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      isAuthenticated: false,
      role: null,  // 'senior' | 'caregiver'
      loading: false,

      // Actions
      login: (userData, token) => set({
        user: userData,
        token,
        isAuthenticated: true,
        role: userData.role
      }),

      logout: () => set({
        user: null,
        token: null,
        isAuthenticated: false,
        role: null
      }),

      setRole: (role) => set({ role }),

      updateUser: (userData) => set((state) => ({
        user: { ...state.user, ...userData }
      })),

      setLoading: (loading) => set({ loading })
    }),
    {
      name: 'auth-storage',  // localStorage key
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
        role: state.role
      })
    }
  )
)
```

#### FamilyContext (가족 - Context 유지)
```javascript
// src/features/family/context/FamilyContext.jsx
import { createContext, useContext, useState } from 'react'

const FamilyContext = createContext()

export const FamilyProvider = ({ children }) => {
  const [familyGroup, setFamilyGroup] = useState(null)
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchFamilyGroup = async () => { /* ... */ }
  const inviteMember = async (email, role) => { /* ... */ }
  const removeMember = async (memberId) => { /* ... */ }

  return (
    <FamilyContext.Provider value={{
      familyGroup,
      members,
      loading,
      fetchFamilyGroup,
      inviteMember,
      removeMember
    }}>
      {children}
    </FamilyContext.Provider>
  )
}

export const useFamily = () => useContext(FamilyContext)
```

---

### React Query 사용

```javascript
// src/features/medication/hooks/useMedications.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { medicationApiClient } from '@/core/services/api/medicationApiClient'

export const useMedications = () => {
  const queryClient = useQueryClient()

  // 약 목록 조회
  const { data: medications, isLoading, error } = useQuery({
    queryKey: ['medications'],
    queryFn: medicationApiClient.getAll
  })

  // 약 등록
  const createMutation = useMutation({
    mutationFn: medicationApiClient.create,
    onSuccess: () => {
      queryClient.invalidateQueries(['medications'])
    }
  })

  // 약 수정
  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => medicationApiClient.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['medications'])
    }
  })

  // 약 삭제
  const deleteMutation = useMutation({
    mutationFn: medicationApiClient.delete,
    onSuccess: () => {
      queryClient.invalidateQueries(['medications'])
    }
  })

  return {
    medications,
    isLoading,
    error,
    createMedication: createMutation.mutate,
    updateMedication: updateMutation.mutate,
    deleteMedication: deleteMutation.mutate
  }
}
```

---

## 🌐 API 연동

### API Client 구조

#### ApiClient (Base - Mock 지원)
```javascript
// src/core/services/api/ApiClient.js
import axios from 'axios'
import { API_BASE_URL, USE_MOCK } from '@/core/config/api.config'

export class ApiClient {
  constructor(baseURL = API_BASE_URL) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // Request Interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('accessToken')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response Interceptor
    this.client.interceptors.response.use(
      (response) => response.data,
      async (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
        }
        return Promise.reject(error)
      }
    )
  }

  async get(url, config) {
    return this.client.get(url, config)
  }

  async post(url, data, config) {
    return this.client.post(url, data, config)
  }

  async put(url, data, config) {
    return this.client.put(url, data, config)
  }

  async delete(url, config) {
    return this.client.delete(url, config)
  }
}
```

#### medicationApiClient
```javascript
// src/core/services/api/medicationApiClient.js
import { ApiClient } from './ApiClient'

class MedicationApiClient extends ApiClient {
  async getAll() {
    return this.get('/api/medications')
  }

  async getById(id) {
    return this.get(`/api/medications/${id}`)
  }

  async create(data) {
    return this.post('/api/medications', data)
  }

  async update(id, data) {
    return this.put(`/api/medications/${id}`, data)
  }

  async delete(id) {
    return this.delete(`/api/medications/${id}`)
  }
}

export const medicationApiClient = new MedicationApiClient()
```

---

## 🚦 라우팅 구조

### Routes Configuration
```javascript
// src/routing/routes.js
export const routes = {
  // Auth
  LOGIN: '/login',
  SIGNUP: '/signup',
  ROLE_SELECTION: '/role-selection',
  KAKAO_CALLBACK: '/auth/kakao/callback',

  // Dashboard
  DASHBOARD_SENIOR: '/dashboard/senior',
  DASHBOARD_CAREGIVER: '/dashboard/caregiver',

  // Medications
  MEDICATIONS: '/medications',
  MEDICATION_ADD: '/medications/add',
  MEDICATION_DETAIL: '/medications/:id',

  // OCR & Search
  PRESCRIPTION_SCAN: '/prescription/scan',
  PILL_SEARCH: '/pill/search',

  // Diet
  DIET_LOG: '/diet/log',

  // Family
  FAMILY: '/family',

  // Disease
  SYMPTOM_SEARCH: '/symptom/search',
  SUSPECTED_DISEASE: '/disease/suspected',
  MY_DISEASES: '/diseases/my',
  DISEASE_RESTRICTIONS: '/diseases/:id/restrictions',

  // Chat
  PHARMACIST_CHAT_LIST: '/chat/pharmacist',
  CHAT_CONVERSATION: '/chat/:roomId',

  // Counsel
  COUNSEL_BOOKING: '/counsel/booking',

  // Report
  ADHERENCE_REPORT: '/report/adherence',

  // Notifications
  NOTIFICATIONS: '/notifications',

  // Settings
  SETTINGS: '/settings',
  PROFILE_EDIT: '/settings/profile',
  NOTIFICATION_SETTINGS: '/settings/notifications'
}
```

---

## 📝 컴포넌트 Props 명세

### MedicationCard Props
```javascript
// src/features/medication/components/MedicationCard.jsx
MedicationCard.propTypes = {
  medication: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    dosage: PropTypes.string,
    timing: PropTypes.string,
    remaining: PropTypes.number,
    quantity: PropTypes.number
  }).isRequired,
  onEdit: PropTypes.func,
  onDelete: PropTypes.func,
  onClick: PropTypes.func
}
```

### Button Props
```javascript
// src/shared/components/ui/Button.jsx
Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger', 'kakao', 'outline']),
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  fullWidth: PropTypes.bool,
  disabled: PropTypes.bool,
  loading: PropTypes.bool,
  onClick: PropTypes.func,
  icon: PropTypes.node,
  type: PropTypes.oneOf(['button', 'submit', 'reset'])
}

Button.defaultProps = {
  variant: 'primary',
  size: 'md',
  fullWidth: false,
  disabled: false,
  loading: false,
  type: 'button'
}
```

### Card Props
```javascript
// src/shared/components/ui/Card.jsx
Card.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['default', 'outlined', 'elevated']),
  padding: PropTypes.oneOf(['sm', 'md', 'lg']),
  onClick: PropTypes.func,
  hoverable: PropTypes.bool
}

Card.defaultProps = {
  variant: 'default',
  padding: 'md',
  hoverable: false
}
```

---

## 🎨 스타일링 가이드

### SCSS Variables
```scss
// src/styles/variables.scss

// Colors
$color-primary: #4CAF50;      // Green
$color-secondary: #2196F3;    // Blue
$color-danger: #F44336;       // Red
$color-warning: #FF9800;      // Orange
$color-kakao: #FEE500;        // Kakao Yellow

$color-gray-50: #FAFAFA;
$color-gray-100: #F5F5F5;
$color-gray-200: #EEEEEE;
$color-gray-300: #E0E0E0;
$color-gray-400: #BDBDBD;
$color-gray-500: #9E9E9E;
$color-gray-600: #757575;
$color-gray-700: #616161;
$color-gray-800: #424242;
$color-gray-900: #212121;

// Spacing (8px grid)
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 20px;
$spacing-xl: 30px;
$spacing-2xl: 40px;

// Border Radius
$radius-sm: 4px;
$radius-md: 8px;
$radius-lg: 12px;
$radius-xl: 16px;
$radius-full: 9999px;

// Typography
$font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

$font-size-xs: 12px;
$font-size-sm: 14px;
$font-size-md: 16px;
$font-size-lg: 20px;
$font-size-xl: 24px;
$font-size-2xl: 32px;

$font-weight-regular: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;
```

---

## 📖 참고 문서

- [SRC_STRUCTURE.md](./SRC_STRUCTURE.md) - 전체 소스 구조
- [WIREFRAME_SCREENS.md](./WIREFRAME_SCREENS.md) - 와이어프레임 명세
- [MVP_DTO_SPECIFICATION.md](./MVP_DTO_SPECIFICATION.md) - API 및 DTO 명세
- [CHAT_API_SPECIFICATION.md](./CHAT_API_SPECIFICATION.md) - 채팅 API 명세
- [ARCHITECTURE.md](./ARCHITECTURE.md) - 시스템 아키텍처
- [CONVENTIONS.md](./CONVENTIONS.md) - 프로젝트 컨벤션

---

**작성일**: 2025-11-07
**최종 수정일**: 2025-11-22
**버전**: 2.0 (Zustand 상태관리, 컴포넌트 구조 업데이트)
**작성자**: 뭐냑? 개발팀
