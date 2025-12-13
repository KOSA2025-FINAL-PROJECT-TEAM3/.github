# 뭐냑? 프로젝트 컨벤션

> AMApill Project Conventions & Coding Standards

---

## 📋 목차

1. [Git 브랜치 전략](#-git-브랜치-전략)
2. [커밋 컨벤션](#-커밋-컨벤션)
3. [코드 네이밍 컨벤션](#-코드-네이밍-컨벤션)
4. [PR 규칙](#-pr-규칙)

---

## 🌿 Git 브랜치 전략

### 브랜치 구조

```
master (main)
  └── develop (dev)
        ├── feature/이슈번호-기능명-작업자
        ├── bugfix/이슈번호-버그명-작업자
        └── release/버전번호
```

### 브랜치 종류

| 브랜치 | 용도 | 머지 대상 |
|--------|------|----------|
| `master` | 프로덕션 배포용 | - |
| `develop` | 개발 통합 브랜치 | `master` |
| `feature/*` | 새 기능 개발 | `develop` |
| `bugfix/*` | 버그 수정 | `develop` |
| `hotfix/*` | 긴급 수정 | `master`, `develop` |
| `release/*` | 배포 준비 (AI 코드 테스트) | `develop`, `master` |

### 브랜치 네이밍 규칙

**형식**: `브랜치타입/이슈번호-작업내용-작업자이름`

#### 예시
```bash
# 기능 개발
feature/#3-admin-junsu
feature/#12-login-minsoo
feature/#25-medication-crud-jiwon

# 버그 수정
bugfix/#8-login-error-junsu
bugfix/#19-api-timeout-minsoo

# 릴리즈
release/v1.0.0
release/v1.2.0-beta

# 핫픽스
hotfix/#45-critical-security-junsu
```

### 브랜치 생성 및 작업 흐름

```bash
# 1. develop 브랜치에서 최신 코드 받기
git checkout develop
git pull origin develop

# 2. 새 브랜치 생성
git checkout -b feature/#10-medication-list-junsu

# 3. 작업 후 커밋
git add .
git commit -m "✨ Feat: 약 목록 조회 기능 구현"

# 4. 원격 브랜치에 푸시
git push -u origin feature/#10-medication-list-junsu

# 5. GitHub에서 Pull Request 생성 (develop으로)
```

---

## 📝 커밋 컨벤션

### 커밋 메시지 형식

**형식**: `이모지 타입: 간단한 설명`

```
✨ Feat: 약 등록 기능 구현

- 약 정보 입력 폼 추가
- 복용 스케줄 설정 기능
- OCR 연동 버튼 추가
```

### 커밋 타입

| 이모지 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| ✨ | **Feat** | 새로운 기능 추가 또는 개선 | `✨ Feat: 약 알림 기능 추가` |
| 🐛 | **Fix** | 버그 수정 | `🐛 Fix: 로그인 에러 수정` |
| 📝 | **Docs** | 문서 수정 (README, 주석 등) | `📝 Docs: API 명세서 업데이트` |
| 💬 | **Style** | 코드 포맷팅, 오타, 함수명 수정 | `💬 Style: 변수명 camelCase로 통일` |
| ♻️ | **Refactor** | 코드 리팩토링 (기능 변경 없음) | `♻️ Refactor: 약 조회 로직 개선` |
| ⚙️ | **Settings** | 설정 파일 변경 | `⚙️ Settings: Vite 설정 추가` |
| ✏️ | **Comment** | 주석 추가 및 변경 | `✏️ Comment: API 함수에 주석 추가` |
| 🧪 | **Test** | 테스트 코드 추가/수정 | `🧪 Test: 약 CRUD 테스트 추가` |
| 🚀 | **Deploy** | 배포 관련 | `🚀 Deploy: 프로덕션 배포 v1.0.0` |
| 🔧 | **Chore** | 빌드, 패키지 매니저 수정 | `🔧 Chore: 의존성 업데이트` |

### 커밋 메시지 작성 규칙

1. **제목과 본문 분리**: 빈 줄로 구분
2. **제목은 50자 이내**
3. **본문은 72자마다 줄바꿈**
4. **제목 끝에 마침표 금지**
5. **제목은 명령문으로 작성** ("추가함" ❌, "추가" ✅)

#### 좋은 예시 ✅
```
✨ Feat: 약 복용 체크 기능 구현

- 체크박스 클릭 시 복용 완료 처리
- 실시간으로 가족 구성원에게 알림 전송
- Hocuspocus로 실시간 동기화
```

#### 나쁜 예시 ❌
```
약 기능 추가함
```

### Conventional Commits 예시

```bash
# 기능 추가
git commit -m "✨ Feat: 카카오 로그인 연동"

# 버그 수정
git commit -m "🐛 Fix: 약 목록 무한 스크롤 오류 수정"

# 문서 수정
git commit -m "📝 Docs: README에 설치 가이드 추가"

# 스타일 수정
git commit -m "💬 Style: 함수명 camelCase로 변경"

# 리팩토링
git commit -m "♻️ Refactor: API 호출 로직 useQuery로 변경"

# 설정 변경
git commit -m "⚙️ Settings: ESLint 규칙 추가"

# 주석 추가
git commit -m "✏️ Comment: MedicationCard 컴포넌트 주석 추가"
```

---

## 💻 코드 네이밍 컨벤션

### Frontend (React)

#### 1. 패키지 / 폴더명
- **규칙**: 소문자 (lowercase)
- **예시**:
  ```
  ✅ medication
  ✅ auth
  ✅ shared
  ❌ Medication
  ❌ AUTH
  ```

#### 2. 변수
- **규칙**: camelCase
- **예시**:
  ```javascript
  ✅ const userName = "김시니어";
  ✅ const medicationList = [];
  ✅ const isLoggedIn = false;

  ❌ const UserName = "김시니어";
  ❌ const medication_list = [];
  ```

#### 3. 함수 / 메소드
- **규칙**: camelCase
- **접두사**: 동사 사용 (get, set, handle, fetch, create 등)
- **예시**:
  ```javascript
  ✅ function getMedications() { }
  ✅ const handleLogin = () => { };
  ✅ const fetchUserData = async () => { };

  ❌ function GetMedications() { }
  ❌ function medications() { }  // 동사 없음
  ```

#### 4. 컴포넌트 (JSX 파일)
- **규칙**: PascalCase
- **파일명**: 컴포넌트명과 동일
- **예시**:
  ```javascript
  // ✅ MedicationCard.jsx
  export const MedicationCard = ({ medication }) => { };

  // ✅ LoginForm.jsx
  export const LoginForm = () => { };

  // ❌ medicationCard.jsx
  // ❌ Medication_Card.jsx
  ```

#### 5. Hooks
- **규칙**: camelCase
- **접두사**: `use` 필수
- **예시**:
  ```javascript
  ✅ useMedications.js
  ✅ useAuth.js
  ✅ useDebounce.js

  ❌ Medications.js  // use 없음
  ❌ UseMedications.js  // PascalCase 사용
  ```

#### 6. 상수
- **규칙**: UPPER_SNAKE_CASE
- **예시**:
  ```javascript
  ✅ const API_BASE_URL = "https://api.amapill.com";
  ✅ const MAX_FILE_SIZE = 5 * 1024 * 1024;
  ✅ const USER_ROLES = {
    SENIOR: "senior",
    CAREGIVER: "caregiver"
  };

  ❌ const apiBaseUrl = "...";
  ❌ const MaxFileSize = 5000;
  ```

#### 7. Boolean 변수
- **규칙**: `is`, `has`, `should` 접두사 사용
- **예시**:
  ```javascript
  ✅ const isLoading = true;
  ✅ const hasError = false;
  ✅ const shouldRender = true;

  ❌ const loading = true;
  ❌ const error = false;
  ```

#### 8. Event Handler
- **규칙**: `handle` 접두사 사용
- **예시**:
  ```javascript
  ✅ const handleSubmit = (e) => { };
  ✅ const handleClick = () => { };
  ✅ const handleChange = (value) => { };

  ❌ const onSubmit = (e) => { };  // Props로 전달할 때만 on 사용
  ❌ const clickButton = () => { };
  ```

#### 9. Zustand Store
- **규칙**: camelCase + `Store` 접미사 + `.js`
- **예시**:
  ```javascript
  ✅ authStore.js
  ✅ medicationStore.js
  ✅ toastStore.js

  ❌ AuthStore.js  // PascalCase 사용
  ❌ auth.store.js  // 점 사용
  ```

#### 10. Context
- **규칙**: PascalCase + `Context` 접미사 + `.jsx`
- **예시**:
  ```javascript
  ✅ FamilyContext.jsx
  ✅ ThemeContext.jsx

  ❌ familyContext.jsx  // camelCase 사용
  ```

#### 11. API Client
- **규칙**: camelCase + `ApiClient` 접미사 + `.js`
- **예시**:
  ```javascript
  ✅ authApiClient.js
  ✅ medicationApiClient.js
  ✅ ocrApiClient.js

  ❌ AuthApiClient.js  // PascalCase 사용
  ❌ auth-api-client.js  // kebab-case 사용
  ```

#### 12. Service
- **규칙**: camelCase + `Service` 접미사 + `.js`
- **예시**:
  ```javascript
  ✅ familyService.js
  ✅ notificationService.js

  ❌ FamilyService.js  // PascalCase 사용
  ```

#### Frontend 파일 네이밍 요약표

| 대상 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 | PascalCase + `.jsx` | `MedicationCard.jsx` |
| Hooks | camelCase + `use` prefix + `.js` | `useMedications.js` |
| Zustand Store | camelCase + `Store` suffix + `.js` | `authStore.js` |
| Context | PascalCase + `Context` suffix + `.jsx` | `FamilyContext.jsx` |
| Service | camelCase + `Service` suffix + `.js` | `familyService.js` |
| API Client | camelCase + `ApiClient` suffix + `.js` | `authApiClient.js` |
| Utils | camelCase + `.js` | `formatting.js` |
| Constants | UPPER_SNAKE_CASE | `API_ENDPOINTS` |

---

### Backend (Java)

#### 1. 클래스
- **규칙**: PascalCase
- **예시**:
  ```java
  ✅ public class MedicationService { }
  ✅ public class UserRepository { }
  ✅ public class JwtTokenProvider { }

  ❌ public class medicationService { }
  ❌ public class Medication_Service { }
  ```

#### 2. 변수
- **규칙**: camelCase
- **예시**:
  ```java
  ✅ private String userName;
  ✅ private int medicationCount;
  ✅ private boolean isActive;

  ❌ private String UserName;
  ❌ private int medication_count;
  ```

#### 3. 메소드
- **규칙**: camelCase
- **접두사**: 동사 사용 (get, set, create, update, delete 등)
- **예시**:
  ```java
  ✅ public Medication getMedicationById(Long id) { }
  ✅ public void updateMedication(Medication medication) { }
  ✅ public boolean validateUser(User user) { }

  ❌ public Medication GetMedicationById(Long id) { }
  ❌ public void medication_update(Medication medication) { }
  ```

#### 4. 상수
- **규칙**: UPPER_SNAKE_CASE
- **예시**:
  ```java
  ✅ public static final String API_VERSION = "v1";
  ✅ public static final int MAX_RETRY_COUNT = 3;

  ❌ public static final String apiVersion = "v1";
  ❌ public static final int maxRetryCount = 3;
  ```

#### 5. 패키지
- **규칙**: 소문자 (lowercase)
- **예시**:
  ```java
  ✅ package com.amapill.medication.service;
  ✅ package com.amapill.domain.model;

  ❌ package com.amapill.Medication.Service;
  ```

#### 6. Interface
- **규칙**: PascalCase
- **접두사**: `I` 사용 (권장)
- **예시**:
  ```java
  ✅ public interface IMedicationService { }
  ✅ public interface IUserRepository { }

  // 또는
  ✅ public interface MedicationService { }
  ```

#### 7. Enum
- **규칙**: PascalCase (클래스), UPPER_SNAKE_CASE (값)
- **예시**:
  ```java
  ✅ public enum UserRole {
      SENIOR,
      CAREGIVER,
      ADMIN
  }

  ✅ public enum MealType {
      BREAKFAST,
      LUNCH,
      DINNER,
      SNACK
  }

  ❌ public enum userRole { }
  ❌ public enum UserRole { senior, caregiver }
  ```

#### 8. DTO / Entity
- **규칙**: PascalCase + Request/Response 접미사
- **예시**:
  ```java
  ✅ public class MedicationRequest { }
  ✅ public class UserResponse { }
  ✅ public class LoginRequest { }

  ❌ public class medicationRequest { }
  ❌ public class Medication_Request { }
  ```

#### 9. MyBatis 매퍼 명명 규칙 (MyBatis Mapper Naming Convention)

**배경:** Core Service는 JPA 대신 **MyBatis 3.0.3**을 사용합니다.

##### Repository 인터페이스 규칙
```java
// @Mapper 어노테이션 필수 (@Repository 아님)
@Mapper
public interface MedicationRepository {
    int insert(Medication medication);       // 생성 (INSERT)
    int update(Medication medication);       // 수정 (UPDATE)
    int deleteById(Long id);                 // 삭제 (DELETE)
    Medication findById(Long id);            // 단일 조회
    List<Medication> findByUserId(Long userId);  // 목록 조회
    List<Medication> findActiveByUserId(Long userId);  // 조건 조회
    long countByUserId(Long userId);         // 카운트
}
```

##### Model (POJO) 규칙
```java
// @Entity 사용하지 않음 (MyBatis용 POJO)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Medication {
    private Long id;
    private Long userId;
    private String name;
    private LocalDateTime createdAt;
}
```

##### XML 매퍼 파일 위치
```
src/main/resources/mappers/
├── family/
│   ├── FamilyGroupMapper.xml
│   └── FamilyMemberMapper.xml
├── medication/
│   ├── MedicationMapper.xml
│   └── MedicationScheduleMapper.xml
└── notification/
    └── NotificationMapper.xml
```

##### XML 매퍼 예시
```xml
<mapper namespace="com.amapill.backend.domain.repository.MedicationRepository">
    <resultMap id="MedicationResultMap" type="Medication">
        <id property="id" column="id"/>
        <result property="userId" column="user_id"/>
        <result property="name" column="name"/>
        <result property="createdAt" column="created_at"/>
    </resultMap>

    <insert id="insert" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO medications (user_id, name, created_at)
        VALUES (#{userId}, #{name}, NOW())
    </insert>

    <select id="findById" resultMap="MedicationResultMap">
        SELECT * FROM medications WHERE id = #{id}
    </select>
</mapper>
```

##### application.properties 설정
```properties
mybatis.mapper-locations=classpath:mappers/**/*.xml
mybatis.type-aliases-package=com.amapill.backend.domain.model
mybatis.configuration.map-underscore-to-camel-case=true
```

##### 메서드 명명 규칙 요약
*   **생성 (Creation):** `insert` (예: `int insert(User user)`)
*   **수정 (Update):** `update` (예: `int update(User user)`)
*   **삭제 (Deletion):** `deleteById` (예: `int deleteById(Long id)`)
*   **단일 조회:** `findById` (예: `User findById(Long id)`)
*   **목록 조회:** `findBy...` (예: `List<User> findByRole(String role)`)
*   **카운트:** `countBy...` (예: `long countByUserId(Long userId)`)

---

### Database (MySQL / PostgreSQL)

#### 1. 테이블명
- **규칙**: snake_case (복수형)
- **예시**:
  ```sql
  ✅ CREATE TABLE users ( ... );
  ✅ CREATE TABLE medications ( ... );
  ✅ CREATE TABLE family_groups ( ... );

  ❌ CREATE TABLE Users ( ... );
  ❌ CREATE TABLE Medication ( ... );  -- 단수형
  ❌ CREATE TABLE FamilyGroups ( ... );
  ```

#### 2. 컬럼명
- **규칙**: snake_case
- **예시**:
  ```sql
  ✅ user_id
  ✅ created_at
  ✅ medication_name
  ✅ family_group_id

  ❌ userId
  ❌ CreatedAt
  ❌ MedicationName
  ```

#### 3. Primary Key
- **규칙**: `id` 또는 `테이블명_id`
- **예시**:
  ```sql
  ✅ id
  ✅ user_id
  ✅ medication_id

  ❌ ID
  ❌ UserId
  ```

#### 4. Foreign Key
- **규칙**: `참조테이블명_id`
- **예시**:
  ```sql
  ✅ user_id (users 테이블 참조)
  ✅ medication_id (medications 테이블 참조)
  ✅ family_group_id (family_groups 테이블 참조)

  ❌ userId
  ❌ medicationId
  ```

#### 5. Boolean 컬럼
- **규칙**: `is_` 또는 `has_` 접두사
- **예시**:
  ```sql
  ✅ is_active
  ✅ is_deleted
  ✅ has_expired

  ❌ active
  ❌ deleted
  ```

#### 6. 날짜/시간 컬럼
- **규칙**: `_at` 또는 `_date` 접미사
- **예시**:
  ```sql
  ✅ created_at
  ✅ updated_at
  ✅ deleted_at
  ✅ birth_date
  ✅ expiry_date

  ❌ createdAt
  ❌ create_time
  ```

#### 7. Enum 컬럼
- **규칙**: snake_case
- **예시**:
  ```sql
  ✅ user_role (ENUM: 'senior', 'caregiver')
  ✅ meal_type (ENUM: 'breakfast', 'lunch', 'dinner')

  ❌ UserRole
  ❌ mealType
  ```

#### 8. Index
- **규칙**: `idx_테이블명_컬럼명`
- **예시**:
  ```sql
  ✅ CREATE INDEX idx_users_email ON users(email);
  ✅ CREATE INDEX idx_medications_user_id ON medications(user_id);

  ❌ CREATE INDEX UsersEmail ON users(email);
  ```

---

## 🔍 PR 규칙

### PR 제목 형식
**형식**: `[타입] 간단한 설명 (#이슈번호)`

```
✨ [Feat] 약 목록 조회 기능 구현 (#10)
🐛 [Fix] 로그인 에러 수정 (#15)
📝 [Docs] API 명세서 업데이트 (#20)
```

### PR 템플릿
`.github/PULL_REQUEST_TEMPLATE.md` 참조

### PR 리뷰 규칙
1. **최소 1명 이상 승인** 필요
2. **CI/CD 테스트 통과** 후 머지
3. **충돌 해결** 후 머지
4. **Squash and Merge** 권장 (커밋 히스토리 정리)

---

## 📚 참고 자료

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Java Code Conventions](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

---

**작성일**: 2025-11-07
**최종 수정일**: 2025-12-13
**버전**: 3.0 (MUI 스타일링 전환 반영)
**작성자**: 볰녕? 개발팀
**적용 범위**: Frontend (MUI), Backend (MyBatis), Database, Git
```
