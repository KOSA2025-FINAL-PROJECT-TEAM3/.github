# k8s-manifests 분석

## 1) 목적

Kubernetes 매니페스트를 GitOps 방식(ArgoCD)으로 관리합니다. 각 서비스의 배포 리소스를 선언하고,
CI/CD 파이프라인에서 이미지 업데이트가 반영되면 ArgoCD가 자동 배포합니다.

## 2) 레포 구조

```
k8s-manifests/
├── applications/          # 애플리케이션 배포 리소스
├── core/                  # Core 인프라 (Ingress/Storage 등)
├── database/              # DB 서비스 정의
├── middleware/            # Kafka/Eureka 등 미들웨어
└── .github/               # 매니페스트 검증 워크플로우
```

## 3) 주요 컴포넌트

- Kafka (KRaft 모드): Zookeeper 제거, 리소스 절감
- Eureka Server: 서비스 레지스트리
- Hocuspocus: 실시간 협업 서버
- n8n: 워크플로우 자동화

## 4) GitOps/CI-CD 흐름

1. 소스 코드 변경 → CI/CD로 이미지 빌드/푸시
2. k8s-manifests의 deployment.yaml 자동 업데이트
3. ArgoCD가 변경 감지 → 클러스터 배포

## 5) 보안/검증

- `.github/workflows/validate-manifests.yml`로 YAML 검증
- `SECURITY_REVIEW.md`에 보안 점검 기준 요약
