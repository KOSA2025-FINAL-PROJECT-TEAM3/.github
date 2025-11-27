# 📘 API 상세 명세서 (API Reference)

> **버전**: 1.0
> **생성일**: 2025-11-27
> **비고**: 이 문서는 소스 코드를 기반으로 자동 생성/정리된 문서입니다.

---

## 1️⃣ 인증 및 사용자 (Auth Service)
**Base URL**: `http://localhost:8081` (Gateway 경유 시 `/api/auth`, `/api/users` 등으로 라우팅 될 수 있음 - Gateway 설정 확인 필요)

### Auth (`/auth`)
| Method | URI | 설명 | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | 일반 로그인 | `LoginRequest` | `LoginResponse` |
| `POST` | `/auth/signup` | 회원가입 | `SignupUserRequest` | `LoginResponse` |
| `POST` | `/auth/kakao-login` | 카카오 OAuth 로그인 | `KakaoLoginRequest` | `LoginResponse` |
| `POST` | `/auth/select-role` | 역할 선택 (SENIOR/CAREGIVER) | `RoleSelectionRequest` | `TokenResponse` |
| `POST` | `/auth/refresh` | 토큰 갱신 | `RefreshTokenRequest` | `TokenResponse` |
| `POST` | `/auth/logout` | 로그아웃 | - | `Void` |

### User (`/users`)
| Method | URI | 설명 | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/users/me` | 내 프로필 조회 | - | `UserResponse` |
| `PUT` | `/users/me` | 내 프로필 수정 | `UpdateUserRequest` | `UserResponse` |
| `DELETE` | `/users/me` | 계정 비활성화/삭제 | - | `Void` |

---

## 2️⃣ 가족 관리 (Family)
**Base URL**: `/family` (Core Service)

### Family Group (`/family`)
| Method | URI | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| `POST` | `/family/groups` | 가족 그룹 생성 | `FamilyGroupRequest` |
| `GET` | `/family/groups` | 내 가족 그룹 목록 조회 | |
| `GET` | `/family/groups/{id}` | 특정 가족 그룹 상세 조회 | |
| `DELETE` | `/family/groups/{id}` | 가족 그룹 삭제 | 생성자만 가능 |
| `POST` | `/family/groups/{id}/members` | 가족 구성원 초대 (이메일 기반) | `FamilyMemberInviteRequest` |
| `GET` | `/family/groups/{id}/members` | 가족 구성원 목록 조회 | |
| `DELETE` | `/family/members/{id}` | 가족 구성원 제거 | |
| `GET` | `/family/members/{userId}/medications` | 가족 구성원 약 조회 (모니터링) | 대상 User ID 필요 |

### Family Invite (Auth Required) (`/family/invites`)
*Double Code System (Long Token + Short Code)*

| Method | URI | 설명 | Request | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/family/invites` | 초대 생성 (링크+코드) | `CreateInviteRequest` | `InviteResponse` |
| `GET` | `/family/invites` | 내가 생성한 초대 목록 | `groupId` (opt) | `List<InvitationDetailResponse>` |
| `DELETE` | `/family/invites/{inviteId}` | 초대 취소 | - | `Void` |

### Public Invite (No Auth / Partial Auth) (`/family/public/invites`)
| Method | URI | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| `GET` | `/family/public/invites/start` | 초대 수락 프로세스 시작 | `token` 파라미터 필요. 쿠키(Short Code) 설정 |
| `POST` | `/family/public/invites/accept` | 초대 수락 (최종) | `AcceptInviteRequest` (Short Code 포함) |

---

## 3️⃣ 약 관리 (Medication)
**Base URL**: `/medications`

### Medication Core (`/medications`)
| Method | URI | 설명 | Request |
| :--- | :--- | :--- | :--- |
| `POST` | `/medications/` | 약 등록 | `MedicationRequest` |
| `POST` | `/medications/register-from-ocr` | OCR 기반 일괄 등록 | `RegisterFromOCRRequest` |
| `GET` | `/medications/` | 내 약 목록 조회 | |
| `PATCH` | `/medications/{id}` | 약 정보 수정 | `MedicationRequest` |
| `DELETE` | `/medications/{id}` | 약 삭제 | |

### Medication Logs (`/medications` & `/api/medications/logs`)
*Controller 경로가 두 곳으로 나뉘어 확인됨, 통일 필요 가능성 있음*

| Method | URI | 설명 |
| :--- | :--- | :--- |
| `POST` | `/medications/logs` | 복용 체크 (기록 등록) |
| `GET` | `/medications/logs` | 복용 기록 조회 |
| `POST` | `/api/medications/logs` | (Alias) 복용 기록 등록 |
| `GET` | `/api/medications/logs` | (Alias) 복용 기록 조회 |

---

## 4️⃣ 질병 & 식단 (Disease & Diet)

### Disease (`/disease`)
| Method | URI | 설명 |
| :--- | :--- | :--- |
| `POST` | `/disease` | 질병 등록 |
| `GET` | `/disease/user/{userId}` | 사용자별 질병 목록 조회 |
| `GET` | `/disease/{id}` | 질병 상세 조회 |
| `PUT` | `/disease/{id}` | 질병 수정 |
| `DELETE` | `/disease/{id}` | 질병 삭제 (Soft Delete) |
| `POST` | `/disease/{diseaseId}/medications/{medicationId}` | 질병-약 연결 |
| `DELETE` | `/disease/{diseaseId}/medications/{medicationId}` | 질병-약 연결 해제 |
| `GET` | `/disease/user/{userId}/export/pdf` | PDF 내보내기 |
| `GET` | `/disease/user/{userId}/trash` | 휴지통 조회 |
| `DELETE` | `/disease/user/{userId}/trash` | 휴지통 비우기 |

### Diet (`/diet`)
| Method | URI | 설명 |
| :--- | :--- | :--- |
| `POST` | `/diet/logs` | 식단 기록 등록 |
| `GET` | `/diet/logs` | 내 식단 내역 조회 |
| `PATCH` | `/diet/logs/{logId}` | 식단 수정 |
| `DELETE` | `/diet/logs/{logId}` | 식단 삭제 |
| `GET` | `/diet/warnings` | 약-음식 충돌 경고 조회 |

---

## 5️⃣ 기타 기능 (Reports, OCR, Notification, Chat)

### Reports (`/reports`)
| Method | URI | 설명 | 파라미터 |
| :--- | :--- | :--- | :--- |
| `GET` | `/reports/adherence` | 복약 순응도 리포트 | `startDate`, `endDate` |

### OCR (`/ocr`)
| Method | URI | 설명 | Request |
| :--- | :--- | :--- | :--- |
| `POST` | `/ocr/scan` | 처방전 스캔 및 분석 | `MultipartFile file` |
| `POST` | `/ocr/extract` | 약물 이미지 OCR | `MultipartFile file` |

### Notification (`/notifications`)
| Method | URI | 설명 |
| :--- | :--- | :--- |
| `GET` | `/notifications` | 알림 히스토리 조회 |
| `PATCH` | `/notifications/{id}/read` | 읽음 처리 |
| `DELETE` | `/notifications/{id}` | 알림 삭제 |

### Family Chat (`/family-chat`)
| Method | URI | 설명 |
| :--- | :--- | :--- |
| `POST` | `/family-chat/rooms` | 채팅방 생성/수정 |
| `GET` | `/family-chat/rooms/by-family/{familyGroupId}` | 가족 그룹별 채팅방 조회 |
| `GET` | `/family-chat/rooms/{roomId}/messages` | 메시지 목록 조회 (Paging) |
| `POST` | `/family-chat/rooms/{roomId}/messages` | 메시지 전송 (HTTP) |
| `GET` | `/family-chat/rooms/{roomId}/messages/search` | 메시지 검색 |
| `POST` | `/family-chat/rooms/{roomId}/members` | 멤버 초대 |
| `GET` | `/family-chat/rooms/{roomId}/members` | 멤버 목록 |
| `DELETE` | `/family-chat/rooms/{roomId}/members/{id}` | 멤버 내보내기 |

### WebSocket Chat
*   **Endpoint**: `/ws-stomp` (추정, Config 확인 필요)
*   **Subscribe**: `/topic/family/{roomId}`
*   **Publish**: `/app/family/{roomId}` (Controller: `FamilyChatSocketController`)
