# 🚀 뭐냑? (AMApill) 빠른 시작 가이드 (Dev)

> 문서 목적: “로컬에서 **인프라 + 백엔드**를 가장 빠르게 띄우는 방법”을 한 페이지로 정리합니다.  
> **민감정보(패스워드/키/토큰)는 문서에 포함하지 않습니다.**

## 0) 준비물

- Java 21
- Docker Desktop + Docker Compose
- (권장) IntelliJ IDEA

## 1) 인프라 먼저 띄우기 (권장)

`docker-compose` 레포지토리에서 `.env`를 준비하고 인프라를 실행합니다.

```bash
git clone https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/docker-compose.git
cd docker-compose

cp .env.example .env
docker compose up -d mysql postgresql redis kafka nginx
```

기본 포트:

- Nginx: `80` (SPA + `/api`, `/ws` 프록시)
- MySQL: `3306`
- PostgreSQL: `5432`
- Redis: `6379`
- Kafka: `9092`

## 2) 백엔드 실행(로컬 IDE)

각 서비스는 로컬에서 띄우고, Nginx(80) → Gateway(8080)로 프록시되는 흐름을 사용합니다.

```bash
# API Gateway
cd ../spring-cloud-api-gateway
./gradlew bootRun --args='--spring.profiles.active=dev'

# Auth Service
cd ../auth-service
./gradlew bootRun --args='--spring.profiles.active=dev'

# Core Service
cd ../spring-boot
./gradlew bootRun
```

포트:

- API Gateway: `8080`
- Auth Service: `8081`
- Core Service: `8082`

## 3) 정상 동작 확인

```bash
curl http://localhost:8080/actuator/health
curl http://localhost:8081/actuator/health
curl http://localhost:8082/actuator/health
```

Core Swagger:

- `http://localhost:8082/swagger-ui.html`

## 4) API 호출 예시 (정확한 엔드포인트)

Gateway는 `/api`를 제거(StripPrefix=1)하고 내부로 전달합니다.

```bash
# 회원가입
curl -X POST http://localhost:8080/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@amapill.com","password":"password123","name":"테스트"}'

# 로그인
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@amapill.com","password":"password123"}'
```

## 5) 종료

```bash
cd ../docker-compose
docker compose down
```

## 다음 문서

- 레포 분석: `documents/REPOSITORIES.md`
- 아키텍처/라우팅: `documents/MICROSERVICES_SETUP.md`
- DB 근거 DDL: `documents/DATABASE_SCHEMA_ANALYSIS.md`

### npm install 실패

```bash
# 캐시 삭제
rm -rf node_modules package-lock.json
npm cache clean --force

# 재설치
npm install
```

---

**최종 수정일**: 2025-12-13
**작성자**: 뭐냑? 개발팀
