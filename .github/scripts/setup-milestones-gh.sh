#!/bin/bash

# 마일스톤 자동 생성 스크립트 (gh CLI 사용)
# 사용법: ./setup-milestones-gh.sh <repository>
# 예시: ./setup-milestones-gh.sh Front
#      ./setup-milestones-gh.sh Back

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
    echo -e "${YELLOW}사용법: $0 <repository>${NC}"
    echo -e "${YELLOW}예시: $0 Front${NC}"
    echo -e "${YELLOW}     $0 Back${NC}"
    exit 1
fi

REPO=$1
FULL_REPO="$ORG/$REPO"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          마일스톤 자동 생성 스크립트                    ║${NC}"
echo -e "${BLUE}║              (gh CLI 버전)                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}📦 저장소: $FULL_REPO${NC}"
echo ""

# gh CLI 설치 확인
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ gh CLI가 설치되어 있지 않습니다.${NC}"
    echo -e "${YELLOW}설치 방법: https://cli.github.com/${NC}"
    exit 1
fi

# gh CLI 인증 확인
if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ gh CLI 인증이 필요합니다.${NC}"
    echo -e "${YELLOW}다음 명령어로 로그인하세요: gh auth login${NC}"
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

# 마일스톤 생성
SUCCESS_COUNT=0
FAIL_COUNT=0

for i in $(seq 0 $((TOTAL - 1))); do
    TITLE=$(jq -r ".milestones[$i].title" "$JSON_FILE")
    DESCRIPTION=$(jq -r ".milestones[$i].description" "$JSON_FILE")
    DUE_ON=$(jq -r ".milestones[$i].due_on // empty" "$JSON_FILE")
    STATE=$(jq -r ".milestones[$i].state // \"open\"" "$JSON_FILE")

    echo -e "${BLUE}[$((i + 1))/$TOTAL]${NC} 생성 중: ${GREEN}$TITLE${NC}"

    # gh CLI로 마일스톤 생성
    CMD="gh api repos/$FULL_REPO/milestones -X POST -f title=\"$TITLE\" -f description=\"$DESCRIPTION\" -f state=\"$STATE\""

    # due_on이 있으면 추가
    if [ -n "$DUE_ON" ]; then
        CMD="$CMD -f due_on=\"$DUE_ON\""
    fi

    # 실행
    if eval $CMD &> /dev/null; then
        echo -e "  ${GREEN}✅ 성공${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "  ${RED}❌ 실패 (이미 존재하거나 권한 오류)${NC}"
        ((FAIL_COUNT++))
    fi

    # API Rate Limit 고려 (짧은 대기)
    sleep 0.5
done

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  완료 요약                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}✅ 성공: $SUCCESS_COUNT 개${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}❌ 실패: $FAIL_COUNT 개${NC}"
fi
echo ""
echo -e "${GREEN}🔗 마일스톤 확인: https://github.com/$FULL_REPO/milestones${NC}"
echo ""
