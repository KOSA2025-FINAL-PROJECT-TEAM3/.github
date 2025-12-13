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

뭐냑?는 **2개의 핵심 서비스 (Auth + Core)**로 구성된 마이크로서비스 아키텍처를 채택합니다.

### 핵심 원칙

1. **통합 서비스 구조**: Auth Service (인증) + Core Service (비즈니스 로직)
2. **데이터베이스 분리**: MySQL(트랜잭션) + PostgreSQL(공동편집 동기화)
3. **이벤트 기반 통신**: Kafka를 통한 비동기 메시징
4. **독립 배포**: 각 서비스는 독립적으로 배포 가능
5. **수평 확장**: 부하에 따라 개별 서비스 스케일 아웃
6. **Eureka/Config Server 미사용**: 직접 라우팅 방식 채택

---

## 📦 9-Stack 구성

### 인프라 레이어 (1개)

| 서비스 | 포트 | 역할 | 기술 스택 | 상태 |
|--------|------|------|-----------|------|
| **API Gateway** | 8080 | JWT 인증, 11개 서비스 라우팅, Circuit Breaker | Spring Cloud Gateway, Resilience4j, Redis, Kafka | ✅ 구현 완료 |
| **Eureka Server** | - | 서비스 디스커버리 | - | ❌ 미사용 |
| **Config Server** | - | 중앙 설정 관리 | - | ❌ 미사용 |

### 비즈니스 서비스 레이어 (2개 - 통합 구조)

| 서비스 | 포트 | 주요 기능 | 데이터베이스 | ORM | 빌드 도구 |
|--------|------|-----------|--------------|-----|----------|
| **Auth Service** | 8081 | 회원가입, 로그인, JWT 발급, 사용자 관리 | MySQL + **Redis** | JPA | **Gradle** |
| **Core Service** | 8082 | 약/가족/식단/알림/OCR 통합 서비스 | MySQL | **MyBatis 3.0.3** | Gradle |

> **아키텍처 변경**: 기존 6개 마이크로서비스에서 2개(Auth + Core)로 통합. Core Service는 Clean Architecture + MyBatis 기반으로 구현.
>
> **Auth Service 변경사항 (v2.0)**:
> - 빌드 도구: Maven → **Gradle**
> - RefreshToken 저장소: MySQL → **Redis**
> - API 경로: `/api/auth/*` → `/auth/*`, `/api/users/*` → `/users/*`
> - User Entity: `role` → `userRole` + `customerRole`

### 실시간 동기화 레이어

| 서비스 | 포트 | 역할 | 데이터베이스 | 용도 |
|--------|------|------|--------------|------|
| **Core Service (WebSocket)** | 8082 | Spring WebSocket/STOMP | MySQL | 알림, 상태 동기화 |
| **Hocuspocus Server** | 1234 | Y.js CRDT 기반 실시간 동기화 | PostgreSQL | 공동편집 (게시글 편집) |

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

### API Gateway (8080) - 구현 완료

**역할**: JWT 인증, 마이크로서비스 라우팅, 장애 격리

**Repository**: [spring-cloud-api-gateway](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/spring-cloud-api-gateway)

```yaml
# 기술 스택
- Java 21
- Spring Boot 3.5.8
- Spring Cloud 2025.0.0
- Spring Cloud Gateway WebFlux (`spring-cloud-starter-gateway-server-webflux`)
- Redis 7 (Reactive 캐싱)
- Kafka (이벤트 발행)
- Resilience4j 2.1.0 (Circuit Breaker)
- JJWT 0.12.6 (JWT 검증)
- Gradle 8.7

# 프로젝트 구조
src/main/java/com/amapill/gateway/
├── GatewayApplication.java
├── config/
│   ├── CircuitBreakerConfig.java
│   └── KafkaConfig.java
├── controller/
│   └── FallbackController.java
├── event/
│   ├── GatewayRequestEvent.java
│   └── GatewayEventProducer.java
├── filter/
│   ├── GatewayJwtAuthenticationFilter.java
│   ├── KafkaLoggingFilter.java
│   └── CacheableResponseFilter.java
└── service/
    └── JwtService.java

# 마이크로서비스 라우팅 (12개)
/api/auth/**         → Auth Service (8081)
/api/family/**       → Core Service (8082)
/ws/**               → Core Service WebSocket (8082)
/api/medications/**  → Core Service (8082)
/api/diet/**         → Core Service (8082)
/api/ocr/**          → Core Service (8082)
/api/chat/**         → Core Service (8082)
/api/search/**       → Core Service (8082)
/api/disease/**      → Core Service (8082)
/api/counsel/**      → Core Service (8082)
/api/notifications/**→ Core Service (8082)
/api/reports/**      → Core Service (8082)
/api/voice/**        → Core Service (8082)

# 인증 제외 경로
- /api/auth/login, /api/auth/signup, /api/auth/kakao-login, /api/auth/refresh
- /actuator/health, /health

# X-User-* 헤더 주입 (9개)
- X-User-Id, X-User-Email, X-User-Name, X-User-Profile-Image
- X-User-Role, X-Customer-Role
- X-Token-Subject, X-Token-Type, X-Request-Id

# Circuit Breaker 설정
| 서비스 | Failure Rate | Wait Duration |
|--------|--------------|---------------|
| 기본 (10개) | 50% | 10초 |
| ocr-service | 60% | 15초 |

# 환경 변수
JWT_SECRET: JWT 서명 시크릿 (Base64)
KAFKA_BOOTSTRAP: Kafka 부트스트랩 서버 (localhost:9092)
REDIS_HOST: Redis 호스트 (localhost)
REDIS_PORT: Redis 포트 (6379)
REDIS_PASSWORD: Redis 비밀번호 (redis123)

# 구현 완료 항목
✅ JWT 인증 필터 (GatewayJwtAuthenticationFilter)
✅ JWT 토큰 검증 서비스 (JwtService)
✅ 11개 마이크로서비스 라우팅 설정
✅ Circuit Breaker 설정 (Resilience4j)
✅ Fallback 컨트롤러
✅ Kafka 이벤트 발행 (요청/응답/에러)
✅ Redis 응답 캐싱
✅ CORS 설정
✅ Actuator 메트릭 (Prometheus)
```

---

### 비즈니스 서비스

### 1. Auth Service (8081)

**역할**: 인증 및 권한 관리

**Repository**: [auth-service](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/auth-service)

```yaml
# 주요 API (경로 변경: /api/auth/* → /auth/*)
POST /auth/login             # 일반 로그인 (이메일/비밀번호)
POST /auth/signup            # 회원가입 (자동 로그인)
POST /auth/kakao-login       # 카카오 OAuth 로그인
POST /auth/select-role       # 역할 선택 (시니어/케어기버)
POST /auth/refresh           # Access Token 갱신
POST /auth/logout            # 로그아웃 (Refresh Token 삭제)
GET  /users/me               # 내 프로필 조회
PUT  /users/me               # 내 프로필 수정
DELETE /users/me             # 계정 비활성화

# OAuth 2.0 Flow
1. Frontend → Kakao 인가 서버: 인가 코드 요청
2. Kakao → Frontend: 인가 코드 (code) 반환
3. Frontend → Auth Service: code + redirectUri 전송
4. Auth Service → Kakao: code로 액세스 토큰 요청
5. Kakao → Auth Service: 사용자 정보 반환
6. Auth Service: JWT 생성 및 사용자 DB 저장/업데이트
7. Auth Service → Frontend: JWT 토큰 반환

# 기술 스택 (변경됨)
- Spring Boot 3.4.7, Java 21 LTS
- Spring Security 6.x
- Kakao OAuth 2.0 (소셜 로그인)
- JWT (JJWT 0.12.3, Access Token 15분, Refresh Token 7일)
- MySQL 8.0 (사용자 정보)
- Redis 6.0+ (Refresh Token 저장) ← 변경됨
- Spring Data JPA (Hibernate)
- Spring Data Redis ← 추가됨
- Gradle 8.x ← Maven에서 변경됨

# User Entity 필드 변경
- role → userRole (시스템 역할: ROLE_USER, ROLE_ADMIN)
- customerRole 추가 (고객 역할: SENIOR, CAREGIVER)
- passwordHash 추가 (일반 로그인용)

# JWT Claims 변경
- userId, name, email, profileImage
- userRole (기존 role에서 변경)
- customerRole (신규)
- type (ACCESS/REFRESH)

# CI/CD (Gradle로 변경)
- GitHub Actions (Gradle 빌드, 테스트, Docker 이미지 빌드)
- 빌드 명령어: ./gradlew clean build -x test --no-daemon
- 테스트 명령어: ./gradlew test --no-daemon
- JAR 경로: build/libs/auth-service-1.0.0.jar
- GitHub Container Registry (GHCR)
- GitOps: k8s-manifests 자동 업데이트 → ArgoCD 배포

# 보안
- JWT 기반 Stateless 인증
- Refresh Token Redis 저장 (무효화 가능)
- Spring Security Filter Chain
- CORS 설정
```

### 2. Core Service (8082) - 통합 서비스

**역할**: 약 관리, 가족 네트워크, 식단, 알림, OCR 통합

**Repository**: [spring-boot](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/spring-boot)

```yaml
# 기술 스택
- Spring Boot 3.5.8, Java 21 LTS
- MyBatis 3.0.3 (JPA 대신 사용)
- Spring AI 1.1.0 (OpenAI GPT-5 nano/mini/5)
- Apache Kafka
- Clean Architecture 4계층
- AWS S3 (v2)
- Google Cloud Vision

# MSA 인증
- Nginx Gateway에서 X-User-* 헤더로 사용자 정보 전달
- SecurityUtil로 헤더에서 사용자 정보 추출
- 전달 헤더: X-User-Id, X-User-Email, X-User-Name, X-User-Role

# 주요 API - 약 관리
GET    /api/medications              # 약 목록
POST   /api/medications              # 약 등록
PUT    /api/medications/{id}         # 약 수정
DELETE /api/medications/{id}         # 약 삭제
POST   /api/medications/{id}/check   # 복용 체크

# 주요 API - 가족 관리
POST /api/family/groups              # 그룹 생성
POST /api/family/groups/{id}/invite  # 가족 초대
GET  /api/family/members             # 가족 구성원 조회

# 주요 API - 식단/상호작용
POST /api/diet/logs                  # 식단 기록
GET  /api/diet/warnings              # 충돌 경고 조회
POST /api/diet/check                 # 실시간 충돌 검사

# 주요 API - 알림
GET  /api/notifications              # 알림 목록
PUT  /api/notifications/{id}/read    # 읽음 처리

# 주요 API - OCR
POST /api/ocr/extract                # 이미지 → 텍스트 추출
POST /api/ocr/parse                  # 텍스트 → 약 정보 파싱

# Kafka 이벤트
- medication.created, medication.taken, medication.missed
- diet.warning
- notification.send

# Clean Architecture 레이어
- Domain: model/ (POJO), repository/ (@Mapper)
- Application: dto/, service/ (인터페이스)
- Infrastructure: service/ (구현체), external/, messaging/
- Presentation: controller/, websocket/
```

### Hocuspocus Server (1234)

**역할**: 실시간 협업 동기화 (게시글 공동편집 전용)

> **주의**: Hocuspocus는 공동편집 기능에만 사용됩니다.
> 일반 실시간 통신 (알림, 복약 상태 동기화)은 Core Service의 Spring WebSocket/STOMP를 사용합니다.

**상세 아키텍처**:
[ARCHITECTURE.md](./ARCHITECTURE.md#4-실시간-동기화-아키텍처) 참조

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

**최종 수정일**: 2025-12-13
**버전**: 3.0 (MSA 통합 구조 + Voice API + Spring Boot 3.5.8)
**작성자**: 뭐냑? 개발팀
