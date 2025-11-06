#!/bin/bash

# 실버케어 JSON Importer - 자동 설치 스크립트

echo "🚀 실버케어 JSON Importer 설치 시작..."
echo ""

# 현재 디렉토리 확인
if [ ! -f "manifest.json" ]; then
    echo "❌ 오류: manifest.json 파일을 찾을 수 없습니다."
    echo "   figma-plugin 폴더에서 이 스크립트를 실행하세요."
    exit 1
fi

echo "✅ manifest.json 확인 완료"

# code.js 파일 확인
if [ ! -f "code.js" ]; then
    echo "⚙️  code.js 파일이 없습니다. TypeScript 컴파일을 시작합니다..."

    # TypeScript 컴파일
    if command -v tsc &> /dev/null; then
        tsc code.ts --target es6
    else
        echo "📦 TypeScript를 찾을 수 없습니다. npx로 실행합니다..."
        npx tsc code.ts --target es6
    fi

    if [ $? -eq 0 ]; then
        echo "✅ TypeScript 컴파일 완료"
    else
        echo "❌ 컴파일 실패. 수동으로 실행하세요: npx tsc code.ts --target es6"
        exit 1
    fi
else
    echo "✅ code.js 파일 확인 완료"
fi

# ui.html 확인
if [ ! -f "ui.html" ]; then
    echo "❌ 오류: ui.html 파일을 찾을 수 없습니다."
    exit 1
fi

echo "✅ ui.html 확인 완료"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ 모든 파일 준비 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 다음 단계:"
echo ""
echo "1. Figma Desktop 앱을 실행하세요"
echo "   (웹 버전이 아닌 데스크톱 앱 필수!)"
echo ""
echo "2. Figma 메뉴에서:"
echo "   Plugins → Development → Import plugin from manifest..."
echo ""
echo "3. 파일 선택 창에서 이 파일을 선택하세요:"
echo "   $(pwd)/manifest.json"
echo ""
echo "4. 플러그인 실행:"
echo "   Plugins → Development → 실버케어 JSON Importer"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 INSTALL.md 파일에 더 자세한 설명이 있습니다."
echo ""
