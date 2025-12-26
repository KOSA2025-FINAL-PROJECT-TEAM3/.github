# 💬 가족 채팅 API 명세 (코드 기준)

> 근거 파일
> - `spring-boot/src/main/java/com/amapill/backend/domain/chat/api/FamilyChatRestController.java`
> - `spring-boot/src/main/java/com/amapill/backend/domain/chat/api/FamilyChatSocketController.java`
> - `spring-boot/src/main/java/com/amapill/backend/global/config/WebSocketConfig.java`
> - `spring-boot/src/main/java/com/amapill/backend/domain/chat/infra/kafka/FamilyChatConsumer.java`

이 문서는 **실제 코드에 존재하는 경로/DTO/실시간 흐름만** 정리합니다.

---

## 1) 공통 경로

- REST Base: `/family-chat` (Gateway 경유 시 `/api/family-chat/**`)
- WebSocket Endpoint: `/ws` (Gateway 경유 시 `/ws`)
- STOMP Prefix
  - Send: `/app`
  - Subscribe: `/topic`

---

## 2) DTO (요약)

### FamilyChatMessageRequest
- `familyGroupId` (Long, required)
- `familyMemberId` (Long, required)
- `content` (String, required, max 1000)
- `type` (FamilyChatMessageType, optional, default: `TEXT`)

### FamilyChatMessageResponse
- `id`, `familyGroupId`, `familyMemberId`
- `memberNickname`, `content`, `type`, `createdAt`
- `unreadCount`, `readMemberIds`

### FamilyChatInitialLoadResponse
- `messages` (List<FamilyChatMessageResponse>)
- `currentUserLastReadMessageId`
- `totalMemberCount`

### FamilyChatMessageType
- `TEXT`, `IMAGE`, `SYSTEM`, `READ`

---

## 3) REST API

### 3.1 메시지 목록 조회
- `GET /family-chat/rooms/{familyGroupId}/messages`
- Query: `page` (default 0), `size` (default 50, min 1, max 100)
- Response: `List<FamilyChatMessageResponse>`

### 3.2 채팅방 초기 로딩
- `GET /family-chat/rooms/{familyGroupId}/init`
- Query: `familyMemberId` (required)
- Response: `FamilyChatInitialLoadResponse`

### 3.3 안 읽은 메시지 개수(뱃지)
- `GET /family-chat/rooms/{familyGroupId}/unread-count`
- Query: `familyMemberId` (required)
- Response: `Integer`

### 3.4 메시지 전송 (REST)
- `POST /family-chat/rooms/{familyGroupId}/messages`
- Body: `FamilyChatMessageRequest`
- 규칙: Path의 `familyGroupId`와 Body의 `familyGroupId`가 다르면 예외
- Response: `FamilyChatMessageResponse` (HTTP 201)

예시:
```json
{
  "familyGroupId": 1,
  "familyMemberId": 10,
  "content": "안부 인사",
  "type": "TEXT"
}
```

### 3.5 메시지 검색
- `GET /family-chat/rooms/{familyGroupId}/messages/search`
- Query: `keyword` (required, NotBlank)
- Response: `List<FamilyChatMessageResponse>`

### 3.6 이미지 메시지 업로드
- `POST /family-chat/rooms/{familyGroupId}/messages/image`
- Form Data:
  - `file` (multipart, required)
  - `familyMemberId` (required)
  - `content` (optional, `/ai `로 시작 시 AI 처리)
- Response: `String` (S3 이미지 URL)
- 동작: 이미지 업로드만 수행하며 **DB에 메시지를 저장하지 않음**

---

## 4) WebSocket/STOMP

### 4.1 연결
- Endpoint: `/ws` (또는 `/ws/`)
- Handshake 헤더: `X-User-Id`를 수신 시 attributes에 저장

### 4.2 메시지 발행
- `SEND /app/family/{familyGroupId}`
- Body: `FamilyChatMessageRequest`
- 서버는 저장 후 Kafka로 발행 → 구독자에게 브로드캐스트

### 4.3 읽음 처리
- `SEND /app/family/{familyGroupId}/read`
- Body: `FamilyChatMessageRequest`
  - `content`에 마지막으로 읽은 메시지 ID를 문자열로 전달

### 4.4 구독
- `SUBSCRIBE /topic/family/{familyGroupId}`
- Payload: `FamilyChatMessage`
  - `id`, `familyGroupId`, `familyMemberId`, `type`, `content`, `createdAt`, `unreadCount`

---

## 5) 알림 연동 (SSE)

- 메시지 저장 시, 발신자를 제외한 멤버에게 SSE 이벤트 전송
- Event 이름: `chat-update`
- Payload: `{"type":"CHAT_MESSAGE","familyGroupId":<id>,"messageId":<id>}`
- SSE Endpoint는 Notifications 도메인(`/notifications/subscribe`)을 사용
