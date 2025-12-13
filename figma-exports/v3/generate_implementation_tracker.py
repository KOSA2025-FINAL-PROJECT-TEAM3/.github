#!/usr/bin/env python3
"""
V3 Figma Export - Implementation Status Tracker Generator

이 스크립트는 Front 프로젝트의 실제 구현 상태를 반영하여
Feature별 구현 진행률을 추적하는 JSON 파일을 생성합니다.

v2와의 차이점:
- v2: Figma 디자인 시스템 정립 (Vision Pro 스타일 적용)
- v3: 실제 코드 구현 상태 추적 (Feature 기반)

작성일: 2025-11-18
기준: Front Repository v0.1.0 (45% 진행)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


# ============================================================================
# Feature 정의 및 구현 상태
# ============================================================================

FEATURES = {
    "auth": {
        "name": "인증 (Authentication)",
        "path": "src/features/auth",
        "progress": 100,
        "status": "completed",
        "files": [
            {"name": "Login.jsx", "status": "completed"},
            {"name": "Signup.jsx", "status": "completed"},
            {"name": "RoleSelection.jsx", "status": "completed"},
            {"name": "KakaoCallback.jsx", "status": "completed"},
            {"name": "KakaoLoginButton.jsx", "status": "completed"},
            {"name": "authStore.js", "status": "completed"},
            {"name": "useAuth.js", "status": "completed"},
        ],
        "figma_screens": ["01_카카오_로그인", "02_역할_선택"],
        "priority": "critical",
        "weight": 10,
    },
    "dashboard": {
        "name": "대시보드 (Dashboard)",
        "path": "src/features/dashboard",
        "progress": 40,
        "status": "in_progress",
        "files": [
            {"name": "Dashboard.jsx", "status": "in_progress"},
            {"name": "StatCard.jsx", "status": "in_progress"},
            {"name": "MedicationSummary.jsx", "status": "in_progress"},
            {"name": "SeniorDashboard.jsx", "status": "not_started"},
            {"name": "CaregiverDashboard.jsx", "status": "not_started"},
        ],
        "figma_screens": ["03_시니어_대시보드", "04_보호자_대시보드"],
        "priority": "critical",
        "weight": 10,
    },
    "medication": {
        "name": "약 관리 (Medication Management)",
        "path": "src/features/medication",
        "progress": 70,
        "status": "in_progress",
        "files": [
            {"name": "MedicationList.jsx", "status": "in_progress"},
            {"name": "MedicationForm.jsx", "status": "completed"},
            {"name": "MedicationDetail.jsx", "status": "in_progress"},
            {"name": "MedicationCard.jsx", "status": "completed"},
            {"name": "ScheduleCalendar.jsx", "status": "in_progress"},
            {"name": "IntakeCheckbox.jsx", "status": "completed"},
            {"name": "medicationStore.js", "status": "completed"},
            {"name": "useMedication.js", "status": "in_progress"},
        ],
        "figma_screens": [
            "05_약_관리",
            "06_약_등록",
            "17_약_리뷰_게시판",
            "18_약_상세_정보",
        ],
        "priority": "critical",
        "weight": 15,
    },
    "family": {
        "name": "가족 관리 (Family Management)",
        "path": "src/features/family",
        "progress": 60,
        "status": "in_progress",
        "files": [
            {"name": "FamilyManagement.jsx", "status": "in_progress"},
            {"name": "InviteMember.jsx", "status": "completed"},
            {"name": "FamilyMemberCard.jsx", "status": "completed"},
            {"name": "InvitationList.jsx", "status": "completed"},
            {"name": "MemberMedicationView.jsx", "status": "in_progress"},
            {"name": "familyStore.js", "status": "completed"},
            {"name": "FamilyContext.jsx", "status": "completed"},
            {"name": "familyService.js", "status": "completed"},
            {"name": "useFamily.js", "status": "completed"},
        ],
        "figma_screens": ["07_가족_관리"],
        "priority": "critical",
        "weight": 15,
    },
    "diet": {
        "name": "식단 관리 (Diet Management)",
        "path": "src/features/diet",
        "progress": 90,
        "status": "completed",
        "files": [
            {"name": "DietLog.jsx", "status": "completed"},
            {"name": "FoodInteractionWarning.jsx", "status": "completed"},
            {"name": "DietForm.jsx", "status": "completed"},
            {"name": "FoodCard.jsx", "status": "completed"},
            {"name": "InteractionBadge.jsx", "status": "completed"},
            {"name": "useDiet.js", "status": "completed"},
        ],
        "figma_screens": ["16_병원_식단_자료"],
        "priority": "high",
        "weight": 5,
    },
    "disease": {
        "name": "질병 관리 (Disease Management)",
        "path": "src/features/disease",
        "progress": 90,
        "status": "completed",
        "files": [
            {"name": "DiseaseManagement.jsx", "status": "completed"},
            {"name": "DiseaseDetail.jsx", "status": "in_progress"},
            {"name": "DiseaseCard.jsx", "status": "completed"},
            {"name": "useDisease.js", "status": "completed"},
        ],
        "figma_screens": ["14_내_질병_관리", "15_질병_제한사항_상세"],
        "priority": "high",
        "weight": 5,
    },
    "settings": {
        "name": "설정 (Settings)",
        "path": "src/features/settings",
        "progress": 90,
        "status": "completed",
        "files": [
            {"name": "Settings.jsx", "status": "completed"},
            {"name": "ProfileSettings.jsx", "status": "completed"},
            {"name": "NotificationSettings.jsx", "status": "completed"},
            {"name": "SettingsMenu.jsx", "status": "completed"},
            {"name": "ProfileForm.jsx", "status": "completed"},
            {"name": "NotificationToggle.jsx", "status": "completed"},
        ],
        "figma_screens": ["08_설정", "19_설정_내_약_관리", "20_설정_내_질병_관리"],
        "priority": "high",
        "weight": 5,
    },
    "notification": {
        "name": "알림 (Notification)",
        "path": "src/features/notification",
        "progress": 20,
        "status": "not_started",
        "files": [
            {"name": "NotificationList.jsx", "status": "in_progress"},
            {"name": "NotificationItem.jsx", "status": "not_started"},
        ],
        "figma_screens": [],
        "priority": "high",
        "weight": 5,
    },
    "ocr": {
        "name": "OCR (처방전 스캔)",
        "path": "src/features/ocr",
        "progress": 30,
        "status": "in_progress",
        "files": [
            {"name": "PrescriptionScan.jsx", "status": "in_progress"},
            {"name": "OCRResult.jsx", "status": "in_progress"},
            {"name": "ImageUploader.jsx", "status": "in_progress"},
            {"name": "OCRPreview.jsx", "status": "not_started"},
            {"name": "ManualCorrection.jsx", "status": "not_started"},
        ],
        "figma_screens": ["06_약_등록"],
        "priority": "high",
        "weight": 10,
    },
    "chat": {
        "name": "채팅 (Pharmacist Chat)",
        "path": "src/features/chat",
        "progress": 10,
        "status": "not_started",
        "files": [
            {"name": "ChatRoom.jsx", "status": "not_started"},
            {"name": "MessageList.jsx", "status": "not_started"},
            {"name": "MessageInput.jsx", "status": "not_started"},
            {"name": "ChatBubble.jsx", "status": "not_started"},
        ],
        "figma_screens": ["09_약사_채팅_목록", "10_약사_1대1_대화"],
        "priority": "medium",
        "weight": 5,
    },
    "search": {
        "name": "검색 (Search)",
        "path": "src/features/search",
        "progress": 10,
        "status": "not_started",
        "files": [
            {"name": "PillSearch.jsx", "status": "not_started"},
            {"name": "SymptomSearch.jsx", "status": "not_started"},
        ],
        "figma_screens": ["11_증상_검색", "12_의심_질환_결과"],
        "priority": "medium",
        "weight": 3,
    },
    "report": {
        "name": "리포트 (Compliance Report)",
        "path": "src/features/report",
        "progress": 10,
        "status": "not_started",
        "files": [
            {"name": "ComplianceReport.jsx", "status": "not_started"},
        ],
        "figma_screens": ["21_복약_순응도_리포트"],
        "priority": "medium",
        "weight": 3,
    },
    "counsel": {
        "name": "약국 상담 (Counsel)",
        "path": "src/features/counsel",
        "progress": 5,
        "status": "not_started",
        "files": [
            {"name": "CounselRecommendation.jsx", "status": "not_started"},
        ],
        "figma_screens": ["13_약국_상담_추천"],
        "priority": "low",
        "weight": 2,
    },
}


# ============================================================================
# 유틸리티 함수
# ============================================================================


def calculate_overall_progress(features: Dict) -> int:
    """전체 진행률 계산 (가중치 기반)"""
    total_weight = sum(f["weight"] for f in features.values())
    weighted_sum = sum(f["progress"] * f["weight"] for f in features.values())
    return round(weighted_sum / total_weight)


def get_status_emoji(status: str) -> str:
    """상태별 이모지 반환"""
    emoji_map = {
        "completed": "✅",
        "in_progress": "🔄",
        "not_started": "❌",
    }
    return emoji_map.get(status, "❓")


def get_priority_emoji(priority: str) -> str:
    """우선순위별 이모지 반환"""
    emoji_map = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
    }
    return emoji_map.get(priority, "⚪")


def count_files_by_status(features: Dict) -> Dict[str, int]:
    """상태별 파일 개수 집계"""
    counts = {"completed": 0, "in_progress": 0, "not_started": 0}
    for feature in features.values():
        for file in feature["files"]:
            status = file["status"]
            counts[status] = counts.get(status, 0) + 1
    return counts


def generate_feature_summary(feature_id: str, feature: Dict) -> Dict:
    """Feature별 요약 정보 생성"""
    total_files = len(feature["files"])
    completed_files = sum(
        1 for f in feature["files"] if f["status"] == "completed"
    )
    in_progress_files = sum(
        1 for f in feature["files"] if f["status"] == "in_progress"
    )

    return {
        "id": feature_id,
        "name": feature["name"],
        "path": feature["path"],
        "progress": feature["progress"],
        "status": feature["status"],
        "status_emoji": get_status_emoji(feature["status"]),
        "priority": feature["priority"],
        "priority_emoji": get_priority_emoji(feature["priority"]),
        "weight": feature["weight"],
        "total_files": total_files,
        "completed_files": completed_files,
        "in_progress_files": in_progress_files,
        "not_started_files": total_files - completed_files - in_progress_files,
        "figma_screens": feature["figma_screens"],
        "files": feature["files"],
    }


# ============================================================================
# JSON 생성 함수
# ============================================================================


def generate_implementation_status_json(output_path: str):
    """구현 상태 추적 JSON 생성"""
    # 전체 진행률 계산
    overall_progress = calculate_overall_progress(FEATURES)

    # Feature별 요약 생성
    feature_summaries = [
        generate_feature_summary(feature_id, feature)
        for feature_id, feature in FEATURES.items()
    ]

    # 파일 상태 집계
    file_counts = count_files_by_status(FEATURES)
    total_files = sum(file_counts.values())

    # 최종 JSON 구조
    output = {
        "version": "3.0.0",
        "generated_at": datetime.now().isoformat(),
        "repository": "KOSA2025-FINAL-PROJECT-TEAM3/Front",
        "branch": "dev",
        "base_version": "v0.1.0",
        "summary": {
            "overall_progress": overall_progress,
            "total_features": len(FEATURES),
            "total_files": total_files,
            "completed_files": file_counts["completed"],
            "in_progress_files": file_counts["in_progress"],
            "not_started_files": file_counts["not_started"],
            "features_by_status": {
                "completed": sum(
                    1 for f in FEATURES.values() if f["status"] == "completed"
                ),
                "in_progress": sum(
                    1 for f in FEATURES.values() if f["status"] == "in_progress"
                ),
                "not_started": sum(
                    1 for f in FEATURES.values() if f["status"] == "not_started"
                ),
            },
        },
        "features": feature_summaries,
        "priority_groups": {
            "critical": [
                f["id"]
                for f in feature_summaries
                if f["priority"] == "critical"
            ],
            "high": [
                f["id"] for f in feature_summaries if f["priority"] == "high"
            ],
            "medium": [
                f["id"] for f in feature_summaries if f["priority"] == "medium"
            ],
            "low": [
                f["id"] for f in feature_summaries if f["priority"] == "low"
            ],
        },
        "next_actions": {
            "week_4_critical": [
                "Dashboard - SeniorDashboard.jsx 구현",
                "Dashboard - CaregiverDashboard.jsx 구현",
                "Medication - MedicationList.jsx 완성",
                "Family - FamilyManagement.jsx 완성",
            ],
            "week_5_high": [
                "Notification - NotificationList.jsx 완성",
                "OCR - Google Vision API 연동",
                "Chat - 기본 채팅 UI 구현",
            ],
            "week_6_medium": [
                "Search - 알약/증상 검색 UI",
                "Report - 복약 순응도 차트",
            ],
        },
    }

    # JSON 파일 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return output


# ============================================================================
# 메인 실행
# ============================================================================


def main():
    """메인 실행 함수"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "implementation-status.json")

    print("=" * 80)
    print("V3 Figma Export - Implementation Status Tracker Generator")
    print("=" * 80)
    print()

    # JSON 생성
    print(f"📝 구현 상태 추적 JSON 생성 중...")
    result = generate_implementation_status_json(output_path)

    # 결과 출력
    print(f"✅ JSON 파일 생성 완료: {output_path}")
    print()
    print("=" * 80)
    print("📊 구현 현황 요약")
    print("=" * 80)
    print(f"전체 진행률: {result['summary']['overall_progress']}%")
    print(f"총 Feature 수: {result['summary']['total_features']}개")
    print(f"총 파일 수: {result['summary']['total_files']}개")
    print()
    print(f"✅ 완료: {result['summary']['completed_files']}개")
    print(f"🔄 진행 중: {result['summary']['in_progress_files']}개")
    print(f"❌ 미착수: {result['summary']['not_started_files']}개")
    print()
    print("=" * 80)
    print("🎯 Feature별 현황")
    print("=" * 80)

    for feature in result["features"]:
        status_emoji = feature["status_emoji"]
        priority_emoji = feature["priority_emoji"]
        print(
            f"{status_emoji} {priority_emoji} [{feature['progress']:3d}%] "
            f"{feature['name']:<30} ({feature['completed_files']}/{feature['total_files']} 파일)"
        )

    print()
    print("=" * 80)
    print("✨ Phase 2 완료!")
    print("=" * 80)


if __name__ == "__main__":
    main()
