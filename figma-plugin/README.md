# 뭐냑? JSON Importer - Figma 플러그인

JSON 와이어프레임을 Figma에 Auto Layout이 적용된 프레임으로 자동 변환하는 플러그인입니다.

## 👥 팀원과 공유하기

> 💡 **빠른 설치**: 팀원들에게 [INSTALL.md](./INSTALL.md) 파일을 공유하세요!

### 방법 1: 개발 플러그인으로 공유 (추천 - 빠르고 쉬움)

팀원들에게 이 저장소를 공유하고 아래 단계만 따라하면 됩니다:

#### 팀원 설치 방법 (자동):
```bash
cd Front/figma-plugin
./install.sh
# 그 다음 Figma Desktop에서 manifest.json import
```

#### 팀원 설치 방법 (수동):
1. **저장소 클론**
   ```bash
   git clone <repository-url>
   cd Front/figma-plugin
   ```

2. **TypeScript 컴파일** (한 번만)
   ```bash
   npx tsc code.ts --target es6
   ```

3. **Figma Desktop에서 Import**
   - Figma Desktop 앱 열기 (필수!)
   - **Plugins → Development → Import plugin from manifest...**
   - `manifest.json` 파일 선택
   - 완료! 🎉

### 방법 2: Private Organization 플러그인으로 퍼블리시 (프로 기능)

Figma Organization 계정이 있다면 가장 편리합니다:

1. **Figma Desktop에서 플러그인 열기**
   - Plugins → Development → 뭐냑? JSON Importer

2. **퍼블리시 준비**
   - 플러그인 우클릭 → **Publish new release...**
   - "Only visible to [Organization]" 선택
   - 설명과 아이콘 추가
   - **Publish** 클릭

3. **팀원 설치 (초간단!)**
   - Figma에서 Plugins → Find more plugins
   - "뭐냑? JSON Importer" 검색
   - **Install** 버튼 클릭
   - 끝!

### 방법 3: ZIP 파일로 공유 (Git 없는 팀원용)

Git을 사용하지 않는 팀원에게는 ZIP 파일로 공유:

1. **ZIP 파일 생성**
   ```bash
   cd figma-plugin
   ./create-plugin-zip.sh
   ```

2. **생성된 ZIP 파일 전송**
   - Slack, 이메일, Google Drive 등으로 공유
   - 파일명: `amapill-json-importer-[날짜].zip`

3. **팀원 설치**
   - ZIP 압축 해제
   - `INSTALL.md` 파일 참고하여 설치

### 방법 4: Public 퍼블리시 (선택사항)

Community에 공개하려면:
- [Figma Community Guidelines](https://help.figma.com/hc/en-us/articles/360038743434) 참고
- 플러그인 아이콘, 스크린샷, 설명 추가 필요
- 심사 시간: 1-2일

---

## 🚀 빠른 시작

### 1. TypeScript 컴파일

플러그인은 TypeScript로 작성되어 있으므로 JavaScript로 컴파일이 필요합니다.

```bash
# TypeScript 설치 (설치 안되어있다면)
npm install -g typescript

# 컴파일
cd figma-plugin
tsc code.ts --target es6
```

또는 간단하게:

```bash
cd figma-plugin
npx tsc code.ts --target es6
```

이제 `code.js` 파일이 생성됩니다.

---

### 2. Figma에 플러그인 설치

#### Step 1: Figma Desktop 앱 열기
- **중요**: Figma Desktop 앱을 사용하세요 (웹 버전에서는 로컬 플러그인 개발 불가)

#### Step 2: 플러그인 개발 모드 활성화

1. Figma 메뉴에서: **Plugins → Development → Import plugin from manifest...**
2. `figma-plugin/manifest.json` 파일 선택
3. 플러그인이 개발 플러그인 목록에 추가됩니다

#### Step 3: 플러그인 실행

1. Figma 파일 열기 (또는 새 파일 생성)
2. **Plugins → Development → 뭐냑? JSON Importer** 클릭
3. 플러그인 UI가 나타납니다

---

### 3. JSON Import 하기

#### Step 1: JSON 파일 복사

프로젝트 루트에서 JSON 파일 중 하나를 엽니다:

```bash
# 예시: 시니어 대시보드
cat figma-exports/01-dashboard-senior.json
```

전체 내용을 복사합니다 (Ctrl+A → Ctrl+C).

#### Step 2: 플러그인에 붙여넣기

1. 플러그인 UI의 텍스트 영역에 붙여넣기 (Ctrl+V)
2. **🚀 Import** 버튼 클릭
3. 자동으로 Figma 캔버스에 프레임 생성됨 ✨

#### Step 3: 생성 확인

다음이 자동으로 적용됩니다:
- ✅ Auto Layout (VERTICAL/HORIZONTAL)
- ✅ Spacing (itemSpacing, padding)
- ✅ Corner Radius
- ✅ Colors (fills, strokes)
- ✅ Typography (fontSize, fontName)
- ✅ Nested Frames & Components

---

## 📁 지원하는 JSON 파일

| 파일명 | 설명 |
|--------|------|
| `01-dashboard-senior.json` | 시니어 대시보드 |
| `02-dashboard-caregiver.json` | 보호자 대시보드 |
| `03-medications.json` | 약 관리 화면 |
| `04-family.json` | 가족 관리 화면 |

---

## 🎨 지원하는 Figma 요소

### 노드 타입
- `FRAME` - 프레임 (Auto Layout 지원)
- `COMPONENT` - 컴포넌트 (Auto Layout 지원)
- `TEXT` - 텍스트
- `RECTANGLE` - 사각형
- `ELLIPSE` - 원/타원

### Auto Layout 속성
- `layoutMode`: `"VERTICAL"` | `"HORIZONTAL"` | `"NONE"`
- `primaryAxisSizingMode`: `"FIXED"` | `"AUTO"`
- `counterAxisSizingMode`: `"FIXED"` | `"AUTO"`
- `primaryAxisAlignItems`: `"MIN"` | `"CENTER"` | `"MAX"` | `"SPACE_BETWEEN"`
- `counterAxisAlignItems`: `"MIN"` | `"CENTER"` | `"MAX"`
- `itemSpacing`: 숫자 (요소 간 간격)
- `paddingTop/Right/Bottom/Left`: 숫자

### 스타일 속성
- `fills`: 배경색 배열
- `strokes`: 테두리색 배열
- `strokeWeight`: 테두리 두께
- `cornerRadius`: 모서리 둥글기
- `fontSize`: 텍스트 크기
- `fontName`: 폰트 (family, style)

---

## 🛠 개발자 가이드

### 플러그인 수정하기

`code.ts` 파일을 수정한 후:

```bash
# 재컴파일
tsc code.ts --target es6

# Figma에서 플러그인 새로고침
# Plugins → Development → 뭐냑? JSON Importer (우클릭) → Reload plugin
```

### UI 수정하기

`ui.html` 파일을 직접 수정 가능 (컴파일 필요 없음)

```bash
# 수정 후 플러그인 새로고침만 하면 됨
```

---

## 🔧 문제 해결

### 1. "Font not available" 경고

Inter 폰트가 시스템에 설치되어 있지 않은 경우:

**해결법**:
- [Google Fonts](https://fonts.google.com/specimen/Inter)에서 Inter 폰트 다운로드
- 시스템에 설치
- Figma Desktop 재시작

또는 `code.ts`에서 기본 폰트를 변경:

```typescript
// 42번째 줄 근처
await figma.loadFontAsync({ family: 'Roboto', style: 'Regular' });
```

### 2. "Invalid JSON structure" 오류

JSON 형식이 올바른지 확인:
- [JSONLint](https://jsonlint.com/)에서 유효성 검사
- `type` 필드가 있는지 확인

### 3. 플러그인이 목록에 안 보임

- Figma **Desktop 앱**을 사용하고 있는지 확인 (웹 버전 안됨)
- `manifest.json` 파일 경로가 정확한지 확인
- Figma 재시작

### 4. TypeScript 컴파일 오류

```bash
# @figma/plugin-typings 설치
npm install --save-dev @figma/plugin-typings

# 또는 타입 체크 없이 강제 컴파일
tsc code.ts --target es6 --skipLibCheck
```

---

## 📚 참고 자료

- [Figma Plugin API](https://www.figma.com/plugin-docs/)
- [Figma Auto Layout](https://help.figma.com/hc/en-us/articles/360040451373)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 🎯 다음 단계

### 1. 디자인 커스터마이징
- 생성된 프레임에서 색상, 간격, 폰트 수정
- 실제 이미지/아이콘 추가
- 인터랙션 프로토타이핑

### 2. 컴포넌트 라이브러리 구축
- 반복되는 요소들을 컴포넌트로 변환
- Variants 추가 (상태별로)
- 팀 라이브러리로 퍼블리시

### 3. 개발 핸드오프
- Figma Inspect 패널에서 CSS/React 코드 추출
- Design Tokens를 코드로 export
- 개발자와 협업

---

## 💡 Tip

**키보드 단축키**:
- `Cmd/Ctrl + Enter`: 빠른 Import
- `Escape`: 플러그인 닫기

**대량 Import**:
- 여러 JSON 파일을 순차적으로 Import 가능
- 각 화면이 별도의 프레임으로 생성됨
- 생성 후 자동으로 뷰포트에 포커스됨

---

Made with ❤️ for 뭐냑? 프로젝트
