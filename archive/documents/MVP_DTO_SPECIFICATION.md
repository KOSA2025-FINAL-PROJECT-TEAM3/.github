# AMApill MVP 기능 및 DTO 명세서

> 가족 돌봄 네트워크 기반 약 관리 플랫폼
> 작성일: 2025-11-05
> 최종 업데이트: 2025-11-14
> 버전: 2.0 (프론트엔드 실제 구현 반영)

---

## 📋 목차

1. [MVP 기능 우선순위](#mvp-기능-우선순위)
2. [API 엔드포인트 목록](#api-엔드포인트-목록)
   - [Auth/User](#1-authuser-인증사용자)
   - [Family](#2-family-가족-관리---mvp-1순위)
   - [Medication](#3-medication-약-관리---mvp-필수)
   - [Diet](#4-diet-식단-관리---mvp-필수)
   - [Drug Interaction](#5-drug-interaction-약-음식-충돌---mvp-2순위)
   - [OCR](#6-ocr-약봉지-인식---mvp-3순위)
   - [Chat](#7-chat-채팅-상담)
   - [Search](#8-search-검색)
   - [Disease](#9-disease-질병-관리)
   - [Counsel](#10-counsel-상담-요청)
   - [Notification](#11-notification-알림)
   - [Report](#12-report-리포트---선택)
3. [DTO 명세](#dto-명세)
4. [아키텍처 참고사항](#아키텍처-참고사항)

---

## 🎯 MVP 기능 우선순위

### 필수 기능 (7주 내 완성)

| 우선순위 | 기능 | 개발 시간 | 차별화 | 상태 |
|---------|------|----------|--------|------|
| 🥇 1순위 | **가족 돌봄 네트워크** | 2주 | ⭐⭐⭐⭐⭐ | ✅ 필수 |
| 🥈 2순위 | **약-음식 충돌 경고** | 1.5주 | ⭐⭐⭐⭐⭐ | ✅ 필수 |
| 🥉 3순위 | **약봉지 OCR 자동 등록** | 1.5주 | ⭐⭐⭐⭐ | ✅ 필수 |
| 4순위 | **알약 역검색** | 1주 | ⭐⭐⭐⭐ | ✅ 필수 |
| 5순위 | 기본 CRUD (약, 스케줄, 로그) | 1주 | ⭐⭐⭐ | ✅ 필수 |

### 선택 기능 (시간 있으면)

| 우선순위 | 기능 | 개발 시간 | 차별화 | 상태 |
|---------|------|----------|--------|------|
| 6순위 | 복약 순응도 리포트 | 3일 | ⭐⭐⭐ | ⚠️ 선택 |
| 7순위 | 약값 절약 비교 | 2일 | ⭐⭐⭐ | ⚠️ 선택 |
| 8순위 | 카카오톡 알림톡 (Phase 2) | 1주 | ⭐⭐⭐⭐ | ⚠️ 선택 |

---

## 🌐 API 엔드포인트 목록

### 1. Auth/User (인증/사용자)

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| POST | `/auth/login` | 일반 로그인 (이메일/비밀번호) | ✅ |
| POST | `/auth/signup` | 일반 회원가입 (자동 로그인) | ✅ |
| POST | `/auth/kakao-login` | 카카오 OAuth 로그인 | ✅ |
| POST | `/auth/select-role` | 역할 선택 (시니어/케어기버) | ✅ |
| POST | `/auth/logout` | 로그아웃 | ✅ |
| POST | `/auth/refresh` | 토큰 갱신 | ✅ |
| GET | `/users/me` | 내 프로필 조회 | ✅ |
| PUT | `/users/me` | 내 프로필 수정 | ✅ |
| DELETE | `/users/me` | 계정 비활성화 | ⚠️ 예정 |

**참고**:
- **API 경로 변경**: `/api/auth/*` → `/auth/*`, `/api/users/*` → `/users/*`
- RefreshToken은 **Redis**에 저장 (MySQL refresh_tokens 테이블 제거)
- JWT Claims에 `userRole`, `customerRole`, `profileImage` 추가

### 2. Family (가족 관리) - MVP 1순위

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/family/` | 가족 그룹 & 멤버 조회 (통합) | ✅ |
| POST | `/api/family/invite` | 가족 구성원 초대 | ✅ |
| DELETE | `/api/family/members/{id}` | 가족 구성원 제거 | ✅ |

**참고**: Zustand store 최적화를 위해 그룹과 멤버 정보를 한 번의 API 호출로 통합 제공

### 3. Medication (약 관리) - MVP 필수

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/medications` | 내 약 목록 조회 (스케줄 포함) | ✅ |
| POST | `/api/medications` | 약 등록 | ✅ |
| PATCH | `/api/medications/{id}` | 약 수정 (부분) | ✅ |
| DELETE | `/api/medications/{id}` | 약 삭제 | ✅ |
| POST | `/api/medications/logs` | 복용 체크 | ⚠️ 예정 |
| GET | `/api/medications/logs` | 복용 로그 조회 (날짜 필터) | ⚠️ 예정 |

**참고**:
- Zustand store에서 medications 배열 관리 (상세 조회 불필요)
- 스케줄은 medication 객체에 포함되어 반환
- 오늘 복용 내역은 클라이언트 사이드에서 필터링

### 4. Diet (식단 관리) - MVP 필수

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/diet/logs` | 식단 내역 조회 | ✅ |
| POST | `/api/diet/logs` | 식단 기록 | ✅ |
| PATCH | `/api/diet/logs/{logId}` | 식단 수정 | ✅ |
| DELETE | `/api/diet/logs/{logId}` | 식단 삭제 | ✅ |
| GET | `/api/diet/warnings` | 약-음식 충돌 경고 조회 | ✅ |

### 5. Drug Interaction (약-음식 충돌) - MVP 2순위

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| POST | `/api/interactions/check` | 약-음식 충돌 검사 | ✅ |
| GET | `/api/interactions/food/{foodName}` | 특정 음식 충돌 조회 | ✅ |

### 6. OCR (약봉지 인식) - MVP 3순위

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| POST | `/api/ocr/recognize` | 약봉지 OCR 인식 | ✅ |
| POST | `/api/ocr/pill-search` | 알약 역검색 (식별정보) | ⚠️ 예정 |

### 7. Chat (채팅 상담)

채팅 API는 별도 문서 참조: [CHAT_API_SPECIFICATION.md](./CHAT_API_SPECIFICATION.md)

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/chat/rooms` | 채팅방 목록 조회 | ✅ |
| POST | `/api/chat/rooms` | 채팅방 생성 (의사/AI 선택) | ✅ |
| GET | `/api/chat/rooms/{roomId}/messages` | 메시지 히스토리 조회 | ✅ |
| POST | `/api/chat/rooms/{roomId}/messages` | 메시지 전송 (REST Fallback) | ✅ |
| PATCH | `/api/chat/rooms/{roomId}/messages/{messageId}/read` | 메시지 읽음 처리 | ✅ |
| DELETE | `/api/chat/rooms/{roomId}` | 채팅방 나가기 | ✅ |

**참고**: 실시간 메시지는 WebSocket (Socket.IO) 사용

### 8. Search (검색)

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/search/symptoms` | 증상 자동완성 검색 | ✅ |
| GET | `/api/search/symptoms/{symptomName}` | 증상 상세 정보 | ✅ |

### 9. Disease (질병 관리)

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/disease/me` | 내 질병 목록 조회 | ✅ |
| GET | `/api/disease/{diseaseId}` | 질병 상세 정보 | ✅ |
| GET | `/api/disease/restrictions/{diseaseId}` | 질병별 식이/약물 제한 정보 | ✅ |

### 10. Counsel (상담 요청)

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| POST | `/api/counsel/submit` | 상담 문의 제출 | ✅ |

### 11. Notification (알림)

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/notifications` | 알림 히스토리 조회 | ⚠️ 예정 |
| PATCH | `/api/notifications/{id}/read` | 알림 읽음 처리 | ⚠️ 예정 |
| DELETE | `/api/notifications/{id}` | 알림 삭제 | ⚠️ 예정 |

**참고**:
- 실시간 알림: WebSocket (`ws://api.amapill.com/notifications`)
- Zustand store에서 알림 상태 관리
- REST API는 과거 알림 조회 및 동기화용

### 12. Report (리포트) - 선택

| Method | Endpoint | 설명 | MVP |
|--------|----------|------|-----|
| GET | `/api/reports/adherence` | 복약 순응도 리포트 | ⚠️ 선택 |
| GET | `/api/reports/adherence/pdf` | 복약 순응도 PDF | ⚠️ 선택 |

---

## 📦 DTO 명세

### 1. Auth/User (인증/사용자)

#### 1.1 KakaoLoginRequest

```json
{
  "authorizationCode": "abc123xyz...",
  "redirectUri": "http://localhost:5173/auth/callback"
}
```

**필드 설명**
- `authorizationCode` (string, required): 카카오 OAuth 인증 코드
- `redirectUri` (string, required): 리다이렉트 URI

**Validation**
- authorizationCode: `@NotBlank`
- redirectUri: `@NotBlank`, `@URL`

---

#### 1.2 LoginResponse (카카오 OAuth 후)

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer",
  "expiresIn": 900,
  "user": {
    "id": 1,
    "email": "senior@example.com",
    "name": "김시니어",
    "profileImage": "https://k.kakaocdn.net/...",
    "userRole": "ROLE_USER",
    "customerRole": "SENIOR"
  }
}
```

**필드 설명**
- `accessToken` (string): JWT 액세스 토큰 (유효기간 15분)
- `refreshToken` (string): JWT 리프레시 토큰 (유효기간 7일, **Redis 저장**)
- `tokenType` (string): 토큰 타입 ("Bearer")
- `expiresIn` (number): 만료 시간(초)
- `user` (object): 사용자 정보
  - `userRole` (string): 시스템 역할 (`ROLE_USER`, `ROLE_ADMIN`)
  - `customerRole` (string): 고객 역할 (`SENIOR`, `CAREGIVER`)

**JWT Access Token Claims**:
```json
{
  "userId": 1,
  "name": "김시니어",
  "email": "senior@example.com",
  "profileImage": "https://k.kakaocdn.net/...",
  "userRole": "ROLE_USER",
  "customerRole": "SENIOR",
  "type": "ACCESS"
}
```

---

#### 1.3 KakaoSignupRequest (OAuth 후 추가 정보 입력)

```json
{
  "kakaoId": "1234567890",
  "phone": "010-1234-5678",
  "role": "caregiver",
  "agreeTerms": true,
  "agreePrivacy": true
}
```

**필드 설명**
- `kakaoId` (string, required): 카카오 사용자 ID (OAuth에서 받은 값)
- `phone` (string, required): 전화번호
- `role` (enum, required): 사용자 역할
  - `senior`: 시니어 (약 복용자)
  - `caregiver`: 자녀/보호자
- `agreeTerms` (boolean, required): 이용약관 동의
- `agreePrivacy` (boolean, required): 개인정보 처리방침 동의

**Validation**
- kakaoId: `@NotBlank`
- phone: `@Pattern(regexp="^01[0-9]-\\d{3,4}-\\d{4}$")`
- role: `@NotNull`
- agreeTerms: `@AssertTrue` (반드시 true)
- agreePrivacy: `@AssertTrue` (반드시 true)

**참고**: 이메일과 이름은 카카오 OAuth에서 자동으로 가져옴

---

#### 1.4 UserResponse

```json
{
  "id": 1,
  "email": "senior@example.com",
  "name": "김시니어",
  "phone": "010-9876-5432",
  "profileImage": "https://k.kakaocdn.net/...",
  "userRole": "ROLE_USER",
  "customerRole": "SENIOR",
  "createdAt": "2025-11-05T10:00:00Z"
}
```

**필드 변경 사항** (auth-service v2.0):
- `role` → `userRole` + `customerRole`로 분리
- `profileImage` 필드 추가

---

### 2. Family (가족 관리)

#### 2.1 FamilyGroupRequest

```json
{
  "name": "김씨 가족"
}
```

**필드 설명**
- `name` (string, required): 가족 그룹 이름

---

#### 2.2 FamilyGroupResponse

```json
{
  "id": 1,
  "name": "김씨 가족",
  "createdBy": {
    "id": 2,
    "name": "이자녀",
    "role": "caregiver"
  },
  "members": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "name": "김시니어",
        "email": "senior@example.com",
        "role": "senior"
      },
      "familyRole": "parent",
      "joinedAt": "2025-11-05T10:00:00Z"
    },
    {
      "id": 2,
      "user": {
        "id": 2,
        "name": "이자녀",
        "email": "caregiver@example.com",
        "role": "caregiver"
      },
      "familyRole": "child",
      "joinedAt": "2025-11-05T10:01:00Z"
    }
  ],
  "createdAt": "2025-11-05T10:00:00Z"
}
```

**필드 설명**
- `id` (number): 가족 그룹 ID
- `name` (string): 가족 그룹 이름
- `createdBy` (object): 그룹 생성자 정보
- `members` (array): 가족 구성원 목록
  - `familyRole`: `parent` (부모) 또는 `child` (자녀)

---

#### 2.3 FamilyMemberInviteRequest

```json
{
  "email": "parent@example.com",
  "familyRole": "parent"
}
```

**필드 설명**
- `email` (string, required): 초대할 사용자 이메일
- `familyRole` (enum, required): 가족 내 역할
  - `parent`: 부모/시니어
  - `child`: 자녀/보호자

---

### 3. Medication (약 관리)

#### 3.1 MedicationRequest

```json
{
  "name": "아스피린",
  "ingredient": "아세틸살리실산",
  "dosage": "100mg",
  "timing": "아침 식후",
  "startDate": "2025-11-01",
  "endDate": "2025-12-01",
  "quantity": 30,
  "remaining": 30,
  "expiryDate": "2026-10-31"
}
```

**필드 설명**
- `name` (string, required): 약 이름
- `ingredient` (string, optional): 주성분
- `dosage` (string, optional): 복용량
- `timing` (string, optional): 복용 시기
- `startDate` (date, required): 복용 시작일
- `endDate` (date, optional): 복용 종료일
- `quantity` (number, optional): 총 개수
- `remaining` (number, optional): 남은 개수
- `expiryDate` (date, optional): 유효기간

---

#### 3.2 MedicationResponse

```json
{
  "id": 1,
  "userId": 1,
  "name": "아스피린",
  "ingredient": "아세틸살리실산",
  "dosage": "100mg",
  "timing": "아침 식후",
  "startDate": "2025-11-01",
  "endDate": "2025-12-01",
  "quantity": 30,
  "remaining": 25,
  "expiryDate": "2026-10-31",
  "schedules": [
    {
      "id": 1,
      "time": "09:00:00",
      "daysOfWeek": "1,2,3,4,5",
      "active": true
    }
  ],
  "createdAt": "2025-11-01T10:00:00Z"
}
```

---

#### 3.3 MedicationScheduleRequest

```json
{
  "time": "09:00:00",
  "daysOfWeek": "1,2,3,4,5",
  "active": true
}
```

**필드 설명**
- `time` (time, required): 복용 시간 (HH:mm:ss)
- `daysOfWeek` (string, optional): 요일 (0=일요일, 1=월요일, ..., 6=토요일)
  - 예: "1,3,5" = 월,수,금
  - 빈 값 = 매일
- `active` (boolean, optional): 활성화 여부 (기본값: true)

---

#### 3.4 MedicationLogRequest

```json
{
  "medicationId": 1,
  "scheduledTime": "2025-11-05T09:00:00Z",
  "completed": true
}
```

**필드 설명**
- `medicationId` (number, required): 약 ID
- `scheduledTime` (timestamp, required): 예정 복용 시간
- `completed` (boolean, required): 복용 완료 여부

---

#### 3.5 MedicationLogResponse

```json
{
  "id": 1,
  "medicationId": 1,
  "medicationName": "아스피린",
  "userId": 1,
  "scheduledTime": "2025-11-05T09:00:00Z",
  "completedTime": "2025-11-05T09:05:32Z",
  "completed": true,
  "missed": false,
  "createdAt": "2025-11-05T09:05:32Z"
}
```

---

#### 3.6 TodayMedicationResponse

```json
{
  "date": "2025-11-05",
  "medications": [
    {
      "medicationId": 1,
      "name": "아스피린",
      "dosage": "100mg",
      "schedules": [
        {
          "time": "09:00:00",
          "scheduledTime": "2025-11-05T09:00:00Z",
          "completed": true,
          "completedTime": "2025-11-05T09:05:32Z"
        },
        {
          "time": "21:00:00",
          "scheduledTime": "2025-11-05T21:00:00Z",
          "completed": false,
          "completedTime": null
        }
      ]
    }
  ],
  "totalScheduled": 6,
  "totalCompleted": 4,
  "completionRate": 66.7
}
```

**필드 설명**
- `date` (date): 조회 날짜
- `medications` (array): 오늘 복용할 약 목록
- `totalScheduled` (number): 총 예정 복용 횟수
- `totalCompleted` (number): 완료된 복용 횟수
- `completionRate` (number): 완료율 (%)

---

### 4. Diet (식단 관리)

#### 4.1 DietLogRequest

```json
{
  "mealType": "breakfast",
  "foodName": "시금치",
  "calories": 150
}
```

**필드 설명**
- `mealType` (enum, required): 식사 종류
  - `breakfast`: 아침
  - `lunch`: 점심
  - `dinner`: 저녁
  - `snack`: 간식
- `foodName` (string, required): 음식 이름
- `calories` (number, optional): 칼로리

---

#### 4.2 DietLogResponse

```json
{
  "id": 1,
  "userId": 1,
  "mealType": "breakfast",
  "foodName": "시금치",
  "calories": 150,
  "recordedAt": "2025-11-05T08:30:00Z",
  "warnings": [
    {
      "id": 1,
      "severity": "높음",
      "message": "와파린과 시금치(비타민K)의 상호작용이 있습니다. 섭취를 제한해주세요.",
      "medication": {
        "id": 2,
        "name": "와파린"
      }
    }
  ]
}
```

---

#### 4.3 DietWarningResponse

```json
{
  "id": 1,
  "userId": 1,
  "dietLog": {
    "id": 1,
    "foodName": "시금치",
    "mealType": "breakfast",
    "recordedAt": "2025-11-05T08:30:00Z"
  },
  "medication": {
    "id": 2,
    "name": "와파린",
    "ingredient": "와파린"
  },
  "warningMessage": "와파린과 시금치(비타민K)의 상호작용이 있습니다. 섭취를 제한해주세요.",
  "severity": "높음",
  "createdAt": "2025-11-05T08:30:00Z"
}
```

---

### 5. Drug Interaction (약-음식 충돌)

#### 5.1 ConflictCheckRequest

```json
{
  "userId": 1,
  "foodName": "자몽"
}
```

**필드 설명**
- `userId` (number, required): 사용자 ID
- `foodName` (string, required): 검사할 음식 이름

---

#### 5.2 ConflictCheckResponse

```json
{
  "conflicts": [
    {
      "drugName": "심바스타틴",
      "drugIngredient": "Simvastatin",
      "foodName": "자몽",
      "foodCategory": "과일",
      "conflictIngredient": "푸라노쿠마린",
      "reason": "자몽의 푸라노쿠마린이 간 효소를 억제하여 약물 농도가 과도하게 높아질 수 있습니다.",
      "severity": "높음",
      "alternatives": "오렌지, 사과, 배 등",
      "source": "식약처 의약품안전나라"
    }
  ],
  "hasConflict": true,
  "highestSeverity": "높음"
}
```

**필드 설명**
- `conflicts` (array): 충돌 목록
- `hasConflict` (boolean): 충돌 여부
- `highestSeverity` (string): 최고 심각도
  - `높음`: 즉시 경고
  - `중간`: 주의 알림
  - `낮음`: 정보 제공

---

#### 5.3 DrugFoodInteractionResponse

```json
{
  "id": 1,
  "drugName": "와파린",
  "drugIngredient": "Warfarin",
  "foodName": "시금치",
  "foodCategory": "채소",
  "conflictIngredient": "비타민K",
  "reason": "시금치의 비타민K가 와파린의 항응고 효과를 감소시킬 수 있습니다.",
  "severity": "높음",
  "alternatives": "오이, 양상추 등 비타민K 함량이 낮은 채소",
  "source": "식약처",
  "createdAt": "2025-11-01T00:00:00Z"
}
```

---

### 6. OCR (약봉지 인식)

#### 6.1 OCRRequest

```json
{
  "imageBase64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAA...",
  "ocrEngine": "google-vision"
}
```

**필드 설명**
- `imageBase64` (string, required): Base64 인코딩된 이미지
- `ocrEngine` (enum, optional): OCR 엔진 선택
  - `google-vision`: Google Vision API (기본값)
  - `tesseract`: Tesseract.js (Fallback)

**파일 업로드 방식** (alternative)
```
POST /api/ocr/prescription
Content-Type: multipart/form-data

image: [File]
```

---

#### 6.2 OCRResponse

```json
{
  "success": true,
  "extractedText": "처방전\n아스피린 100mg\n1일 1회 아침 식후 복용\n30정",
  "parsedMedication": {
    "name": "아스피린",
    "dosage": "100mg",
    "timing": "아침 식후",
    "quantity": 30,
    "confidence": 0.92
  },
  "ocrEngine": "google-vision",
  "processingTime": 1.2
}
```

**필드 설명**
- `success` (boolean): OCR 성공 여부
- `extractedText` (string): 추출된 원본 텍스트
- `parsedMedication` (object): 파싱된 약 정보
  - `confidence` (number): 신뢰도 (0.0 ~ 1.0)
- `ocrEngine` (string): 사용된 OCR 엔진
- `processingTime` (number): 처리 시간(초)

---

#### 6.3 PillSearchRequest (알약 역검색)

```json
{
  "shape": "원형",
  "color": "흰색",
  "printFront": "A",
  "printBack": "100"
}
```

**필드 설명**
- `shape` (string, optional): 모양 (원형, 타원형, 장방형, 사각형 등)
- `color` (string, optional): 색상
- `printFront` (string, optional): 앞면 각인
- `printBack` (string, optional): 뒷면 각인

---

#### 6.4 PillSearchResponse

```json
{
  "results": [
    {
      "itemSeq": "200001234",
      "itemName": "아스피린정100밀리그램",
      "entpName": "바이엘코리아(주)",
      "itemImage": "https://nedrug.mfds.go.kr/pbp/...",
      "chart": "원형",
      "printFront": "A",
      "printBack": "100",
      "colorClass1": "흰색",
      "formCodeName": "정제",
      "markCodeFrontAnal": "A",
      "markCodeBackAnal": "100",
      "itemIngr": "아세틸살리실산",
      "efcyQesitm": "혈전 예방, 해열, 진통",
      "useMethodQesitm": "1일 1회 100mg 경구 투여",
      "atpnQesitm": "위장 장애 주의"
    }
  ],
  "totalCount": 1,
  "source": "식약처 의약품안전나라"
}
```

---

### 7. Notification (알림)

#### 7.1 NotificationResponse

```json
{
  "id": 1,
  "userId": 1,
  "type": "medication_reminder",
  "title": "약 복용 시간입니다",
  "message": "아스피린 100mg을 복용하세요",
  "read": false,
  "createdAt": "2025-11-05T09:00:00Z"
}
```

**필드 설명**
- `type` (enum): 알림 종류
  - `medication_reminder`: 복약 알림
  - `diet_warning`: 식단 경고
  - `family_alert`: 가족 알림
  - `system`: 시스템 알림

---

### 8. Report (리포트) - 선택 기능

#### 8.1 AdherenceReportResponse

```json
{
  "userId": 1,
  "userName": "김시니어",
  "startDate": "2025-10-01",
  "endDate": "2025-10-31",
  "overallAdherence": 87.5,
  "medications": [
    {
      "medicationId": 1,
      "medicationName": "아스피린",
      "totalScheduled": 60,
      "completed": 55,
      "missed": 5,
      "adherenceRate": 91.7
    },
    {
      "medicationId": 2,
      "medicationName": "메트포르민",
      "totalScheduled": 60,
      "completed": 50,
      "missed": 10,
      "adherenceRate": 83.3
    }
  ],
  "weeklyTrends": [
    {
      "weekStart": "2025-10-01",
      "weekEnd": "2025-10-07",
      "adherenceRate": 85.7,
      "completed": 12,
      "missed": 2
    }
  ],
  "generatedAt": "2025-11-05T10:00:00Z"
}
```

---

## 🔧 공통 DTO

### ErrorResponse

```json
{
  "status": 400,
  "error": "Bad Request",
  "message": "이메일은 필수입니다",
  "timestamp": "2025-11-05T10:00:00Z",
  "path": "/api/auth/login"
}
```

---

### PageResponse<T>

```json
{
  "content": [...],
  "page": 0,
  "size": 20,
  "totalElements": 100,
  "totalPages": 5,
  "first": true,
  "last": false
}
```

---

### SuccessResponse

```json
{
  "success": true,
  "message": "성공적으로 처리되었습니다",
  "data": {...}
}
```

---

## 📚 참고 사항

### Validation 어노테이션 (Spring)

- `@NotNull`: null 불가
- `@NotBlank`: 빈 문자열 불가
- `@Email`: 이메일 형식 검증
- `@Size(min=, max=)`: 길이 제한
- `@Pattern(regexp=)`: 정규식 검증
- `@Min`, `@Max`: 숫자 범위
- `@Past`, `@Future`: 날짜 검증

### JWT 토큰 구조

```
Authorization: Bearer <accessToken>
```

- **Access Token**: 15분 유효
- **Refresh Token**: 7일 유효, **Redis에 저장** (MySQL에서 이관)
- **블랙리스트**: Redis에서 관리

#### JWT Claims 구조 (변경됨)
```json
{
  "userId": 1,
  "name": "김시니어",
  "email": "senior@example.com",
  "profileImage": "https://k.kakaocdn.net/...",
  "userRole": "ROLE_USER",
  "customerRole": "SENIOR",
  "type": "ACCESS",
  "iat": 1700000000,
  "exp": 1700000900
}
```

> **주의**: 기존 `role` 필드가 `userRole` + `customerRole`로 분리됨

### 에러 코드

| HTTP Status | 설명 |
|-------------|------|
| 200 | 성공 |
| 201 | 생성됨 |
| 400 | 잘못된 요청 |
| 401 | 인증 실패 |
| 403 | 권한 없음 |
| 404 | 찾을 수 없음 |
| 409 | 충돌 (중복 등) |
| 500 | 서버 오류 |

---

## 📝 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-11-05 | 초안 작성 |
| 2.0 | 2025-11-14 | 프론트엔드 실제 구현 기준으로 업데이트 (Zustand 아키텍처 반영) |
| 2.1 | 2025-11-22 | auth-service 변경 반영 (API 경로, JWT Claims, Redis RefreshToken) |
| 2.2 | 2025-11-22 | Family API 경로 일관성 수정 ({memberId} → {id}) |

---

**문서 버전**: 2.2
**최종 수정일**: 2025-12-25
**작성자**: AMApill 개발팀 (구 뭐냑?)
**프로젝트명**: AMApill (구 SilverCare)
**노션 복사 가능**: ✅

---

## 🏗️ 아키텍처 참고사항

### Frontend 상태 관리 (Zustand)
- **authStore**: 사용자 인증 정보 (user, token, role)
- **medicationStore**: 약 목록 (medications 배열)
- **familyStore**: 가족 그룹 & 멤버 (familyGroup, members)
- **notificationStore** (예정): 알림 목록 & 읽음 상태

### API 최적화 전략
1. **통합 조회**: 관련 데이터를 한 번의 API 호출로 제공 (예: Family)
2. **클라이언트 필터링**: 간단한 필터링은 클라이언트에서 처리
3. **WebSocket 우선**: 실시간 데이터는 WebSocket 사용, REST는 히스토리 조회
4. **PATCH 사용**: 부분 수정은 PUT 대신 PATCH 사용

### 실시간 통신
- **Chat**: WebSocket (Socket.IO)
- **Notification**: WebSocket (향후 구현)
- **Family 상태**: Hocuspocus + Y.js (향후 구현)
