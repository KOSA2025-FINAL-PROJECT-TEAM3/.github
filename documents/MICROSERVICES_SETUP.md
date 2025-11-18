# 🏗️ 뭐냑? 9-Stack 마이크로서비스 아키텍처

> MySQL + PostgreSQL 분리 구조 및 Spring Cloud 기반 마이크로서비스 설정 가이드

---

## 📋 목차

- [아키텍처 개요](#-아키텍처-개요)
- [9-Stack 구성](#-9-stack-구성)
- [데이터베이스 분리 전략](#-데이터베이스-분리-전략)
- [설치 및 실행](#-설치-및-실행)
- [서비스별 상세 설명](#-서비스별-상세-설명)
- [개발 가이드](#-개발-가이드)
- [트러블슈팅](#-트러블슈팅)

---

## 🎯 아키텍처 개요

뭐냑?는 **9개의 독립적인 서비스**로 구성된 마이크로서비스 아키텍처를 채택합니다.

### 핵심 원칙

1. **단일 책임 원칙**: 각 서비스는 하나의 비즈니스 도메인만 담당
2. **데이터베이스 분리**: MySQL(트랜잭션) + PostgreSQL(실시간 동기화)
3. **이벤트 기반 통신**: Kafka를 통한 비동기 메시징
4. **독립 배포**: 각 서비스는 독립적으로 배포 가능
5. **수평 확장**: 부하에 따라 개별 서비스 스케일 아웃

---

## 📦 9-Stack 구성

### 인프라 레이어 (3개)

| 서비스 | 포트 | 역할 | 기술 스택 |
|--------|------|------|-----------|
| **API Gateway** | 8080 | 단일 진입점, 라우팅, 인증 | Spring Cloud Gateway |
| **Eureka Server** | 8761 | 서비스 디스커버리 | Spring Cloud Netflix Eureka |
| **Config Server** | 8888 | 중앙 설정 관리 | Spring Cloud Config |

### 비즈니스 서비스 레이어 (6개)

| 서비스 | 포트 | 주요 기능 | 데이터베이스 |
|--------|------|-----------|--------------|
| **Auth Service** | 8081 | 회원가입, 로그인, JWT 발급 | MySQL + Redis |
| **Medication Service** | 8082 | 약 관리, 복용 일정 | MySQL |
| **Family Service** | 8083 | 가족 네트워크, 권한 관리 | MySQL |
| **Diet Service** | 8084 | 식단 관리, 약-음식 충돌 | MySQL |
| **Notification Service** | 8085 | 알림 발송 (웹/모바일) | MySQL |
| **OCR Service** | 8086 | 약봉지 이미지 인식 | - |

### 실시간 동기화 레이어 (1개)

| 서비스 | 포트 | 역할 | 데이터베이스 |
|--------|------|------|--------------|
| **Hocuspocus Server** | 1234 | WebSocket 기반 실시간 동기화 | PostgreSQL |

---

## 🗄️ 데이터베이스 분리 전략

### MySQL vs PostgreSQL 역할 분담

```
┌─────────────────────────────────────────────────────────────┐
│                      뭐냑? 데이터 레이어                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐        ┌─────────────────────┐     │
│  │   MySQL 8.0         │        │  PostgreSQL 16      │     │
│  │   (amapill)      │        │  (amapill_sync)  │     │
│  ├─────────────────────┤        ├─────────────────────┤     │
│  │ • users             │        │ • documents         │     │
│  │ • medications       │        │ • sessions          │     │
│  │ • family_groups     │        │ • cursor_positions  │     │
│  │ • diet_logs         │        │ • document_history  │     │
│  │ • notifications     │        │ • metrics           │     │
│  │ • drug_food_inter.. │        │                     │     │
│  └─────────────────────┘        └─────────────────────┘     │
│         ▲                                ▲                   │
│         │                                │                   │
│         │                                │                   │
│  ┌──────┴────────┐              ┌────────┴─────────┐       │
│  │ Spring Boot   │              │ Hocuspocus       │       │
│  │ Microservices │◄────Kafka────┤ (Node.js)        │       │
│  │ (Auth, Med,   │              │                  │       │
│  │  Family, etc) │              │ Y.js CRDT        │       │
│  └───────────────┘              └──────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 데이터베이스 선택 기준

#### MySQL 사용 (트랜잭션 보장 필요)
- ✅ 사용자 인증/인가 데이터
- ✅ 약 정보 및 복용 기록
- ✅ 가족 네트워크 관계
- ✅ 식단 기록 및 경고
- ✅ 알림 이력
- ✅ 약-음식 상호작용 룰

#### PostgreSQL 사용 (실시간 동기화)
- ✅ Y.js CRDT 문서 저장
- ✅ WebSocket 세션 관리
- ✅ 협업 커서 위치 추적
- ✅ 실시간 변경 이력
- ✅ 연결 메트릭스

---

## 🚀 설치 및 실행

### 빠른 시작

```bash
# Docker Compose로 전체 스택 실행
docker-compose up -d

# Frontend 개발 서버
npm install && npm run dev
```

**상세 가이드**: [QUICKSTART.md](./QUICKSTART.md) 참조

### 주요 서비스 URL

| 서비스 | URL | 설명 |
|--------|-----|------|
| Frontend | http://localhost:5173 | React 개발 서버 |
| API Gateway | http://localhost:8080 | API 진입점 |
| Eureka Dashboard | http://localhost:8761 | 서비스 목록 확인 |

---

## 🔍 서비스별 상세 설명

### Spring Cloud 인프라

**API Gateway, Eureka Server, Config Server 상세 설명**:
[ARCHITECTURE.md](./ARCHITECTURE.md#-spring-cloud-컴포넌트-상세-설명) 참조

---

### 비즈니스 서비스

### 1. Auth Service (8081)

**역할**: 인증 및 권한 관리

**Repository**: [auth-service](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/auth-service)

```yaml
# 주요 API
POST /api/auth/kakao/login   # 카카오 OAuth 로그인 (JWT 발급)
POST /api/auth/refresh       # Access Token 갱신
POST /api/auth/logout        # 로그아웃 (Refresh Token 삭제)
GET  /api/users/me           # 내 프로필 조회
PUT  /api/users/me           # 내 프로필 수정
DELETE /api/users/me         # 계정 비활성화

# OAuth 2.0 Flow
1. Frontend → Kakao 인가 서버: 인가 코드 요청
2. Kakao → Frontend: 인가 코드 (code) 반환
3. Frontend → Auth Service: code + redirectUri 전송
4. Auth Service → Kakao: code로 액세스 토큰 요청
5. Kakao → Auth Service: 사용자 정보 반환
6. Auth Service: JWT 생성 및 사용자 DB 저장/업데이트
7. Auth Service → Frontend: JWT 토큰 반환

# 기술 스택
- Spring Boot 3.4.7, Java 21 LTS
- Spring Security 6.x
- Kakao OAuth 2.0 (소셜 로그인)
- JWT (JJWT 0.12.3, Access Token 15분, Refresh Token 7일)
- MySQL 8.0 (사용자 정보, Refresh Token 저장)
- Spring Data JPA (Hibernate)

# CI/CD
- GitHub Actions (Maven 빌드, 테스트, Docker 이미지 빌드)
- GitHub Container Registry (GHCR)
- GitOps: k8s-manifests 자동 업데이트 → ArgoCD 배포

# 보안
- JWT 기반 Stateless 인증
- Refresh Token DB 저장 (무효화 가능)
- Spring Security Filter Chain
- CORS 설정
```

### 5. Medication Service (8082)

**역할**: 약 관리 및 복용 일정

```yaml
# 주요 API
GET    /api/medications              # 약 목록
POST   /api/medications              # 약 등록
PUT    /api/medications/{id}         # 약 수정
DELETE /api/medications/{id}         # 약 삭제
POST   /api/medications/{id}/check   # 복용 체크
GET    /api/medications/schedule     # 오늘 일정

# 이벤트 발행 (Kafka)
- medication.created
- medication.taken
- medication.missed
```

### 6. Family Service (8083)

**역할**: 가족 네트워크 관리

```yaml
# 주요 API
POST /api/family/groups              # 그룹 생성
POST /api/family/groups/{id}/invite  # 가족 초대
GET  /api/family/members             # 가족 구성원 조회
GET  /api/family/{userId}/medications # 가족 약 조회

# 권한 관리
- parent: 약 복용만 가능
- child: 약 등록/수정/삭제 가능
```

### 7. Diet Service (8084)

**역할**: 식단 관리 및 약-음식 충돌 검사

```yaml
# 주요 API
POST /api/diet/logs                  # 식단 기록
GET  /api/diet/warnings              # 충돌 경고 조회
POST /api/diet/check                 # 실시간 충돌 검사

# 룰 베이스 시스템
1. 사용자가 음식 입력
2. 현재 복용 중인 약 조회
3. drug_food_interactions 테이블 검색
4. 충돌 발견 시 경고 생성
5. 대체 음식 추천
```

### 8. Notification Service (8085)

**역할**: 알림 발송 및 관리

```yaml
# 주요 API
GET  /api/notifications              # 알림 목록
PUT  /api/notifications/{id}/read    # 읽음 처리
POST /api/notifications/send         # 수동 알림 발송

# 알림 트리거 (Kafka Consumer)
- medication.missed → "자녀에게 미복용 알림"
- medication.low_stock → "재고 부족 알림"
- diet.warning → "약-음식 충돌 경고"

# 발송 채널
- Phase 1: 웹 알림 (DB 저장)
- Phase 2: 카카오톡 알림톡 (계획)
```

### 9. OCR Service (8086)

**역할**: 약봉지 이미지 인식

```yaml
# 주요 API
POST /api/ocr/extract    # 이미지 업로드 → 텍스트 추출
POST /api/ocr/parse      # 텍스트 → 약 정보 파싱

# OCR 엔진
- 1순위: Google Cloud Vision API
- 2순위: Tesseract.js (Fallback)

# 파싱 로직
1. 이미지 수신
2. 텍스트 추출
3. 정규표현식으로 약 이름, 용량, 복용법 파싱
4. 식약처 API로 약 정보 검증
5. Medication Service로 자동 등록
```

### Hocuspocus Server (1234)

**역할**: 실시간 협업 동기화 (게시글 공동편집 - 선택 기능)

**상세 아키텍처**:
[ARCHITECTURE.md](./ARCHITECTURE.md#5️⃣-실시간-동기화-아키텍처) 참조

---

## 🛠️ 개발 가이드

### 새로운 마이크로서비스 추가하기

```bash
# 1. Spring Initializr로 프로젝트 생성
# 2. pom.xml 의존성 추가
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
  </dependency>
</dependencies>

# 3. application.yml 설정
spring:
  application:
    name: new-service
  cloud:
    config:
      uri: http://localhost:8888
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/

# 4. @EnableDiscoveryClient 추가
@SpringBootApplication
@EnableDiscoveryClient
public class NewServiceApplication { }

# 5. docker-compose.yml에 서비스 추가
```

### 서비스 간 통신 패턴

#### 1. 동기 통신 (OpenFeign)

```java
@FeignClient(name = "medication-service")
public interface MedicationClient {
  @GetMapping("/api/medications/{id}")
  MedicationDTO getMedication(@PathVariable Long id);
}
```

#### 2. 비동기 통신 (Kafka)

```java
// Producer
@Autowired
private KafkaTemplate<String, MedicationEvent> kafkaTemplate;

kafkaTemplate.send("medication.created", new MedicationEvent(...));

// Consumer
@KafkaListener(topics = "medication.created", groupId = "notification-group")
public void handleMedicationCreated(MedicationEvent event) {
  // 알림 발송 로직
}
```

### 데이터베이스 마이그레이션

```bash
# MySQL (Flyway)
src/main/resources/db/migration/
  V1__init_schema.sql
  V2__add_expiry_date.sql

# PostgreSQL (Liquibase)
src/main/resources/db/changelog/
  changelog-master.xml
  V1__init_documents.sql
```

---

## 🔧 트러블슈팅

### 1. Eureka에 서비스가 등록되지 않음

```bash
# 원인: 네트워크 문제 또는 Eureka 서버 미실행
# 해결:
docker-compose logs eureka-server
curl http://localhost:8761/eureka/apps
```

### 2. API Gateway 라우팅 실패

```bash
# 원인: 서비스 이름 불일치
# 해결: application.yml의 spring.application.name 확인
spring:
  application:
    name: medication-service  # Eureka에 등록된 이름과 동일해야 함
```

### 3. MySQL 연결 실패

```bash
# 원인: 컨테이너 간 네트워크 문제
# 해결:
docker network ls
docker network inspect amapill-network

# JDBC URL 확인
jdbc:mysql://mysql:3306/amapill  # 컨테이너 이름 사용
```

### 4. PostgreSQL 초기화 실패

```bash
# 원인: 스키마 파일 권한 문제
# 해결:
chmod 644 database-schema-postgresql.sql
docker-compose down -v
docker-compose up -d postgresql
```

### 5. Kafka 연결 오류

```bash
# 원인: Kafka가 완전히 시작되기 전에 서비스가 실행됨
# 해결: depends_on + healthcheck 활용
depends_on:
  kafka:
    condition: service_healthy
```

### 6. Hocuspocus WebSocket 연결 실패

```bash
# 원인: CORS 설정 오류
# 해결: Hocuspocus 서버 환경 변수 확인
CORS_ORIGIN=http://localhost:5173,http://localhost:3000
```

### 7. 서비스 간 통신 지연

```bash
# 원인: Eureka 캐시
# 해결: 강제 새로고침
POST http://localhost:8080/actuator/refresh
```

---

## 📈 모니터링 및 로깅

### Actuator Endpoints

```bash
# 헬스 체크
GET http://localhost:8081/actuator/health

# 메트릭스
GET http://localhost:8081/actuator/metrics

# Prometheus 형식
GET http://localhost:8081/actuator/prometheus
```

### 로그 집계 (ELK Stack)

```bash
# Elasticsearch로 로그 전송
logstash:
  hosts: ["localhost:5044"]
  index: "amapill-logs-%{+YYYY.MM.dd}"

# Kibana 대시보드
http://localhost:5601
```

---

## 🔐 보안 체크리스트

- [x] JWT Secret은 환경 변수로 관리
- [x] 데이터베이스 비밀번호 Docker Secret 사용
- [x] API Gateway에서 JWT 검증
- [x] HTTPS 강제 (운영 환경)
- [x] Rate Limiting 활성화
- [x] CORS 화이트리스트 설정
- [x] SQL Injection 방지 (PreparedStatement)
- [x] XSS 방지 (Content Security Policy)

---

## 📞 문의 및 지원

- **GitHub Issues**: [KOSA2025-FINAL-PROJECT-TEAM3/Front/issues](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/issues)
- **Wiki**: [프로젝트 위키](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/wiki)

---

**최종 수정일**: 2025-11-06
**버전**: 1.0
**작성자**: 뭐냑? 개발팀
