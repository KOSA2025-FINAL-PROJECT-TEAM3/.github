# 🚀 뭐냑? JSON Importer - 빠른 설치 가이드

## 3분 안에 설치 완료!

### Step 1: 파일 준비 ✅

이 폴더의 파일들이 필요합니다:
- ✅ `manifest.json`
- ✅ `code.js` (없으면 아래 명령어 실행)
- ✅ `ui.html`

**`code.js`가 없다면** (처음 설치하는 경우):
```bash
npx tsc code.ts --target es6
```

### Step 2: Figma Desktop 앱 열기 🖥️

**중요**: 웹 브라우저 버전이 아닌 **Figma Desktop 앱**을 사용해야 합니다!

- 💻 [Figma Desktop 다운로드](https://www.figma.com/downloads/)

### Step 3: 플러그인 Import 📥

1. Figma Desktop 메뉴바에서:
   ```
   Plugins → Development → Import plugin from manifest...
   ```

2. 파일 선택 창에서:
   - `figma-plugin/manifest.json` 파일 선택
   - **열기** 클릭

3. 완료! ✨

### Step 4: 플러그인 실행 ▶️

1. Figma 파일 열기 (아무거나)
2. 메뉴:
   ```
   Plugins → Development → 뭐냑? JSON Importer
   ```
3. 플러그인 UI가 나타나면 성공! 🎉

---

## 📁 ZIP 파일로 받은 경우

1. **압축 해제**
   ```bash
   unzip figma-plugin.zip
   cd figma-plugin
   ```

2. **컴파일** (code.js가 없는 경우)
   ```bash
   npx tsc code.ts --target es6
   ```

3. **위의 Step 2-4 따라하기**

---

## ❓ 문제 해결

### "Import plugin from manifest" 메뉴가 안 보여요
→ **Figma Desktop 앱**을 사용하고 있나요? 웹 버전에서는 안 됩니다.

### "Cannot find manifest.json"
→ 정확한 파일을 선택했나요? `figma-plugin/manifest.json`이어야 합니다.

### "Plugin failed to load"
→ `code.js` 파일이 있나요? TypeScript 컴파일을 먼저 실행하세요:
```bash
npx tsc code.ts --target es6
```

### 플러그인 목록에 안 나타나요
→ Figma Desktop 앱을 재시작해보세요.

---

## 💡 팁

### 플러그인 업데이트하기
새 버전을 받았다면:
1. 파일 덮어쓰기
2. TypeScript 재컴파일 (code.ts가 변경된 경우)
3. Figma에서:
   ```
   Plugins → Development → 뭐냑? JSON Importer (우클릭) → Reload plugin
   ```

### 플러그인 삭제하기
Figma에서:
```
Plugins → Development → 뭐냑? JSON Importer (우클릭) → Remove
```

---

**도움이 필요하면 팀원에게 문의하세요!** 👋
