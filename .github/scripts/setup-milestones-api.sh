#!/bin/bash

# 마일스톤 자동 생성 스크립트 (GitHub API 직접 사용)
# 사용법: GITHUB_TOKEN=your_token ./setup-milestones-api.sh <repository>
# 예시: GITHUB_TOKEN=ghp_xxx ./setup-milestones-api.sh Front
#       GITHUB_TOKEN=ghp_xxx ./setup-milestones-api.sh Back

set -e

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 조직명
ORG="KOSA2025-FINAL-PROJECT-TEAM3"

# 인자 확인
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ 오류: 저장소 이름을 입력해주세요${NC}"
    echo -e "${YELLOW}사용법: GITHUB_TOKEN=your_token $0 <repository>${NC}"
    echo -e "${YELLOW}예시: GITHUB_TOKEN=ghp_xxx $0 Front${NC}"
    echo -e "${YELLOW}     GITHUB_TOKEN=ghp_xxx $0 Back${NC}"
    exit 1
fi

REPO=$1
FULL_REPO="$ORG/$REPO"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          마일스톤 자동 생성 스크립트                    ║${NC}"
echo -e "${BLUE}║           (GitHub API 직접 호출)                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}📦 저장소: $FULL_REPO${NC}"
echo ""

# GitHub Token 확인
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ GITHUB_TOKEN 환경변수가 설정되지 않았습니다.${NC}"
    echo ""
    echo -e "${YELLOW}GitHub Personal Access Token이 필요합니다.${NC}"
    echo -e "${YELLOW}토큰 생성 방법:${NC}"
    echo -e "${YELLOW}  1. GitHub → Settings → Developer settings → Personal access tokens${NC}"
    echo -e "${YELLOW}  2. Generate new token (classic)${NC}"
    echo -e "${YELLOW}  3. repo 권한 선택${NC}"
    echo -e "${YELLOW}  4. 생성된 토큰 복사${NC}"
    echo ""
    echo -e "${YELLOW}사용법: GITHUB_TOKEN=your_token $0 $REPO${NC}"
    exit 1
fi

# 스크립트 디렉토리 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_FILE="$SCRIPT_DIR/../milestones.json"

# JSON 파일 확인
if [ ! -f "$JSON_FILE" ]; then
    echo -e "${RED}❌ milestones.json 파일을 찾을 수 없습니다.${NC}"
    echo -e "${YELLOW}경로: $JSON_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ JSON 파일 발견: $JSON_FILE${NC}"
echo ""

# jq 설치 확인
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ jq가 설치되어 있지 않습니다.${NC}"
    echo -e "${YELLOW}설치 방법:${NC}"
    echo -e "${YELLOW}  - macOS: brew install jq${NC}"
    echo -e "${YELLOW}  - Ubuntu/Debian: sudo apt-get install jq${NC}"
    echo -e "${YELLOW}  - CentOS/RHEL: sudo yum install jq${NC}"
    exit 1
fi

# curl 설치 확인
if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl이 설치되어 있지 않습니다.${NC}"
    exit 1
fi

# 마일스톤 개수 확인
TOTAL=$(jq '.milestones | length' "$JSON_FILE")
echo -e "${BLUE}📊 생성할 마일스톤: ${TOTAL}개${NC}"
echo ""

# 확인 메시지
echo -e "${YELLOW}⚠️  이 작업은 $FULL_REPO 저장소에 $TOTAL 개의 마일스톤을 생성합니다.${NC}"
read -p "계속하시겠습니까? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ 취소되었습니다.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🚀 마일스톤 생성 시작...${NC}"
echo ""

# GitHub API URL
API_URL="https://api.github.com/repos/$FULL_REPO/milestones"

# 마일스톤 생성
SUCCESS_COUNT=0
FAIL_COUNT=0

for i in $(seq 0 $((TOTAL - 1))); do
    TITLE=$(jq -r ".milestones[$i].title" "$JSON_FILE")
    DESCRIPTION=$(jq -r ".milestones[$i].description" "$JSON_FILE")
    DUE_ON=$(jq -r ".milestones[$i].due_on // empty" "$JSON_FILE")
    STATE=$(jq -r ".milestones[$i].state // \"open\"" "$JSON_FILE")

    echo -e "${BLUE}[$((i + 1))/$TOTAL]${NC} 생성 중: ${GREEN}$TITLE${NC}"

    # JSON 페이로드 생성
    PAYLOAD=$(jq -n \
        --arg title "$TITLE" \
        --arg description "$DESCRIPTION" \
        --arg state "$STATE" \
        '{title: $title, description: $description, state: $state}')

    # due_on이 있으면 추가
    if [ -n "$DUE_ON" ]; then
        PAYLOAD=$(echo "$PAYLOAD" | jq --arg due_on "$DUE_ON" '. + {due_on: $due_on}')
    fi

    # GitHub API 호출
    RESPONSE=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$PAYLOAD" \
        "$API_URL")

    # HTTP 상태 코드 추출
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" -eq 201 ]; then
        echo -e "  ${GREEN}✅ 성공${NC}"
        ((SUCCESS_COUNT++))
    elif [ "$HTTP_CODE" -eq 422 ]; then
        echo -e "  ${YELLOW}⚠️  이미 존재합니다${NC}"
        ((FAIL_COUNT++))
    else
        echo -e "  ${RED}❌ 실패 (HTTP $HTTP_CODE)${NC}"
        if command -v jq &> /dev/null; then
            ERROR_MSG=$(echo "$RESPONSE_BODY" | jq -r '.message // empty')
            if [ -n "$ERROR_MSG" ]; then
                echo -e "  ${RED}   오류: $ERROR_MSG${NC}"
            fi
        fi
        ((FAIL_COUNT++))
    fi

    # API Rate Limit 고려
    sleep 0.5
done

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  완료 요약                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}✅ 성공: $SUCCESS_COUNT 개${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠️  건너뜀/실패: $FAIL_COUNT 개${NC}"
fi
echo ""
echo -e "${GREEN}🔗 마일스톤 확인: https://github.com/$FULL_REPO/milestones${NC}"
echo ""

# 토큰 보안 경고
echo -e "${YELLOW}⚠️  보안 주의사항:${NC}"
echo -e "${YELLOW}  - GitHub Token은 절대 코드에 하드코딩하지 마세요${NC}"
echo -e "${YELLOW}  - 사용 후 토큰을 환경변수에서 삭제하세요: unset GITHUB_TOKEN${NC}"
echo -e "${YELLOW}  - 토큰이 노출되면 즉시 폐기하세요${NC}"
echo ""
