# 📊 뭐냑? 프로젝트 - DB 스킬 활용 가이드

> 트리거, 커서, 배치 처리를 활용한 데이터베이스 최적화 전략

**작성일**: 2025-12-25 (Updated)
**프로젝트**: 뭐냑? (AMApill)
**문서 버전**: 1.0

---

## 📋 목차

- [1. DB 트리거 (Trigger)](#1-db-트리거-trigger)
- [2. DB 커서 (Cursor)](#2-db-커서-cursor)
- [3. DB 배치 (Batch)](#3-db-배치-batch)
- [4. 실시간 처리](#4-실시간-처리)
- [5. 권장 아키텍처](#5-권장-아키텍처)

---

## 1. DB 트리거 (Trigger)

### 🎯 트리거란?

데이터베이스에서 특정 이벤트(INSERT, UPDATE, DELETE)가 발생할 때 **자동으로 실행되는 프로시저**

### ✅ 뭐냑? 프로젝트에서 트리거 활용

#### 1.1 복약 기록 자동 통계 업데이트

**목적**: 약 복용 시 자동으로 통계 테이블 갱신 (복약 순응도 리포트용)

```sql
-- 약 복용 시 자동으로 통계 테이블 업데이트
DELIMITER $$

CREATE TRIGGER after_medication_taken
AFTER INSERT ON medication_logs
FOR EACH ROW
BEGIN
  -- 복약 횟수 증가
  UPDATE medication_statistics
  SET taken_count = taken_count + 1,
      last_taken_date = NEW.taken_at,
      updated_at = NOW()
  WHERE user_id = NEW.user_id
    AND medication_id = NEW.medication_id;

  -- 통계 레코드가 없으면 생성
  INSERT INTO medication_statistics
    (user_id, medication_id, taken_count, last_taken_date, created_at, updated_at)
  SELECT NEW.user_id, NEW.medication_id, 1, NEW.taken_at, NOW(), NOW()
  WHERE NOT EXISTS (
    SELECT 1 FROM medication_statistics
    WHERE user_id = NEW.user_id AND medication_id = NEW.medication_id
  );
END$$

DELIMITER ;
```

**장점**:
- ✅ 실시간 통계 갱신
- ✅ 애플리케이션 코드 간소화
- ✅ 데이터 일관성 보장

---

#### 1.2 가족 알림 자동 생성

**목적**: 약 미복용 시 가족에게 자동 알림 레코드 생성

```sql
DELIMITER $$

CREATE TRIGGER after_medication_missed
AFTER UPDATE ON medication_schedules
FOR EACH ROW
BEGIN
  -- 상태가 SCHEDULED → MISSED로 변경된 경우만
  IF NEW.status = 'MISSED' AND OLD.status = 'SCHEDULED' THEN
    -- 가족 구성원들에게 알림 생성
    INSERT INTO notifications (user_id, family_id, type, message, severity, created_at)
    SELECT
      fm.user_id,
      NEW.family_id,
      'MISSED_MEDICATION',
      CONCAT(
        (SELECT name FROM users WHERE id = NEW.user_id),
        '님이 ',
        NEW.medication_name,
        ' 복용을 놓쳤습니다.'
      ),
      'HIGH',
      NOW()
    FROM family_members fm
    WHERE fm.family_id = NEW.family_id
      AND fm.user_id != NEW.user_id  -- 본인 제외
      AND fm.role = 'GUARDIAN';      -- 보호자만
  END IF;
END$$

DELIMITER ;
```

**사용 시나리오**:
1. 스케줄러가 예정 시간 지난 약을 `MISSED` 상태로 변경
2. 트리거 자동 실행 → 가족에게 알림 레코드 생성
3. Notification Service가 알림 발송

---

#### 1.3 약-음식 충돌 이력 자동 기록

**목적**: 식단 등록 시 충돌 검사 이력 자동 기록 (감사 로그)

```sql
DELIMITER $$

CREATE TRIGGER after_diet_insert
AFTER INSERT ON diet_logs
FOR EACH ROW
BEGIN
  -- 충돌 검사 로그 기록
  INSERT INTO interaction_check_logs
    (user_id, diet_id, checked_at, check_type)
  VALUES
    (NEW.user_id, NEW.id, NOW(), 'AUTO_ON_INSERT');
END$$

DELIMITER ;
```

---

#### 1.4 감사 로그 (Audit Trail)

**목적**: 의료 정보 수정 시 누가 언제 무엇을 변경했는지 자동 기록

```sql
DELIMITER $$

CREATE TRIGGER after_medication_update
AFTER UPDATE ON medications
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs
    (table_name, record_id, action, old_value, new_value, changed_by, changed_at)
  VALUES (
    'medications',
    NEW.id,
    'UPDATE',
    JSON_OBJECT(
      'name', OLD.medication_name,
      'dosage', OLD.dosage,
      'frequency', OLD.frequency
    ),
    JSON_OBJECT(
      'name', NEW.medication_name,
      'dosage', NEW.dosage,
      'frequency', NEW.frequency
    ),
    NEW.updated_by,
    NOW()
  );
END$$

DELIMITER ;
```

**법적 준수**: 의료정보 보호법 대응

---

### ⚠️ 트리거 사용 시 주의사항

| 사용 권장 ✅ | 사용 비권장 ❌ |
|------------|--------------|
| ✅ 단순 통계 계산 | ❌ 복잡한 비즈니스 로직 |
| ✅ 감사 로그 자동 기록 | ❌ 외부 API 호출 |
| ✅ 참조 무결성 보장 | ❌ Kafka 이벤트 발행 |
| ✅ 타임스탬프 자동 업데이트 | ❌ 이메일/SMS 발송 |

**이유**: 트리거는 디버깅이 어렵고, 성능 문제 발생 시 추적 힘듦

---

## 2. DB 커서 (Cursor)

### 🎯 커서란?

쿼리 결과를 **한 행씩 순회하며 처리**하는 메커니즘

### ✅ 뭐냑? 프로젝트에서 커서 활용

#### 2.1 월간 복약 순응도 리포트 생성

**목적**: 한 달치 복약 기록을 순회하며 상세 리포트 생성

```sql
DELIMITER $$

CREATE PROCEDURE generate_monthly_report(
  IN p_user_id INT,
  IN p_month DATE
)
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE v_medication_id INT;
  DECLARE v_medication_name VARCHAR(255);
  DECLARE v_scheduled_count INT;
  DECLARE v_taken_count INT;
  DECLARE v_adherence_rate DECIMAL(5,2);

  -- 커서 선언: 약별 복용 통계
  DECLARE med_cursor CURSOR FOR
    SELECT
      m.id,
      m.medication_name,
      COUNT(ms.id) as scheduled_count,
      SUM(CASE WHEN ms.status = 'TAKEN' THEN 1 ELSE 0 END) as taken_count
    FROM medications m
    LEFT JOIN medication_schedules ms
      ON m.id = ms.medication_id
      AND ms.user_id = p_user_id
      AND DATE_FORMAT(ms.scheduled_date, '%Y-%m') = DATE_FORMAT(p_month, '%Y-%m')
    WHERE m.user_id = p_user_id
    GROUP BY m.id, m.medication_name;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  -- 임시 리포트 테이블 초기화
  DELETE FROM report_details_temp WHERE user_id = p_user_id;

  -- 커서 열기
  OPEN med_cursor;

  read_loop: LOOP
    FETCH med_cursor INTO
      v_medication_id,
      v_medication_name,
      v_scheduled_count,
      v_taken_count;

    IF done THEN
      LEAVE read_loop;
    END IF;

    -- 복약 순응도 계산
    SET v_adherence_rate =
      CASE
        WHEN v_scheduled_count > 0
        THEN (v_taken_count / v_scheduled_count) * 100
        ELSE 0
      END;

    -- 리포트 상세 데이터 삽입
    INSERT INTO report_details_temp
      (user_id, medication_id, medication_name, scheduled_count,
       taken_count, adherence_rate, report_month)
    VALUES
      (p_user_id, v_medication_id, v_medication_name, v_scheduled_count,
       v_taken_count, v_adherence_rate, p_month);

  END LOOP;

  CLOSE med_cursor;

  -- 최종 리포트 생성
  SELECT * FROM report_details_temp WHERE user_id = p_user_id;
END$$

DELIMITER ;
```

**사용 예시**:
```sql
CALL generate_monthly_report(123, '2025-11-01');
```

---

#### 2.2 가족 전체에게 일괄 알림 전송

**목적**: 여러 가족 구성원에게 순차적으로 알림

```sql
DELIMITER $$

CREATE PROCEDURE notify_family_members(
  IN p_family_id INT,
  IN p_message TEXT,
  IN p_notification_type VARCHAR(50)
)
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE v_user_id INT;

  -- 가족 구성원 커서
  DECLARE family_cursor CURSOR FOR
    SELECT user_id
    FROM family_members
    WHERE family_id = p_family_id
      AND role = 'GUARDIAN';  -- 보호자만

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN family_cursor;

  notify_loop: LOOP
    FETCH family_cursor INTO v_user_id;

    IF done THEN
      LEAVE notify_loop;
    END IF;

    -- 각 가족 구성원에게 알림 생성
    INSERT INTO notifications
      (user_id, family_id, type, message, created_at, is_read)
    VALUES
      (v_user_id, p_family_id, p_notification_type, p_message, NOW(), FALSE);

  END LOOP;

  CLOSE family_cursor;
END$$

DELIMITER ;
```

---

### ⚠️ 커서 사용 시 주의사항

**단점**:
- ❌ 성능이 느림 (행 단위 처리)
- ❌ 메모리 사용량 많음
- ❌ 복잡한 코드

**대안**:
- ✅ **Set-based 쿼리** (한 번에 여러 행 처리)
- ✅ **Spring Batch** (애플리케이션 레벨)

**커서 사용 권장 경우**:
- 각 행마다 복잡한 계산이 필요할 때
- 순차 처리가 필수일 때

---

## 3. DB 배치 (Batch)

### 🎯 배치란?

주기적으로 대량의 데이터를 일괄 처리하는 작업

### ✅ 뭐냑? 프로젝트에서 배치 활용

#### 3.1 매일 밤 복약 스케줄 미복용 체크

**실행 시간**: 매일 자정 (00:00)

```sql
DELIMITER $$

CREATE PROCEDURE check_missed_medications()
BEGIN
  -- 1. 어제 날짜의 미복용 약을 MISSED 상태로 변경
  UPDATE medication_schedules
  SET status = 'MISSED',
      updated_at = NOW()
  WHERE scheduled_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    AND status = 'SCHEDULED'
    AND scheduled_time < CURTIME();

  -- 2. 영향받은 행 수 로깅
  INSERT INTO batch_logs (batch_name, executed_at, rows_affected)
  VALUES ('check_missed_medications', NOW(), ROW_COUNT());

  -- 참고: 가족 알림은 트리거에서 자동 생성됨
END$$

DELIMITER ;
```

**스케줄링 방법**:
```sql
-- MySQL Event Scheduler 사용
CREATE EVENT daily_check_missed_medications
ON SCHEDULE EVERY 1 DAY
STARTS '2025-11-07 00:00:00'
DO
  CALL check_missed_medications();
```

---

#### 3.2 매주 복약 순응도 통계 계산

**실행 시간**: 매주 월요일 오전 1시

```sql
DELIMITER $$

CREATE PROCEDURE calculate_weekly_adherence()
BEGIN
  -- 지난 주 통계 집계
  INSERT INTO adherence_weekly_stats
    (user_id, medication_id, week_start_date, week_end_date,
     total_scheduled, taken_count, adherence_rate, calculated_at)
  SELECT
    user_id,
    medication_id,
    DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 7 DAY) as week_start,
    DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 1 DAY) as week_end,
    COUNT(*) as total_scheduled,
    SUM(CASE WHEN status = 'TAKEN' THEN 1 ELSE 0 END) as taken_count,
    ROUND(
      (SUM(CASE WHEN status = 'TAKEN' THEN 1 ELSE 0 END) / COUNT(*)) * 100,
      2
    ) as adherence_rate,
    NOW()
  FROM medication_schedules
  WHERE scheduled_date >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 7 DAY)
    AND scheduled_date < DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 1 DAY)
  GROUP BY user_id, medication_id;

  -- 배치 로그
  INSERT INTO batch_logs (batch_name, executed_at, rows_affected)
  VALUES ('calculate_weekly_adherence', NOW(), ROW_COUNT());
END$$

DELIMITER ;
```

```sql
-- 매주 월요일 오전 1시 실행
CREATE EVENT weekly_adherence_calculation
ON SCHEDULE EVERY 1 WEEK
STARTS '2025-11-11 01:00:00'  -- 다음 월요일
DO
  CALL calculate_weekly_adherence();
```

---

#### 3.3 만료 임박 약 알림

**실행 시간**: 매일 오전 9시

```sql
DELIMITER $$

CREATE PROCEDURE notify_expiring_medications()
BEGIN
  -- 유효기간 7일 이내인 약 조회 후 알림 생성
  INSERT INTO notifications
    (user_id, type, message, severity, created_at, is_read)
  SELECT
    user_id,
    'EXPIRING_SOON',
    CONCAT(
      medication_name,
      ' 유효기간 ',
      DATEDIFF(expiry_date, CURDATE()),
      '일 남음 (',
      DATE_FORMAT(expiry_date, '%Y-%m-%d'),
      ')'
    ),
    CASE
      WHEN DATEDIFF(expiry_date, CURDATE()) <= 3 THEN 'HIGH'
      WHEN DATEDIFF(expiry_date, CURDATE()) <= 7 THEN 'MEDIUM'
      ELSE 'LOW'
    END,
    NOW(),
    FALSE
  FROM user_medications
  WHERE expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
    AND is_deleted = FALSE;

  -- 배치 로그
  INSERT INTO batch_logs (batch_name, executed_at, rows_affected)
  VALUES ('notify_expiring_medications', NOW(), ROW_COUNT());
END$$

DELIMITER ;
```

```sql
-- 매일 오전 9시 실행
CREATE EVENT daily_expiry_notification
ON SCHEDULE EVERY 1 DAY
STARTS '2025-11-07 09:00:00'
DO
  CALL notify_expiring_medications();
```

---

#### 3.4 오래된 알림 자동 삭제 (Cleanup)

**실행 시간**: 매주 일요일 새벽 3시

```sql
DELIMITER $$

CREATE PROCEDURE cleanup_old_notifications()
BEGIN
  -- 30일 이상 된 읽은 알림 삭제
  DELETE FROM notifications
  WHERE is_read = TRUE
    AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

  -- 배치 로그
  INSERT INTO batch_logs (batch_name, executed_at, rows_affected)
  VALUES ('cleanup_old_notifications', NOW(), ROW_COUNT());
END$$

DELIMITER ;
```

```sql
-- 매주 일요일 새벽 3시
CREATE EVENT weekly_notification_cleanup
ON SCHEDULE EVERY 1 WEEK
STARTS '2025-11-10 03:00:00'  -- 다음 일요일
DO
  CALL cleanup_old_notifications();
```

---

### 📊 배치 작업 모니터링

**배치 로그 테이블**:
```sql
CREATE TABLE batch_logs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  batch_name VARCHAR(100) NOT NULL,
  executed_at DATETIME NOT NULL,
  rows_affected INT DEFAULT 0,
  execution_time_ms INT,
  status ENUM('SUCCESS', 'FAILED') DEFAULT 'SUCCESS',
  error_message TEXT,
  INDEX idx_batch_name (batch_name),
  INDEX idx_executed_at (executed_at)
);
```

**배치 작업 조회**:
```sql
-- 오늘 실행된 배치 작업
SELECT * FROM batch_logs
WHERE DATE(executed_at) = CURDATE()
ORDER BY executed_at DESC;

-- 배치별 실행 이력
SELECT
  batch_name,
  COUNT(*) as execution_count,
  AVG(rows_affected) as avg_rows,
  MAX(executed_at) as last_executed
FROM batch_logs
GROUP BY batch_name;
```

---

## 4. 실시간 처리

### 🔴 뭐냑? 프로젝트의 실시간 처리 영역

#### 4.1 가족 돌봄 네트워크 (MVP 핵심)

**요구사항**:
- 부모님이 약 복용 → 자녀에게 **즉시** 알림
- 예정 시간 지남 → 자녀에게 **실시간** 미복용 경고
- 자녀가 실시간으로 부모님 복용 상태 모니터링

**기술 스택**:
```
SSE (EventSource) - 실시간 알림(복약/식단/OCR/초대 등)
    +
Spring WebSocket/STOMP - 실시간 채팅
    ↓
(주요 상태 저장) MySQL 트랜잭션 데이터

(선택) 공동편집/CRDT가 필요한 경우에만 Hocuspocus + Y.js 도입
```

**데이터 흐름**:
```
부모님 앱: 약 복용 버튼 클릭
    ↓
Frontend → Backend API (복용 로그 기록)
    ↓
Backend → 알림 이벤트 생성
    ↓
SSE Push → 자녀 앱: 실시간 알림 표시
```

---

#### 4.2 약-음식 충돌 경고

**요구사항**:
- 식단 입력 즉시 약과의 충돌 검사
- 위험 음식 섭취 시 **즉시** 경고

**기술 스택**:
```
Frontend: 식단 입력
    ↓
Backend API: Diet Service
    ↓
Rule Engine: 약-음식 충돌 검사
    ↓
Kafka Event: FOOD_INTERACTION_DETECTED
    ↓
Notification Service
    ↓
WebSocket Push → Frontend
```

**Kafka Event 예시**:
```json
{
  "eventType": "FOOD_INTERACTION_DETECTED",
  "userId": 123,
  "medication": "와파린",
  "food": "시금치",
  "severity": "HIGH",
  "message": "와파린 복용 중 시금치 섭취는 약효를 감소시킬 수 있습니다.",
  "timestamp": "2025-11-07T14:30:00Z"
}
```

---

#### 4.3 약사 1:1 채팅

**요구사항**:
- 약사와 실시간 상담
- 메시지 즉시 전송/수신

**기술 스택**:
```
Spring WebSocket/STOMP (채팅)
    ↓
MySQL 저장 + (선택) Kafka 이벤트
```

---

#### 4.4 OCR 처리 상태

**요구사항**:
- 약봉지 사진 업로드 → 처리 진행률 실시간 표시
- "분석 중 → 약 정보 추출 중 → 완료" 상태 업데이트

**기술 스택**:
```
SSE (Server-Sent Events)
```

**구현 예시**:
```java
@GetMapping(value = "/ocr/status/{taskId}", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<OcrStatusDto>> getOcrStatus(@PathVariable String taskId) {
    return ocrService.getStatusStream(taskId)
        .map(status -> ServerSentEvent.<OcrStatusDto>builder()
            .data(status)
            .build());
}
```

**Frontend**:
```javascript
const eventSource = new EventSource(`/api/ocr/status/${taskId}`);
eventSource.onmessage = (event) => {
  const status = JSON.parse(event.data);
  updateProgressBar(status.progress); // 0-100%
};
```

---

#### 4.5 알림 시스템

**요구사항**:
- 약 복용 시간 알림
- 가족 활동 알림 (약 등록, 복용 등)
- 시스템 알림 (만료 임박 등)

**기술 스택**:
```
Medication Service: 약 복용 이벤트 발생
    ↓
Kafka Topic: medication-events
    ↓
Notification Service: 이벤트 수신 → 알림 생성
    ↓
WebSocket Push → Frontend (실시간 알림)
```

---

## 5. 권장 아키텍처

### 🏗️ 뭐냑? 프로젝트 최종 권장 방식

| 기능 | DB 커서 | DB 배치 | Spring Batch | @Scheduled | 실시간 | **권장** |
|-----|---------|---------|--------------|-----------|--------|----------|
| 월간 리포트 생성 | 가능 | - | ✅ | - | - | **Spring Batch** |
| 미복용 체크 | - | 가능 | ✅ | ✅ | - | **@Scheduled** |
| 주간 통계 | - | 가능 | ✅ | - | - | **Spring Batch** |
| 만료 알림 | - | 가능 | - | ✅ | - | **@Scheduled** |
| 복약 알림 | - | - | - | - | ✅ | **SSE** |
| 약-음식 충돌 | - | - | - | - | ✅ | **Kafka + WebSocket** |
| 약사 채팅 | - | - | - | - | ✅ | **WebSocket/STOMP** |
| OCR 진행률 | - | - | - | - | ✅ | **SSE** |

---

### ✅ DB 트리거 사용 권장

**사용할 곳**:
1. ✅ 복약 기록 → 통계 자동 업데이트
2. ✅ 약 미복용 → 알림 레코드 자동 생성
3. ✅ 감사 로그 자동 기록

**사용하지 말 곳**:
- ❌ 복잡한 비즈니스 로직
- ❌ 외부 API 호출
- ❌ Kafka 이벤트 발행

---

### ⚠️ DB 커서 최소화

**대신 사용**:
- ✅ Set-based SQL (한 번에 여러 행 처리)
- ✅ Spring Batch (대용량 데이터 처리)

**커서 사용 최소 예시**:
- 월간 리포트 상세 계산 (행마다 복잡한 계산 필요 시)

---

### ✅ Spring Boot 스케줄러 권장

**@Scheduled 사용**:
```java
@Component
public class MedicationScheduler {

    @Autowired
    private MedicationService medicationService;

    @Autowired
    private NotificationService notificationService;

    // 매일 자정에 미복용 체크
    @Scheduled(cron = "0 0 0 * * *")
    public void checkMissedMedications() {
        medicationService.markMissedMedications();
        log.info("Missed medications check completed");
    }

    // 매주 월요일 오전 1시에 통계 계산
    @Scheduled(cron = "0 0 1 * * MON")
    public void calculateWeeklyStats() {
        statisticsService.calculateWeeklyAdherence();
        log.info("Weekly adherence calculation completed");
    }

    // 매일 오전 9시에 만료 알림
    @Scheduled(cron = "0 0 9 * * *")
    public void notifyExpiringMedications() {
        notificationService.notifyExpiringMedications();
        log.info("Expiry notifications sent");
    }

    // 매주 일요일 새벽 3시에 정리 작업
    @Scheduled(cron = "0 0 3 * * SUN")
    public void cleanupOldData() {
        notificationService.cleanupOldNotifications();
        log.info("Old data cleanup completed");
    }
}
```

**장점**:
- ✅ Java 코드로 작성 → 디버깅 쉬움
- ✅ 유닛 테스트 가능
- ✅ 로깅/모니터링 편리
- ✅ 분산 환경 지원 (ShedLock 사용 시)

---

### ✅ Spring Batch 대용량 처리

**사용 시나리오**:
- 수만 건 이상 데이터 처리
- 트랜잭션 관리 필요
- 재시작 가능성 (중간에 실패 시)

**예시: 월간 리포트 생성**
```java
@Configuration
public class ReportBatchConfig {

    @Bean
    public Job monthlyReportJob() {
        return jobBuilderFactory.get("monthlyReportJob")
            .start(generateReportStep())
            .build();
    }

    @Bean
    public Step generateReportStep() {
        return stepBuilderFactory.get("generateReportStep")
            .<MedicationSchedule, ReportDetail>chunk(1000)
            .reader(medicationScheduleReader())
            .processor(reportDetailProcessor())
            .writer(reportDetailWriter())
            .build();
    }
}
```

---

## 📌 결론

### 뭐냑? 프로젝트 DB 스킬 활용 전략

1. **트리거**: 통계 자동 갱신, 감사 로그만 사용
2. **커서**: 가급적 사용 안 함 (Set-based 쿼리로 대체)
3. **배치**: Spring @Scheduled로 구현 (DB Event보다 유연)
4. **실시간**: SSE + WebSocket/STOMP (+ Kafka 이벤트) 조합

**핵심 원칙**:
- ✅ 간단한 작업 → DB 트리거
- ✅ 주기 작업 → Spring @Scheduled
- ✅ 대용량 처리 → Spring Batch
- ✅ 실시간 알림/채팅 → SSE + WebSocket/STOMP
- ✅ (선택) 공동편집/CRDT → Hocuspocus + Y.js
- ✅ 이벤트 기반 → Kafka

---

**문서 작성자**: 뭐냑? 개발팀
**최종 수정일**: 2025-11-07
**관련 문서**:
- [ARCHITECTURE.md](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/ARCHITECTURE.md)
- [MICROSERVICES_SETUP.md](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/MICROSERVICES_SETUP.md)
- [PROJECT_SPECIFICATION.md](https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/.github/blob/dev/archive/documents/PROJECT_SPECIFICATION.md)
