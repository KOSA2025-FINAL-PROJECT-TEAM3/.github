# docker-compose 분석

## 1) 목적

로컬 개발에서 **DB/캐시/메시징 인프라**를 빠르게 구동하고,
필요 시 Gateway/Auth를 컨테이너로 함께 띄우는 구성을 제공합니다.

## 2) 기본 구성(프로필 없이 실행)

`docker-compose/docker-compose.yml` 기준 기본 서비스:

- MySQL `3306` (mysql:8.0)
- PostgreSQL `5432` (pgvector/pg16-trixie)
- Redis `6379` (redis:7-alpine)
- Kafka `9092` (Confluent 7.5, KRaft)
- Nginx `80` (SPA 정적서빙 + `/api`, `/ws` 프록시)
- phpMyAdmin `8888`
- redis-commander `8889`

## 3) 선택 구성(프로필 기반)

- `--profile services` 또는 `--profile full`
  - `api-gateway:8080`
  - `auth-service:8081`
- `--profile n8n`
  - `n8n:5678`
- `--profile hocuspocus`
  - `hocuspocus:1234`

아래 서비스는 Compose에 정의되어 있지만 **현재 레포에 코드가 없습니다**.
별도 레포가 필요합니다.

- `family-service`, `medication-service`, `diet-service`, `ocr-service`,
  `chat-service`, `search-service`, `disease-service`, `counsel-service`,
  `notification-service`, `report-service`

## 4) Nginx 프록시

`docker-compose/nginx.conf` 기준:

- `/api/**` → `host.docker.internal:8080` (Gateway)
- `/ws/**` → `host.docker.internal:8080` (Gateway WebSocket)
- `/health` → `200 ok`

## 5) DB 초기화

DB 스키마는 init scripts가 근거입니다.

- MySQL: `docker-compose/init-scripts/mysql/*.sql`
- PostgreSQL: `docker-compose/init-scripts/postgresql/*.sql`

## 6) 환경 변수(.env)

`.env.example`에 정의된 키:

- MySQL: `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
- PostgreSQL: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- Redis: `REDIS_PASSWORD`
- JWT: `JWT_SECRET`
- Kakao: `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`
- 기타: `N8N_HOST`, `TZ`

