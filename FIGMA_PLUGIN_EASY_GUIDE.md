# 🎯 피그마 플러그인 - 매니페스트 없이 쉽게 사용하기

## ✨ 새로 추가된 기능

### 1️⃣ **로컬 스토리지 자동 저장/로드**
- JSON을 한번 붙여넣으면 **자동으로 저장**됩니다
- 다음에 플러그인을 열면 **자동으로 로드**됩니다
- 매번 복사-붙여넣기 할 필요 없음!

### 2️⃣ **클립보드 자동 감지**
- JSON을 복사한 상태로 플러그인을 열면
- **자동으로 클립보드에서 JSON을 감지**하여 붙여넣습니다
- 수동으로 붙여넣기 필요 없음!

### 3️⃣ **URL에서 직접 가져오기**
- **🌐 URL에서 가져오기** 버튼 클릭
- JSON 파일 URL 입력 (예: https://example.com/screens.json)
- 자동으로 다운로드하여 로드

---

## 🚀 사용 방법 (3가지)

### 방법 1: 클립보드 자동 감지 (가장 빠름! ⚡)

```bash
# 1. JSON 복사
cat figma-exports/all-screens-with-flows.json | pbcopy  # Mac
cat figma-exports/all-screens-with-flows.json | xclip -selection clipboard  # Linux

# 2. 피그마 플러그인 열기
# Plugins → Development → 실버케어 JSON Importer

# 3. 자동으로 클립보드에서 JSON 감지! ✨
# 바로 🚀 Import 버튼만 누르면 됨!
```

### 방법 2: 파일 드래그앤드롭

```
1. 피그마 플러그인 열기
2. JSON 파일을 플러그인 창으로 **드래그**
3. 자동으로 로드됨
4. 🚀 Import 버튼 클릭
```

### 방법 3: URL에서 가져오기 (팀 공유에 최적!)

```
1. JSON 파일을 웹 서버에 업로드
   - GitHub Raw URL
   - Gist
   - 간단한 HTTP 서버

2. 플러그인에서 🌐 URL에서 가져오기 클릭
3. URL 입력
4. 자동으로 다운로드 & 로드
5. 🚀 Import 버튼 클릭
```

---

## 🔧 한번만 설치하면 끝!

### 첫 설치 (1회만)

```bash
# 1. TypeScript 컴파일 (이미 되어있음)
cd figma-plugin
# code.js가 있으면 OK!

# 2. 피그마 Desktop 앱 열기
# 3. Plugins → Development → Import plugin from manifest...
# 4. figma-plugin/manifest.json 선택
```

### 이후 사용

```bash
# 매번 매니페스트 import 필요 없음!
# Plugins → Development → 실버케어 JSON Importer 클릭하면 바로 실행됨
```

---

## 💡 추천 워크플로우

### 시나리오 1: 로컬에서 작업

```bash
# 1. JSON 복사
cat figma-exports/all-screens-with-flows.json | pbcopy

# 2. 피그마 플러그인 열기 → 자동 감지 → Import 클릭
# 끝!
```

### 시나리오 2: 팀원과 공유

```bash
# 1. GitHub에서 Raw URL 복사
https://raw.githubusercontent.com/your-repo/main/figma-exports/all-screens.json

# 2. 팀원에게 URL 공유
# 3. 팀원은 플러그인에서 "URL에서 가져오기" → URL 입력 → Import
# 끝!
```

### 시나리오 3: 여러 버전 테스트

```bash
# 한번 붙여넣으면 자동 저장되므로
# 다른 버전을 테스트하려면:
# 1. 새 JSON 복사 → 플러그인 열기 (자동 감지)
# 2. 또는 파일 드래그앤드롭
# 3. 이전 버전은 로컬 스토리지에 저장되어 있음
```

---

## 🌐 URL 서버 예시

### GitHub Pages / GitHub Raw

```bash
# 1. JSON을 GitHub에 푸시
git add figma-exports/
git commit -m "Add Figma exports"
git push

# 2. Raw URL 사용
https://raw.githubusercontent.com/KOSA2025-FINAL-PROJECT-TEAM3/Front/main/figma-exports/all-screens-with-flows.json
```

### 간단한 로컬 HTTP 서버

```bash
# Python 사용
cd figma-exports
python3 -m http.server 8000

# 이제 URL 사용 가능:
http://localhost:8000/all-screens-with-flows.json
```

### GitHub Gist

```bash
# 1. gist.github.com에서 새 Gist 생성
# 2. JSON 내용 붙여넣기
# 3. "Raw" 버튼 클릭하여 URL 복사
# 예: https://gist.githubusercontent.com/username/xxx/raw/xxx/screens.json
```

---

## 🎯 매니페스트 없이 사용하는 다른 방법들

### 옵션 1: Figma Community에 플러그인 퍼블리시

```
1. 피그마에서:
   Plugins → Development → 실버케어 JSON Importer (우클릭)
   → Publish

2. 퍼블리시 후:
   - 플러그인 ID가 생성됨
   - 팀원들은 ID로 설치 가능
   - 매니페스트 필요 없음!
```

### 옵션 2: Figma Plugin URL

```
# 플러그인 ID를 알면:
figma://plugin/{plugin-id}

# 이 URL을 공유하면 바로 실행됨
```

---

## 📊 기능 비교

| 방법 | 속도 | 편의성 | 팀 공유 |
|------|------|--------|---------|
| **클립보드 자동 감지** | ⚡⚡⚡ | 🌟🌟🌟 | ⭐⭐ |
| **파일 드래그앤드롭** | ⚡⚡ | 🌟🌟🌟 | ⭐ |
| **URL에서 가져오기** | ⚡⚡ | 🌟🌟 | 🌟🌟🌟 |
| **로컬 스토리지 자동 로드** | ⚡⚡⚡ | 🌟🌟🌟 | ⭐ |
| **매니페스트 Import** | ⚡ | ⭐ | ⭐⭐ |

---

## ⚡ 키보드 단축키

- `Cmd/Ctrl + Enter` : 빠른 Import
- `Escape` : 플러그인 닫기

---

## ✅ 최종 추천 방법

### 개인 작업
1. JSON 복사
2. 플러그인 열기 (자동 감지!)
3. Cmd+Enter로 빠른 Import

### 팀 협업
1. GitHub Raw URL 공유
2. 팀원은 "URL에서 가져오기" 클릭
3. 한번 로드하면 로컬 스토리지에 저장되어 재사용 가능

---

**이제 매니페스트 import는 처음 한번만!** 🎉

Made with ❤️ for 실버케어 프로젝트
