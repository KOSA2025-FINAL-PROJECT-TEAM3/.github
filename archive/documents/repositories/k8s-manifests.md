# k8s manifests 분석

## 1) 목적

`k8s/` 디렉토리는 클러스터 배포에 필요한 리소스를 선언합니다.
애플리케이션/데이터베이스/미들웨어를 네임스페이스별로 분리해 관리하며,
일부 리소스에는 ArgoCD 동기화를 위한 `sync-wave` 어노테이션이 포함되어 있습니다.

## 2) 디렉토리 구조(현재 레포 기준)

```
k8s/
├── applications/          # 앱(Backend) 리소스
├── core/                  # Ingress/스토리지/Cloudflared
├── database/              # MySQL/PostgreSQL/Redis + 관리자 도구
├── middleware/            # Kafka
├── docs/                  # 운영/가이드 문서(비코드)
├── scripts/               # 배포 보조 스크립트
└── .yamllint.yml
```

## 3) 네임스페이스

매니페스트에 정의된 네임스페이스:

- `applications`
- `database`
- `middleware`
- `apigateway`
- `ingress-nginx`
- `local-path-storage` (Local Path Provisioner)

## 4) 애플리케이션 리소스

### auth-service (`applications`)
- Deployment/Service/ConfigMap
- 포트: `8081`
- ConfigMap: `SPRING_PROFILES_ACTIVE=prod`, `SPRING_KAFKA_BOOTSTRAP_SERVERS` 등

### spring-boot (`applications`)
- Deployment/Service/ConfigMap
- 포트: `8082`
- ConfigMap: `SPRING_PROFILES_ACTIVE=prod`, `FRONTEND_BASE_URL`, `KAKAO_REDIRECT_URI` 등

### spring-cloud-api-gateway (`apigateway`)
- Deployment/Service/ConfigMap 2종(앱 설정 + 환경변수)
- 포트: `8080`
- `/app/config`에 `application.yml`, `application-prod.yml`을 마운트
- Core 서비스는 `/api/**`를 `spring-boot`로 라우팅

## 5) 데이터/미들웨어

### Database (`database`)
- MySQL: StatefulSet + Headless Service (`3306`)
- PostgreSQL(+pgvector): StatefulSet + Headless Service (`5432`)
- Redis: StatefulSet + Headless Service (`6379`)
- Admin 도구: Adminer, phpMyAdmin, Redis Commander

### Middleware (`middleware`)
- Kafka (KRaft, single broker): StatefulSet + Service (`9092`)

## 6) 네트워크/Ingress

- `core/ingress-storage.yaml`: Ingress-NGINX 컨트롤러 + Local Path 스토리지 클래스
- `core/cloudflared/*`: Cloudflared 터널 설정(게이트웨이/DB 용도)

## 7) 보안/설정

- DB 및 앱 비밀값은 `sealed-*.yaml`로 관리
- 앱별 ConfigMap으로 프로필/기본값 주입

