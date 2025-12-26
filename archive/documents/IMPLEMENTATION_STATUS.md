# 🚀 AMApill 구현 상태 요약 (현재 코드 기준)

이 문서는 **코드에 존재하는 모듈/구성 요소**를 기준으로 현재 상태를 요약합니다.
진행률 퍼센트는 코드로 자동 산출되지 않으므로 표기하지 않습니다.

---

## 🏗️ Backend (spring-boot)

### 도메인 패키지

- appointment
- chat
- diet
- disease
- family
- interaction
- medication
- notification
- ocr
- report
- voice
- security

### 실시간 통신

- WebSocket/STOMP: `/ws`
- SSE: `/notifications/subscribe`

---

## 🎨 Frontend (Front)

### Feature 모듈

- appointment
- auth
- chat
- dashboard
- diet
- disease
- family
- medication
- notification
- ocr
- places
- report
- search
- settings
- voice

---

## 🧩 인프라 구성

### docker-compose

- MySQL, PostgreSQL(pgvector), Redis, Kafka, Nginx
- 선택 프로필: api-gateway, auth-service, n8n, hocuspocus

### k8s

- applications: auth-service, spring-boot
- apigateway: spring-cloud-api-gateway
- database: mysql/postgres/redis + admin tools
- middleware: kafka
- core: ingress-nginx, cloudflared

---

## ✅ 참고

상세 기능/진행 상황은 실제 코드, Swagger, 그리고 이슈 트래커를 기준으로 판단합니다.

