---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  /* --- Global Settings --- */
  section {
    background-color: #F5F5F5;
    font-family: 'Roboto', 'Noto Sans KR', sans-serif;
    color: #212121;
    padding: 40px;
  }
  
  /* --- Typography & Colors --- */
  h1 {
    color: #1976D2; /* Primary Blue */
    font-size: 48px;
    border-bottom: none;
  }
  h2 {
    color: #1565C0;
    font-size: 36px;
    border-bottom: 2px solid #E0E0E0;
    padding-bottom: 10px;
  }
  h3 {
    color: #00796B; /* Success Green */
    font-size: 28px;
  }
  strong {
    color: #1976D2;
    font-weight: bold;
  }
  em {
    color: #E53935; /* Danger Red for alerts/critical */
    font-style: normal;
    font-weight: bold;
  }
  
  /* --- Layout Utilities --- */
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
  .box {
    background: #FFFFFF;
    border-radius: 16px; /* Rounded Corners */
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  
  /* --- Code Block --- */
  code {
    background: #E3F2FD;
    color: #0D47A1;
  }
---

<style scoped>
section {
  background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
h1 { color: #FFFFFF; font-size: 64px; margin-bottom: 20px;}
h3 { color: #81D4FA; font-size: 32px; }
p { font-size: 24px; opacity: 0.9; }
</style>

# AMApill (뭐냑?)
### 가족 돌봄 네트워크 기반 약 관리 플랫폼

**3차 프로젝트 아키텍처 및 UI 설계안**

---

## 📱 Project Overview

**AMApill**은 고령층의 복약 관리를 돕고, 가족 구성원이 이를 실시간으로 모니터링할 수 있는 **돌봄 네트워크 플랫폼**입니다.

<div class="columns">
<div class="box">

### 🎯 Core Mission
* **복약 순응도 향상**: 알림 및 리포트
* **가족 연결**: 보호자 모드 & 실시간 채팅
* **건강한 노후**: 식단 및 질병 관리
</div>

<div class="box">

### 💡 Key Features
* **Dual Mode UI**: 노인 모드 / 보호자 모드
* **AI Support**: OCR 약 봉투 스캔, 음성 인식
* **Real-time**: 복약 상태 실시간 동기화
</div>
</div>

---

## 🎨 UI/UX Design Strategy

요청하신 **Material Design** 가이드를 준수하여 직관적이고 편안한 사용자 경험을 제공합니다.

* **Color Palette**:
    * 🔵 **Primary**: `#1976D2` (신뢰, 안정)
    * 🟢 **Success**: `#00796B` (복약 완료, 정상)
    * 🔴 **Alert**: `#E53935` (미복약, 위험 경고)
* **Components**:
    * **Card UI**: Radius 16px의 부드러운 카드 형태
    * **Typography**: 노인 모드를 위한 큰 폰트 및 고대비 지원
    * **Dashboard**: 오늘의 복약, 최근 기록, 식단 로그를 한눈에 파악

---

## 🏗️ System Architecture (High-Level)

**Microservices Architecture**를 지향하며, 보안과 확장성을 고려한 3-Tier 구조입니다.

<div class="columns">
<div>

### 🛡️ Gateway Service
* **Single Entry Point**: `/api/**`, `/ws/**`
* **Security**: JWT 검증 및 `X-User-*` 헤더 주입
* **Resilience**: Circuit Breaker, Rate Limiting

</div>
<div>

### 🔐 Auth Service
* **OAuth 2.0**: 카카오 로그인 연동
* **Token**: Access(JWT) / Refresh(Redis) 관리
* **User Profile**: 계정 및 프로필 이미지 관리

</div>
</div>

---

## ⚙️ Backend Core Features

**Core Service** (`Spring Boot 3.5.8`)는 비즈니스 로직의 핵심을 담당합니다.

<div class="box">

* **👨‍👩‍👧‍👦 Family Network**: 가족 그룹 초대, 관리, 채팅 (WebSocket/STOMP)
* **💊 Medication**: 처방전 OCR, 복약 스케줄링, 순응도 분석
* **🍎 Diet & Health**: 식단 로그, 혈압 등 건강 데이터 추적
* **📢 Notification**: SSE(Server-Sent Events) 기반 실시간 알림 구독
* **🤖 AI & Voice**: Spring AI 기반 의도 분석 및 답변 생성
</div>

---

## 💾 Infrastructure & Data Flow

안정적인 서비스를 위해 컨테이너 기반의 인프라를 구성했습니다. (`docker-compose`)

* **MySQL 8.0**: 사용자, 처방전, 복약 기록 등 정형 데이터 (트랜잭션 관리)
* **Redis 7**: JWT Refresh Token, API 캐싱, 실시간 세션 정보
* **Kafka (KRaft)**: 서비스 간 이벤트 스트리밍 (채팅, 로그, 비동기 작업)
* **PostgreSQL (+pgvector)**: AI 기능을 위한 벡터 스토어 (보안/검색)

---

## 🔒 Security Architecture

**"Gateway가 검증하고, 내부 서비스는 신뢰한다"** 원칙을 따릅니다.

1.  **Client Request**: JWT 포함 요청 (`Authorization: Bearer ...`)
2.  **API Gateway**:
    * Token 유효성 검증
    * 사용자 정보 파싱 → **HTTP Header 주입** (`X-User-Id`, `X-User-Role`)
3.  **Core Service**:
    * Header 기반으로 `Authentication` 객체 생성 (Stateless)
    * 별도의 토큰 파싱 로직 없이 비즈니스 로직 수행

---

## 🚀 Development Stack

최신 기술 스택을 적용하여 유지보수성과 퍼포먼스를 확보했습니다.

| Category | Stack | Version |
| :--- | :--- | :--- |
| **Language** | Java | **21** (LTS) |
| **Framework** | Spring Boot | **3.5.8** |
| **Gateway** | Spring Cloud | 2025.0.0 |
| **Message Queue** | **Kafka** | KRaft Mode |
| **AI Integration** | Spring AI | OpenAI Model |

---

<style scoped>
section {
  background-color: #ffffff;
  color: #1976D2;
}
h1 { color: #1976D2; border: none; }
</style>

# Thank You
### 목표 -> 건강한 노후 🏃‍♂️

**Q & A**