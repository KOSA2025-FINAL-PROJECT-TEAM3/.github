-- MySQL Workbench Forward Engineering
-- Corrected Schema for AMApill Database
--
-- Fixes Applied:
-- 1. Added AUTO_INCREMENT to diseases.id
-- 2. Added AUTO_INCREMENT to chat_messages.id and changed INT to BIGINT
-- 3. Fixed chat_messages.context → content
-- 4. Fixed day_of_week UNIQUE INDEX issue
-- 5. Added AUTO_INCREMENT to day_of_week.id
-- 6. Changed notifications.medication_schedules_id to allow NULL
-- 7. Simplified diet_warnings PRIMARY KEY
--
-- Date: 2025-11-18
-- Version: 1.1 (Corrected)

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema amapill
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `amapill` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `amapill` ;

-- -----------------------------------------------------
-- Table `amapill`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`users` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20) NULL DEFAULT NULL,
  `kakao_id` VARCHAR(100) NULL DEFAULT NULL,
  `password_hash` VARCHAR(255) NULL DEFAULT NULL,
  `is_active` TINYINT(1) NULL DEFAULT '1',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `phone` (`phone` ASC) VISIBLE,
  UNIQUE INDEX `kakao_id` (`kakao_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '사용자 계정 정보 - KakaoLoginPage, ProfilePage';


-- -----------------------------------------------------
-- Table `amapill`.`adherence_reports`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`adherence_reports` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `start_date` DATE NULL DEFAULT NULL,
  `end_date` DATE NULL DEFAULT NULL,
  `overall_adherence` DECIMAL(5,2) NULL DEFAULT NULL,
  `report_data` JSON NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `adherence_reports_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'AdherenceReportResponse';


-- -----------------------------------------------------
-- Table `amapill`.`audit_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`audit_logs` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `action` VARCHAR(100) NULL DEFAULT NULL,
  `entity_type` VARCHAR(100) NULL DEFAULT NULL,
  `ip_address` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `idx_created_at` (`created_at` ASC) VISIBLE,
  CONSTRAINT `audit_logs_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'GDPR 대응용 감사 로그';


-- -----------------------------------------------------
-- Table `amapill`.`chat_rooms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`chat_rooms` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(20) NULL DEFAULT 'consultation',
  `status` VARCHAR(20) NULL DEFAULT 'active',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_type_status` (`type` ASC, `status` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'AI/의사 상담 또는 가족 채팅방';


-- -----------------------------------------------------
-- Table `amapill`.`family_groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`family_groups` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `invite_code` VARCHAR(20) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `invite_code` (`invite_code` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'FamilyGroupRequest / FamilyGroupResponse';


-- -----------------------------------------------------
-- Table `amapill`.`family_members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`family_members` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `family_group_id` BIGINT NULL DEFAULT NULL,
  `user_id` BIGINT NULL DEFAULT NULL,
  `family_role` ENUM('CAREGIVER', 'SENIOR') NOT NULL,
  `joined_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `family_group_id` (`family_group_id` ASC) VISIBLE,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `family_members_ibfk_1`
    FOREIGN KEY (`family_group_id`)
    REFERENCES `amapill`.`family_groups` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `family_members_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'FamilyMemberInviteRequest / FamilyGroupResponse.members';


-- -----------------------------------------------------
-- Table `amapill`.`chat_room_members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`chat_room_members` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `room_id` BIGINT NULL DEFAULT NULL,
  `family_member_id` BIGINT NULL DEFAULT NULL,
  `joined_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `room_id` (`room_id` ASC) VISIBLE,
  INDEX `family_member_id` (`family_member_id` ASC) VISIBLE,
  CONSTRAINT `chat_room_members_ibfk_1`
    FOREIGN KEY (`room_id`)
    REFERENCES `amapill`.`chat_rooms` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `chat_room_members_ibfk_2`
    FOREIGN KEY (`family_member_id`)
    REFERENCES `amapill`.`family_members` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '가족 채팅방 참여자 목록';


-- -----------------------------------------------------
-- Table `amapill`.`medications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`medications` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '복용 약물 번호',
  `name` VARCHAR(255) NOT NULL,
  `ingredient` VARCHAR(255) NULL DEFAULT NULL,
  `dosage` VARCHAR(100) NULL DEFAULT NULL,
  `timing` VARCHAR(100) NULL DEFAULT NULL,
  `start_date` DATE NULL DEFAULT NULL,
  `end_date` DATE NULL DEFAULT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `remaining` INT NULL DEFAULT NULL,
  `expiry_date` DATE NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `users_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_medications_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `idx_expiry_date` (`expiry_date` ASC) VISIBLE,
  CONSTRAINT `fk_medications_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'MedicationRequest / MedicationResponse (복용 약물 정보)';


-- -----------------------------------------------------
-- Table `amapill`.`medication_schedules`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`medication_schedules` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `medication_id` BIGINT NULL DEFAULT NULL,
  `time` TIME NOT NULL,
  `days_of_week` VARCHAR(50) NULL DEFAULT NULL,
  `active` TINYINT(1) NULL DEFAULT '1',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `medication_id` (`medication_id` ASC) VISIBLE,
  CONSTRAINT `medication_schedules_ibfk_1`
    FOREIGN KEY (`medication_id`)
    REFERENCES `amapill`.`medications` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'MedicationScheduleRequest / MedicationResponse.schedules';


-- -----------------------------------------------------
-- Table `amapill`.`day_of_week`
-- -----------------------------------------------------
-- NOTE: This table is optional. You can use medication_schedules.days_of_week VARCHAR instead.
-- If using this table, ensure the UNIQUE constraint allows multiple schedules for the same day.
CREATE TABLE IF NOT EXISTS `amapill`.`day_of_week` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `day_of_week` TINYINT(1) NULL DEFAULT NULL COMMENT '1=monday 7=sunday',
  `medication_schedules_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  -- FIXED: Changed from UNIQUE(day_of_week) to composite UNIQUE
  UNIQUE INDEX `uk_schedule_day` (`medication_schedules_id` ASC, `day_of_week` ASC) VISIBLE,
  INDEX `fk_day_of_week_medication_schedules1_idx` (`medication_schedules_id` ASC) VISIBLE,
  CONSTRAINT `fk_day_of_week_medication_schedules1`
    FOREIGN KEY (`medication_schedules_id`)
    REFERENCES `amapill`.`medication_schedules` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '복약 스케줄별 요일 정보 (선택적 사용)';


-- -----------------------------------------------------
-- Table `amapill`.`diet_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`diet_logs` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `meal_type` VARCHAR(20) NULL DEFAULT NULL,
  `food_name` VARCHAR(255) NULL DEFAULT NULL,
  `recorded_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `idx_recorded_at` (`recorded_at` ASC) VISIBLE,
  CONSTRAINT `diet_logs_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'DietLogRequest / DietLogResponse';


-- -----------------------------------------------------
-- Table `amapill`.`diseases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`diseases` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,  -- FIXED: Added AUTO_INCREMENT
  `name` VARCHAR(255) NOT NULL,
  `users_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_diseases_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_diseases_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '사용자별 질병 정보';


-- -----------------------------------------------------
-- Table `amapill`.`diet_warnings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`diet_warnings` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `diet_log_id` BIGINT NULL DEFAULT NULL,
  `medication_id` BIGINT NULL DEFAULT NULL,
  `diseases_id` BIGINT NULL DEFAULT NULL,  -- OPTIONAL: Changed to allow NULL
  `severity` VARCHAR(20) NULL DEFAULT NULL,
  `warning_message` TEXT NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),  -- FIXED: Simplified from composite PK (id, diseases_id) to just (id)
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `diet_log_id` (`diet_log_id` ASC) VISIBLE,
  INDEX `medication_id` (`medication_id` ASC) VISIBLE,
  INDEX `fk_diet_warnings_diseases1_idx` (`diseases_id` ASC) VISIBLE,
  INDEX `idx_severity` (`severity` ASC) VISIBLE,
  CONSTRAINT `diet_warnings_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `diet_warnings_ibfk_2`
    FOREIGN KEY (`diet_log_id`)
    REFERENCES `amapill`.`diet_logs` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `diet_warnings_ibfk_3`
    FOREIGN KEY (`medication_id`)
    REFERENCES `amapill`.`medications` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_diet_warnings_diseases1`
    FOREIGN KEY (`diseases_id`)
    REFERENCES `amapill`.`diseases` (`id`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'DietWarningResponse';


-- -----------------------------------------------------
-- Table `amapill`.`notifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`notifications` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `type` VARCHAR(50) NULL DEFAULT NULL,
  `title` VARCHAR(255) NULL DEFAULT NULL,
  `message` TEXT NULL DEFAULT NULL,
  `is_read` TINYINT(1) NULL DEFAULT '0',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `medication_schedules_id` BIGINT NULL DEFAULT NULL,  -- FIXED: Changed to allow NULL for non-medication notifications
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `fk_notifications_medication_schedules1_idx` (`medication_schedules_id` ASC) VISIBLE,
  INDEX `idx_type_is_read` (`type` ASC, `is_read` ASC) VISIBLE,
  CONSTRAINT `fk_notifications_medication_schedules1`
    FOREIGN KEY (`medication_schedules_id`)
    REFERENCES `amapill`.`medication_schedules` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `notifications_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'NotificationResponse';


-- -----------------------------------------------------
-- Table `amapill`.`family_notifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`family_notifications` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `notification_id` BIGINT NULL DEFAULT NULL,
  `family_member_id` BIGINT NULL DEFAULT NULL,
  `is_acknowledged` TINYINT(1) NULL DEFAULT '0',
  `read_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `notification_id` (`notification_id` ASC) VISIBLE,
  INDEX `family_member_id` (`family_member_id` ASC) VISIBLE,
  CONSTRAINT `family_notifications_ibfk_1`
    FOREIGN KEY (`notification_id`)
    REFERENCES `amapill`.`notifications` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `family_notifications_ibfk_2`
    FOREIGN KEY (`family_member_id`)
    REFERENCES `amapill`.`family_members` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '가족 구성원별 알림 수신 상태 관리';


-- -----------------------------------------------------
-- Table `amapill`.`medication_logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`medication_logs` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `scheduled_time` TIMESTAMP NULL DEFAULT NULL,
  `completed_time` TIMESTAMP NULL DEFAULT NULL,
  `completed` TINYINT(1) NULL DEFAULT '0',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `medication_schedules_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_medication_logs_medication_schedules1_idx` (`medication_schedules_id` ASC) VISIBLE,
  INDEX `idx_scheduled_time` (`scheduled_time` ASC) VISIBLE,
  INDEX `idx_completed` (`completed` ASC) VISIBLE,
  CONSTRAINT `fk_medication_logs_medication_schedules1`
    FOREIGN KEY (`medication_schedules_id`)
    REFERENCES `amapill`.`medication_schedules` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'MedicationLogRequest / MedicationLogResponse / TodayMedicationResponse';


-- -----------------------------------------------------
-- Table `amapill`.`oauth_providers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`oauth_providers` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `provider` VARCHAR(50) NOT NULL,
  `provider_user_id` VARCHAR(255) NOT NULL,
  `access_token` TEXT NULL DEFAULT NULL,
  `refresh_token` TEXT NULL DEFAULT NULL,
  `expires_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `uk_provider_user` (`provider` ASC, `provider_user_id` ASC) VISIBLE,
  CONSTRAINT `oauth_providers_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'OAuth 계정 매핑 - Kakao, Google 등';


-- -----------------------------------------------------
-- Table `amapill`.`refresh_tokens`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`refresh_tokens` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NULL DEFAULT NULL,
  `token_hash` VARCHAR(255) NOT NULL,
  `device_id` VARCHAR(255) NULL DEFAULT NULL,
  `ip_address` VARCHAR(45) NULL DEFAULT NULL,
  `expires_at` TIMESTAMP NULL DEFAULT NULL,
  `revoked_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `token_hash` (`token_hash` ASC) VISIBLE,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `idx_expires_at` (`expires_at` ASC) VISIBLE,
  CONSTRAINT `refresh_tokens_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'JWT Refresh Token 관리';


-- -----------------------------------------------------
-- Table `amapill`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`roles` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '시스템 역할 정의';


-- -----------------------------------------------------
-- Table `amapill`.`user_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`user_roles` (
  `user_id` BIGINT NULL DEFAULT NULL,
  `role_id` BIGINT NULL DEFAULT NULL,
  `assigned_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX `user_roles_index_0` (`user_id` ASC, `role_id` ASC) VISIBLE,
  INDEX `role_id` (`role_id` ASC) VISIBLE,
  CONSTRAINT `user_roles_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `amapill`.`users` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `user_roles_ibfk_2`
    FOREIGN KEY (`role_id`)
    REFERENCES `amapill`.`roles` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '사용자 ↔ 역할 매핑 테이블 (N:M)';


-- -----------------------------------------------------
-- Table `amapill`.`chat_messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `amapill`.`chat_messages` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,  -- FIXED: Changed from INT to BIGINT and added AUTO_INCREMENT
  `sender_type` VARCHAR(45) NULL DEFAULT NULL,
  `content` TEXT NULL DEFAULT NULL,  -- FIXED: Changed from 'context' to 'content'
  `message_type` VARCHAR(45) NULL DEFAULT NULL,
  `ai_model` VARCHAR(100) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `chat_rooms_id` BIGINT NOT NULL,
  `chat_room_members_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_chat_messages_chat_rooms1_idx` (`chat_rooms_id` ASC) VISIBLE,
  INDEX `fk_chat_messages_chat_room_members1_idx` (`chat_room_members_id` ASC) VISIBLE,
  INDEX `idx_created_at` (`created_at` ASC) VISIBLE,
  CONSTRAINT `fk_chat_messages_chat_rooms1`
    FOREIGN KEY (`chat_rooms_id`)
    REFERENCES `amapill`.`chat_rooms` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_chat_messages_chat_room_members1`
    FOREIGN KEY (`chat_room_members_id`)
    REFERENCES `amapill`.`chat_room_members` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '채팅 메시지 저장';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
