#!/bin/bash

# 실버케어 JSON Importer - ZIP 배포 파일 생성 스크립트

PLUGIN_NAME="silvercare-json-importer"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ZIP_NAME="${PLUGIN_NAME}-${TIMESTAMP}.zip"

echo "📦 피그마 플러그인 배포 ZIP 생성 중..."
echo ""

# code.js 확인 및 컴파일
if [ ! -f "code.js" ]; then
    echo "⚙️  code.js가 없습니다. TypeScript 컴파일을 시작합니다..."
    if command -v tsc &> /dev/null; then
        tsc code.ts --target es6
    else
        npx tsc code.ts --target es6
    fi

    if [ $? -ne 0 ]; then
        echo "❌ 컴파일 실패"
        exit 1
    fi
    echo "✅ 컴파일 완료"
fi

# 임시 디렉토리 생성
TEMP_DIR="temp-plugin"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

echo "📋 필수 파일 복사 중..."

# 필수 파일만 복사
cp manifest.json "$TEMP_DIR/" 2>/dev/null || { echo "❌ manifest.json 없음"; exit 1; }
cp code.js "$TEMP_DIR/" 2>/dev/null || { echo "❌ code.js 없음"; exit 1; }
cp ui.html "$TEMP_DIR/" 2>/dev/null || { echo "❌ ui.html 없음"; exit 1; }
cp INSTALL.md "$TEMP_DIR/" 2>/dev/null || echo "⚠️  INSTALL.md 없음 (선택사항)"

echo "✅ 파일 복사 완료"

# ZIP 생성
cd "$TEMP_DIR"
zip -q ../"$ZIP_NAME" *
cd ..

# 임시 디렉토리 삭제
rm -rf "$TEMP_DIR"

if [ -f "$ZIP_NAME" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✨ ZIP 파일 생성 완료!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📁 파일: $(pwd)/$ZIP_NAME"
    echo "📊 크기: $(du -h "$ZIP_NAME" | cut -f1)"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📤 팀원 공유 방법:"
    echo ""
    echo "1. 이 ZIP 파일을 팀원에게 전송"
    echo "   (Slack, 이메일, 드라이브 등)"
    echo ""
    echo "2. 팀원이 압축 해제:"
    echo "   unzip $ZIP_NAME"
    echo ""
    echo "3. 팀원이 Figma Desktop에서:"
    echo "   Plugins → Development → Import plugin from manifest..."
    echo "   → manifest.json 선택"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ ZIP 파일 생성 실패"
    exit 1
fi
