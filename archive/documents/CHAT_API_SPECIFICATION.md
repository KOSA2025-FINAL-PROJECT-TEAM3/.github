# 뭐냑? 채팅 API 명세서

> Chat API Specification for AMApill Platform (Stage 4)
>
> 의사 및 AI 챗봇 상담 기능을 위한 실시간 채팅 API

---

## 📋 목차

1. [개요](#-개요)
2. [핵심 기능](#-핵심-기능)
3. [REST API 엔드포인트](#-rest-api-엔드포인트)
4. [WebSocket 프로토콜](#-websocket-프로토콜)
5. [데이터 모델](#-데이터-모델)
6. [개발 단계](#-개발-단계)
7. [에러 처리](#-에러-처리)

---

## 🎯 개요

### 목적
AMApill 플랫폼의 **의사 상담** 및 **AI 챗봇 상담** 기능을 위한 실시간 1:1 채팅 시스템 구축

### 기술 스택
- **Real-time Communication**: WebSocket (Socket.IO)
- **REST API**: Spring Boot (백엔드), Axios (프론트엔드)
- **인증**: JWT Bearer Token
- **메시지 저장**: MySQL/PostgreSQL
- **실시간 동기화**: Socket.IO

### 상담 유형
1. **의사 상담**: 실제 약사와 1:1 채팅 (약 복용법, 부작용 상담 등)
2. **AI 챗봇 상담**: AI 기반 건강 및 약물 정보 제공

---

## 🔑 핵심 기능

### 1. 채팅방 관리
- 사용자별 채팅방 목록 조회
- 새로운 상담방 생성 (의사/AI 선택)
- 채팅방 나가기/삭제

### 2. 실시간 메시지 교환
- WebSocket을 통한 실시간 메시지 송수신
- 메시지 읽음 처리
- 타이핑 상태 표시 (typing indicator)

### 3. 메시지 히스토리
- 과거 대화 내용 조회 (Cursor-based Pagination)
- 메시지 검색 (선택 사항)

### 4. 알림
- 새 메시지 알림
- 읽지 않은 메시지 카운트

---

## 🌐 REST API 엔드포인트

### 1. 채팅방 관리

#### 1.1. 채팅방 목록 조회
```http
GET /api/chat/rooms
Authorization: Bearer {JWT_TOKEN}
```

**Query Parameters:**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `page` | `number` | No | 페이지 번호 (기본값: 0) |
| `size` | `number` | No | 페이지 크기 (기본값: 20) |
| `counselorType` | `string` | No | `doctor` 또는 `ai` |

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "rooms": [
      {
        "roomId": "room_12345",
        "counselor": {
          "counselorId": "doc_001",
          "name": "김약사",
          "type": "doctor",
          "profileImageUrl": "https://cdn.amapill.com/profiles/doc_001.jpg",
          "hospital": "서울약국",
          "specialty": "일반 약학"
        },
        "lastMessage": {
          "messageId": "msg_98765",
          "content": "네, 식후 30분에 복용하시면 됩니다.",
          "timestamp": "2025-11-12T10:30:00Z",
          "senderId": "doc_001",
          "senderType": "doctor"
        },
        "unreadCount": 3,
        "createdAt": "2025-11-10T09:00:00Z",
        "updatedAt": "2025-11-12T10:30:00Z",
        "status": "active"
      }
    ],
    "pagination": {
      "currentPage": 0,
      "totalPages": 5,
      "totalElements": 100,
      "size": 20
    }
  }
}
```

---

#### 1.2. 새 채팅방 생성
```http
POST /api/chat/rooms
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "counselorId": "doc_001",
  "counselorType": "doctor",
  "initialMessage": "안녕하세요, 약 복용법에 대해 상담하고 싶습니다."
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "roomId": "room_12345",
    "counselor": {
      "counselorId": "doc_001",
      "name": "김약사",
      "type": "doctor",
      "profileImageUrl": "https://cdn.amapill.com/profiles/doc_001.jpg",
      "hospital": "서울약국",
      "specialty": "일반 약학"
    },
    "createdAt": "2025-11-12T11:00:00Z",
    "status": "active"
  }
}
```

---

#### 1.3. 채팅방 나가기/삭제
```http
DELETE /api/chat/rooms/:roomId
Authorization: Bearer {JWT_TOKEN}
```

**Response (204 No Content):**
```json
{
  "success": true,
  "message": "채팅방에서 나갔습니다."
}
```

---

### 2. 메시지 관리

#### 2.1. 메시지 히스토리 조회
```http
GET /api/chat/rooms/:roomId/messages
Authorization: Bearer {JWT_TOKEN}
```

**Query Parameters:**
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `cursor` | `string` | No | 커서 (마지막 메시지 ID) |
| `limit` | `number` | No | 메시지 개수 (기본값: 50) |

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "messageId": "msg_98765",
        "content": "안녕하세요, 약 복용법에 대해 상담하고 싶습니다.",
        "sender": {
          "senderId": "user_001",
          "senderType": "user",
          "senderName": "김시니어",
          "profileImageUrl": "https://cdn.amapill.com/profiles/user_001.jpg"
        },
        "timestamp": "2025-11-12T10:00:00Z",
        "isRead": true,
        "attachments": []
      },
      {
        "messageId": "msg_98766",
        "content": "네, 어떤 약에 대해 궁금하신가요?",
        "sender": {
          "senderId": "doc_001",
          "senderType": "doctor",
          "senderName": "김약사",
          "profileImageUrl": "https://cdn.amapill.com/profiles/doc_001.jpg"
        },
        "timestamp": "2025-11-12T10:05:00Z",
        "isRead": true,
        "attachments": []
      }
    ],
    "nextCursor": "msg_98760",
    "hasMore": true
  }
}
```

---

#### 2.2. 메시지 전송 (REST Fallback)
```http
POST /api/chat/rooms/:roomId/messages
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "타이레놀 복용법에 대해 알고 싶습니다.",
  "attachments": []
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "messageId": "msg_98767",
    "content": "타이레놀 복용법에 대해 알고 싶습니다.",
    "sender": {
      "senderId": "user_001",
      "senderType": "user",
      "senderName": "김시니어"
    },
    "timestamp": "2025-11-12T10:10:00Z",
    "isRead": false
  }
}
```

---

#### 2.3. 메시지 읽음 처리
```http
PATCH /api/chat/rooms/:roomId/messages/:messageId/read
Authorization: Bearer {JWT_TOKEN}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "messageId": "msg_98767",
    "isRead": true,
    "readAt": "2025-11-12T10:11:00Z"
  }
}
```

---

## 🔌 WebSocket 프로토콜

### 연결 설정
```javascript
// Frontend: Socket.IO 연결
import { io } from 'socket.io-client';

const socket = io('wss://api.amapill.com', {
  auth: {
    token: 'JWT_TOKEN_HERE'
  },
  transports: ['websocket']
});
```

---

### WebSocket 이벤트

#### 1. 채팅방 입장
**Client → Server:**
```javascript
socket.emit('joinRoom', {
  roomId: 'room_12345'
});
```

**Server → Client:**
```javascript
socket.on('roomJoined', (data) => {
  console.log('방에 입장했습니다:', data);
  // data: { roomId: 'room_12345', members: [...] }
});
```

---

#### 2. 메시지 전송
**Client → Server:**
```javascript
socket.emit('sendMessage', {
  roomId: 'room_12345',
  content: '안녕하세요',
  attachments: []
});
```

**Server → Client:**
```javascript
socket.on('messageReceived', (data) => {
  console.log('새 메시지:', data);
  // data: { messageId, content, sender, timestamp, ... }
});
```

---

#### 3. 타이핑 상태 표시
**Client → Server:**
```javascript
socket.emit('typingIndicator', {
  roomId: 'room_12345',
  isTyping: true
});
```

**Server → Client:**
```javascript
socket.on('userTyping', (data) => {
  console.log('상대방이 입력 중:', data);
  // data: { userId, userName, isTyping }
});
```

---

#### 4. 메시지 읽음 처리
**Client → Server:**
```javascript
socket.emit('markAsRead', {
  roomId: 'room_12345',
  messageId: 'msg_98767'
});
```

**Server → Client:**
```javascript
socket.on('messageRead', (data) => {
  console.log('메시지가 읽혔습니다:', data);
  // data: { messageId, readBy, readAt }
});
```

---

#### 5. 채팅방 나가기
**Client → Server:**
```javascript
socket.emit('leaveRoom', {
  roomId: 'room_12345'
});
```

**Server → Client:**
```javascript
socket.on('roomLeft', (data) => {
  console.log('방을 나갔습니다:', data);
  // data: { roomId }
});
```

---

## 📦 데이터 모델

### ChatRoom
```typescript
interface ChatRoom {
  roomId: string;                // 채팅방 ID (UUID)
  counselor: Counselor;           // 상담자 정보 (의사 또는 AI)
  lastMessage: ChatMessage | null; // 마지막 메시지
  unreadCount: number;            // 읽지 않은 메시지 수
  createdAt: string;              // 생성 시각 (ISO 8601)
  updatedAt: string;              // 마지막 업데이트 시각
  status: 'active' | 'archived';  // 상태
}
```

---

### Counselor
```typescript
interface Counselor {
  counselorId: string;            // 상담자 ID
  name: string;                   // 이름
  type: 'doctor' | 'ai';          // 상담자 유형
  profileImageUrl?: string;       // 프로필 이미지 URL

  // 의사인 경우
  hospital?: string;              // 병원/약국 이름
  specialty?: string;             // 전문 분야

  // AI인 경우
  aiModel?: string;               // AI 모델명 (예: "GPT-4", "Claude")
  capabilities?: string[];        // AI 기능 목록
}
```

---

### ChatMessage
```typescript
interface ChatMessage {
  messageId: string;              // 메시지 ID (UUID)
  content: string;                // 메시지 내용
  sender: MessageSender;          // 발신자 정보
  timestamp: string;              // 전송 시각 (ISO 8601)
  isRead: boolean;                // 읽음 여부
  readAt?: string;                // 읽은 시각
  attachments: Attachment[];      // 첨부 파일 목록
}
```

---

### MessageSender
```typescript
interface MessageSender {
  senderId: string;               // 발신자 ID
  senderType: 'user' | 'doctor' | 'ai'; // 발신자 유형
  senderName: string;             // 발신자 이름
  profileImageUrl?: string;       // 프로필 이미지 URL
}
```

---

### Attachment
```typescript
interface Attachment {
  attachmentId: string;           // 첨부 파일 ID
  type: 'image' | 'file' | 'prescription'; // 파일 유형
  fileName: string;               // 파일명
  fileUrl: string;                // 파일 URL
  fileSize: number;               // 파일 크기 (bytes)
  mimeType: string;               // MIME 타입
}
```

---

## 🚀 개발 단계

### Phase 1: REST API 기본 구현
- [x] 채팅방 CRUD API
- [x] 메시지 CRUD API
- [x] 메시지 히스토리 조회 (Cursor-based Pagination)
- [x] 메시지 읽음 처리

### Phase 2: WebSocket 실시간 통신
- [ ] Socket.IO 연동
- [ ] 실시간 메시지 송수신
- [ ] 타이핑 상태 표시
- [ ] 읽음 처리 실시간 반영

### Phase 3: AI 챗봇 통합
- [ ] AI 챗봇 엔드포인트 연동
- [ ] 건강 정보 및 약물 정보 제공
- [ ] AI 응답 스트리밍 (Optional)

### Phase 4: 고급 기능
- [ ] 메시지 검색
- [ ] 첨부 파일 업로드/다운로드
- [ ] 상담 내역 PDF 다운로드
- [ ] 알림 푸시 연동

---

## ⚠️ 에러 처리

### HTTP 에러 코드

| 코드 | 의미 | 설명 |
|------|------|------|
| `400` | Bad Request | 잘못된 요청 (필수 파라미터 누락 등) |
| `401` | Unauthorized | 인증 실패 (JWT 토큰 없음/만료) |
| `403` | Forbidden | 권한 없음 (다른 사용자의 채팅방 접근) |
| `404` | Not Found | 리소스 없음 (채팅방/메시지 없음) |
| `409` | Conflict | 중복 (이미 존재하는 채팅방) |
| `500` | Internal Server Error | 서버 오류 |

---

### 에러 응답 형식
```json
{
  "success": false,
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "채팅방을 찾을 수 없습니다.",
    "details": {
      "roomId": "room_99999"
    }
  }
}
```

---

### WebSocket 에러 이벤트
```javascript
socket.on('error', (error) => {
  console.error('WebSocket 에러:', error);
  // error: { code, message, details }
});
```

**에러 코드 목록:**
- `INVALID_TOKEN`: 유효하지 않은 JWT 토큰
- `ROOM_NOT_FOUND`: 채팅방을 찾을 수 없음
- `UNAUTHORIZED_ACCESS`: 권한 없는 접근
- `MESSAGE_SEND_FAILED`: 메시지 전송 실패
- `CONNECTION_LOST`: 연결 끊김

---

## 📖 참고 자료

- [Socket.IO Documentation](https://socket.io/docs/)
- [WebSocket API Specification](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [JWT Authentication](https://jwt.io/)
- [Cursor-based Pagination](https://slack.engineering/evolving-api-pagination-at-slack/)

---

## 📝 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-11-12 | 초안 작성 (REST API + WebSocket 명세) |

---

**작성일**: 2025-12-25 (Updated)
**버전**: 1.0
**작성자**: 뭐냑? 개발팀
**상태**: 초안 완성
