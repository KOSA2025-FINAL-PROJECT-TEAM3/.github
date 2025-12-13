# 뭐냑? 개발 로드맵 - 실전 가이드

## 🎯 핵심 질문: 프론트엔드 vs 백엔드, 뭘 먼저?

### ✅ 답: 백엔드 인프라 먼저 → 그 다음 병렬 개발

```
Week 1 (전체 팀): 백엔드 인프라 구축
  ├─ Database 설정
  ├─ JWT 인증 시스템
  └─ 기본 API 틀

Week 2-6 (병렬 개발): 기능 개발
  ├─ 팀원 1: Backend API 개발
  ├─ 팀원 2: Frontend UI 개발
  └─ 팀원 3: 통합 & 인프라

Week 7: 테스트 & 배포 & 발표 준비
```

---

## 📅 Week 1 상세 일정 (가장 중요!)

### Day 1-2: 프로젝트 초기 설정

#### 🔧 Backend (Spring Boot) 생성

```bash
# Spring Initializr로 프로젝트 생성
# https://start.spring.io/

필수 의존성:
✅ Spring Web
✅ Spring Data JPA
✅ Spring Security
✅ MySQL Driver
✅ Lombok
✅ Validation
✅ JWT (io.jsonwebtoken:jjwt)
```

#### 🎨 Frontend (React + Vite) 설정

```bash
# 이미 있는 프로젝트 활용
npm install axios react-router-dom sass
npm install @tiptap/react @hocuspocus/provider
```

#### 📁 폴더 구조 생성

```bash
# Backend
backend/src/main/java/com/amapill/
├── domain/          # Entity, Repository
├── application/     # Service, DTO
├── infrastructure/  # 구현체
├── presentation/    # Controller
├── config/          # 설정
└── security/        # JWT

# Frontend (src-structure.md 참고)
frontend/src/
├── core/            # API, Utils
├── features/        # 기능 모듈
└── shared/          # 공통 컴포넌트
```

---

### Day 3: Database 설정

#### 1. MySQL 설치 & DB 생성

```sql
CREATE DATABASE amapill CHARACTER SET utf8mb4;
CREATE USER 'amapill_dev'@'localhost' IDENTIFIED BY 'dev_password';
GRANT ALL PRIVILEGES ON amapill.* TO 'amapill_dev'@'localhost';
```

#### 2. application.yml 설정

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/amapill
    username: amapill_dev
    password: dev_password
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true

jwt:
  secret: your-secret-key-min-256-bits
  expiration: 86400000  # 24시간
```

#### 3. User Entity 생성

```java
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    private String name;
    private String phone;

    @Enumerated(EnumType.STRING)
    private UserRole role;  // PARENT, CHILD

    private LocalDateTime createdAt;
}
```

---

### Day 4-5: JWT 인증 시스템 구현

#### 🔐 Backend: JWT Provider

```java
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String jwtSecret;

    public String generateToken(Authentication auth) {
        return Jwts.builder()
            .setSubject(auth.getName())
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + expiration))
            .signWith(getSigningKey())
            .compact();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }
}
```

#### 🔐 Backend: Security Config

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .sessionManagement().sessionCreationPolicy(STATELESS)
            .and()
            .authorizeRequests()
                .antMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated()
            .and()
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

#### 🔐 Backend: Auth Controller

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request) {
        Authentication auth = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                request.getEmail(),
                request.getPassword()
            )
        );

        String token = tokenProvider.generateToken(auth);
        return ResponseEntity.ok(new AuthResponse(token));
    }

    @PostMapping("/signup")
    public ResponseEntity<AuthResponse> signup(@RequestBody SignupRequest request) {
        // 회원가입 로직
        User user = userService.createUser(request);
        String token = tokenProvider.generateToken(...);
        return ResponseEntity.ok(new AuthResponse(token));
    }
}
```

#### 🎨 Frontend: API Client

```javascript
// src/core/services/api/ApiClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8080/api',
  headers: { 'Content-Type': 'application/json' }
});

// JWT 토큰 자동 추가
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 401 에러 시 자동 로그아웃
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### 🎨 Frontend: Auth Context

```javascript
// src/features/auth/context/AuthContext.jsx
import { createContext, useState, useContext } from 'react';
import apiClient from '../../../core/services/api/ApiClient';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { token, ...userData } = response.data;

      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);

      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

#### 🎨 Frontend: Login Component

```javascript
// src/features/auth/components/LoginForm.jsx
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(email, password);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>로그인</h2>

      {error && <div className="error">{error}</div>}

      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="이메일"
        required
      />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="비밀번호"
        required
      />

      <button type="submit">로그인</button>
    </form>
  );
};

export default LoginForm;
```

---

### Day 6-7: 테스트 & Week 1 마무리

#### ✅ Week 1 완료 체크리스트

**Backend:**
- [ ] Spring Boot 실행 성공 (`http://localhost:8080`)
- [ ] MySQL 연결 성공
- [ ] User 테이블 생성 확인
- [ ] POST /api/auth/signup 동작
- [ ] POST /api/auth/login 동작 (JWT 발급)
- [ ] Authorization 헤더로 보호된 API 접근 성공

**Frontend:**
- [ ] npm run dev 실행 성공 (`http://localhost:5173`)
- [ ] 로그인 페이지 렌더링
- [ ] 회원가입 페이지 렌더링
- [ ] 로그인 성공 → Dashboard 이동
- [ ] JWT 토큰 자동 전송 확인 (개발자 도구 Network 탭)
- [ ] 로그아웃 동작

#### 🧪 Postman 테스트

```bash
# 1. 회원가입
POST http://localhost:8080/api/auth/signup
Content-Type: application/json

{
  "email": "parent@test.com",
  "password": "password123",
  "name": "홍길동",
  "phone": "010-1234-5678",
  "role": "PARENT"
}

# 2. 로그인
POST http://localhost:8080/api/auth/login
Content-Type: application/json

{
  "email": "parent@test.com",
  "password": "password123"
}

# 응답: { "token": "eyJhbGc..." }

# 3. 보호된 API 테스트
GET http://localhost:8080/api/users/me
Authorization: Bearer eyJhbGc...
```

---

## 📅 Week 2-6: 기능 개발 (병렬 가능!)

### Week 2: 약 관리 CRUD + 가족 네트워크

**Backend 담당자:**
```java
// Medication Entity, Repository, Service, Controller 구현
@Entity
public class Medication {
    private Long id;
    private Long userId;
    private String name;
    private String dosage;
    private String timing;
    // ...
}
```

**Frontend 담당자:**
```javascript
// 약 목록, 약 등록 폼 UI 구현
<MedicationList />
<MedicationForm />
```

**통합 담당자:**
- Hocuspocus 서버 설정
- 실시간 동기화 테스트

---

### Week 3: 약 스케줄 + 복용 체크

**Backend:**
- MedicationSchedule, MedicationLog 엔티티
- Kafka 이벤트 (복용 완료 시)

**Frontend:**
- 부모님용 체크리스트
- 자녀용 실시간 모니터링

---

### Week 4: OCR + 약-음식 충돌

**Backend:**
- Google Vision API 연동
- DrugFoodInteraction 데이터 구축

**Frontend:**
- 약봉지 스캔 UI
- 식단 입력 + 경고 표시

---

### Week 5: 알약 역검색 + 복약 순응도

**Backend:**
- 식약처 API 연동
- PDF 생성 (iText)

**Frontend:**
- 알약 검색 UI
- 리포트 차트

---

### Week 6: 통합 & 추가 기능

- 카카오톡 알림톡 (시간 있으면)
- 재고 관리
- 버그 수정

---

### Week 7: 테스트 & 배포

- 통합 테스트
- AWS/GCP 배포
- 발표 자료 제작

---

## 💡 개발 핵심 팁

### 1. **병렬 개발 전략**

Week 1 완료 후:
- **Backend 담당자**: API 개발 (Controller, Service)
- **Frontend 담당자**: UI 개발 (Component, Page)
- **통합 담당자**: 인프라 (Kafka, Hocuspocus, 배포)

### 2. **Mock Data 활용**

Backend API 완성 전에 Frontend 먼저 개발:

```javascript
// Mock API Client
export const mockMedications = [
  { id: 1, name: '아스피린', dosage: '1일 1회' },
  { id: 2, name: '혈압약', dosage: '1일 2회' }
];
```

### 3. **Git Branch 전략**

```bash
main
├── develop
├── feature/user-auth
├── feature/medication-crud
├── feature/medication-schedule
└── feature/ocr-scan
```

```bash
# 기능 개발 시작
git checkout develop
git checkout -b feature/medication-crud

# 개발 완료
git add .
git commit -m "feat: 약 CRUD API 구현"
git push origin feature/medication-crud

# Pull Request → Code Review → Merge
```

### 4. **일일 스탠드업 (15분)**

매일 오전:
- 어제 한 일
- 오늘 할 일
- 블로커 (막힌 부분)

---

## 🚨 Week 1 최소 목표 (MVP)

이것만 완성하면 Week 2부터 기능 개발 가능:

1. ✅ Backend 실행 성공
2. ✅ Database 연결
3. ✅ 회원가입/로그인 API 동작
4. ✅ JWT 인증 동작
5. ✅ Frontend 실행 성공
6. ✅ 로그인 UI → Dashboard 이동

**이 6가지만 되면 OK!**

---

## 📊 역할 분담 예시

### 팀원 1 (Backend 전문)
- Week 1: JWT 인증, User CRUD
- Week 2-3: Medication API
- Week 4: OCR Service
- Week 5-6: 식약처 API, PDF

### 팀원 2 (Frontend 전문)
- Week 1: 로그인/회원가입 UI
- Week 2-3: 약 관리 UI
- Week 4: OCR 스캔 UI
- Week 5-6: 리포트 UI, 차트

### 팀원 3 (Full-stack/인프라)
- Week 1: 프로젝트 초기 설정
- Week 2-3: Hocuspocus, Kafka
- Week 4-6: 통합 테스트, 배포

---

## 🎓 학습 자료

### Backend (Spring Boot)
- [Spring Boot 공식 문서](https://spring.io/projects/spring-boot)
- [JWT 인증 튜토리얼](https://jwt.io/introduction)
- [JPA 기초](https://spring.io/guides/gs/accessing-data-jpa/)

### Frontend (React)
- [React 공식 문서](https://react.dev/)
- [React Router](https://reactrouter.com/)
- [Axios 가이드](https://axios-http.com/)

---

## 🆘 자주 발생하는 에러

### CORS 에러
```java
// Backend: SecurityConfig.java
http.cors().configurationSource(request -> {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(Arrays.asList("http://localhost:5173"));
    config.setAllowedMethods(Arrays.asList("*"));
    config.setAllowedHeaders(Arrays.asList("*"));
    return config;
});
```

### JWT 401 Unauthorized
- JWT 토큰 만료 확인 (24시간)
- Authorization 헤더 형식: `Bearer {token}`
- 백엔드 JWT secret 키 일치 확인

### Database 연결 실패
- MySQL 서비스 실행 확인
- application.yml의 DB 정보 확인
- 방화벽 설정 확인

---

## 🎯 최종 조언

> **"완벽한 코드보다 일단 돌아가는 코드!"**

- Week 1은 **기반 구축**이 목표
- 리팩토링은 나중에
- 매일 커밋하고 푸시하기
- 막히면 팀원에게 바로 물어보기

**화이팅! 🚀**

---

**작성일**: 2025-11-05
**버전**: 1.0
**작성자**: AMApill Development Team
