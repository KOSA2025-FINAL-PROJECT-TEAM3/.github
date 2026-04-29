# 🧩 마이크로서비스 구성 & 라우팅 (현재 코드 기준)

이 문서는 **Gateway/Auth/Core + docker-compose + k8s** 실제 설정을 기준으로 구성합니다.

관련 문서:
- 레포 분석 인덱스: [`documents/REPOSITORIES.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/REPOSITORIES.md)
- 전체 아키텍처: [`documents/ARCHITECTURE.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/ARCHITECTURE.md)

---

## 1) 서비스 구성(현재 구현)

| 구분 | 서비스 | 포트(로컬) | 핵심 책임 |
|---|---|---:|---|
| Entry | API Gateway (`spring-cloud-api-gateway`) | `8080` | JWT 검증 + 라우팅 + 캐싱 + CB |
| Auth | Auth Service (`auth-service`) | `8081` | 로그인/회원가입, Kakao OAuth, JWT 발급/갱신 |
| Core | Core Service (`spring-boot`) | `8082` | 가족/약/식단/OCR/알림/리포트/질병/채팅/Voice |
| Infra | MySQL/Redis/Kafka/PostgreSQL (`docker-compose`) | - | DB/캐시/메시징/벡터스토어 |

> `docker-compose`에는 향후 분리 마이크로서비스(예: family-service 등) 정의가 포함되어 있으나,
> 현재 레포에 해당 코드가 존재하지 않습니다.

---

## 2) 외부 진입점과 프록시

로컬 개발에서는 다음 2가지 진입점을 모두 사용할 수 있습니다.

1) Gateway 직접 호출: `http://localhost:8080`
2) Nginx(80) 경유 호출: `http://localhost`

`docker-compose/nginx.conf` 기준:

- `/api/**` → `host.docker.internal:8080` (Gateway)
- `/ws/**` → `host.docker.internal:8080` (Gateway WebSocket)

---

## 3) Gateway 라우팅 규칙

### 3.1 개발(`application-dev.yaml`)

- `/api/auth/**` → `http://localhost:8081` (Auth)
- `/api/appointments/**` → `http://localhost:8082`
- `/api/family/**` → `http://localhost:8082`
- `/api/family-chat/**` → `http://localhost:8082`
- `/api/prescriptions/**` → `http://localhost:8082`
- `/api/medications/**` → `http://localhost:8082`
- `/api/diet/**` → `http://localhost:8082`
- `/api/ocr/**` → `http://localhost:8082`
- `/api/chat/**` → `http://localhost:8082`
- `/api/search/**` → `http://localhost:8082`
- `/api/disease/**` → `http://localhost:8082`
- `/api/counsel/**` → `http://localhost:8082`
- `/api/notifications/**` → `http://localhost:8082`
- `/api/reports/**` → `http://localhost:8082`
- `/api/voice/**` → `http://localhost:8082`
- `/ws/**` → `http://localhost:8082` (WebSocket)
- SSE: `/api/notifications/subscribe`는 `response-timeout: 3600s`

### 3.2 K8s 배포(`k8s/.../spring-cloud-api-gateway/configmap.yaml`)

- `/api/auth/**` → `auth-service.applications.svc.cluster.local:8081`
- `/api/**` → `spring-boot.applications.svc.cluster.local:8082`
- `/ws/**` → `ws://spring-boot.applications.svc.cluster.local:8082`

---

## 4) 인증/인가 방식(헤더 주입)

- Gateway가 JWT를 검증한 뒤 `X-User-*` 헤더를 주입합니다.
- Core/Auth는 헤더 기반으로 사용자 컨텍스트를 구성합니다.
- SSE는 EventSource 제약으로 `token` 쿼리 파라미터를 허용합니다.

---

## 5) 로컬 개발 권장 플로우

1. `docker-compose`로 인프라만 실행(MySQL/PostgreSQL/Redis/Kafka/Nginx)
2. IDE에서 Gateway/Auth/Core를 각각 실행
3. 호출은 `http://localhost:8080/api/...` 또는 `http://localhost/api/...` 사용

빠른 시작: [`QUICKSTART.md`](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/QUICKSTART.md)

---

## 6) 환경 변수(민감정보 제외)

문서에는 “키 이름”만 기록합니다.

- 공통: `JWT_SECRET`, `REDIS_*`, `KAFKA_*`
- Auth: `SPRING_DATASOURCE_*`, `SPRING_DATA_REDIS_*`, `KAKAO_CLIENT_ID`, `KAKAO_CLIENT_SECRET`, `KAKAO_REDIRECT_URI`
- Core: `OPENAI_API_KEY`, `GOOGLE_VISION_API_KEY`, `DRUGINFO_API_SERVICE_KEY`, `AWS_*`

