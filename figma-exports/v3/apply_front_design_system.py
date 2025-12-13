#!/usr/bin/env python3
"""
V3 Figma Export - Front Design System Applier

이 스크립트는 Figma JSON 파일에 Front 프로젝트의 디자인 시스템을 적용합니다.

v2와의 차이점:
- v2: Vision Pro 스타일 (블러, 그라데이션, 그림자)
- v3: Front 프로젝트 디자인 시스템 (Tailwind CSS 기반, 실제 구현된 색상)

작성일: 2025-11-18
기준: Front Repository v0.1.0 디자인 시스템
"""

import json
import os
import sys
from typing import Dict, List, Optional


# ============================================================================
# Front 프로젝트 디자인 시스템 (component-templates.json 기준)
# ============================================================================

DESIGN_SYSTEM = {
    "colors": {
        # Primary Colors
        "primary": {"r": 0.145, "g": 0.388, "b": 0.922},  # #2563eb (indigo-600)
        "success": {"r": 0.133, "g": 0.773, "b": 0.369},  # #22c55e (green-500)
        "danger": {"r": 0.937, "g": 0.267, "b": 0.267},   # #ef4444 (red-500)
        "warning": {"r": 0.976, "g": 0.451, "b": 0.086},  # #f97316 (orange-500)

        # Role-specific Colors
        "caregiver": {"r": 0.647, "g": 0.706, "b": 0.988},  # #a5b4fc (indigo-300)
        "senior": {"r": 0.976, "g": 0.659, "b": 0.831},     # #f9a8d4 (pink-300)

        # OCR Feature Colors
        "ocr_background": {"r": 0.059, "g": 0.090, "b": 0.161},  # #0f172a (slate-900)
        "ocr_accent": {"r": 0.133, "g": 0.827, "b": 0.910},      # #22d3ee (cyan-400)

        # Text Colors
        "text_primary": {"r": 0.122, "g": 0.161, "b": 0.212},    # #1f2937 (gray-900)
        "text_secondary": {"r": 0.420, "g": 0.447, "b": 0.502},  # #6b7280 (gray-500)

        # UI Colors
        "border": {"r": 0.898, "g": 0.906, "b": 0.922},     # #e5e7eb (gray-200)
        "background": {"r": 0.976, "g": 0.980, "b": 0.984},  # #f9fafb (gray-50)
        "white": {"r": 1, "g": 1, "b": 1},
    },
    "spacing": {
        "xs": 4,   # 0.25rem
        "sm": 8,   # 0.5rem
        "md": 16,  # 1rem
        "lg": 24,  # 1.5rem
        "xl": 32,  # 2rem
        "2xl": 48, # 3rem
    },
    "border_radius": {
        "card": 12,    # 0.75rem
        "button": 8,   # 0.5rem
        "input": 8,    # 0.5rem
        "modal": 16,   # 1rem
    },
    "shadows": {
        "sm": {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0, "b": 0, "a": 0.05},
            "offset": {"x": 0, "y": 1},
            "radius": 2,
        },
        "md": {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0, "b": 0, "a": 0.08},
            "offset": {"x": 0, "y": 4},
            "radius": 12,
        },
        "lg": {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0, "b": 0, "a": 0.1},
            "offset": {"x": 0, "y": 8},
            "radius": 25,
        },
    },
}


# ============================================================================
# 유틸리티 함수
# ============================================================================

def has_keyword(name: str, keywords: List[str]) -> bool:
    """Check if any keyword is in the frame name (case-insensitive)"""
    name_lower = name.lower()
    return any(keyword.lower() in name_lower for keyword in keywords)


def get_color_type(color: Dict) -> Optional[str]:
    """Determine the color type based on RGB values"""
    r, g, b = color.get("r", 0), color.get("g", 0), color.get("b", 0)

    # Primary Blue (old: 0, 0.48, 1)
    if b > 0.8 and r < 0.2 and g < 0.6:
        return "primary"

    # Success Green (old: 0.3, 0.69, 0.31)
    if g > 0.6 and r < 0.4 and b < 0.4:
        return "success"

    # Danger Red (old: 0.96, 0.26, 0.21)
    if r > 0.8 and g < 0.4 and b < 0.4:
        return "danger"

    # Warning Orange (old: 1, 0.6, 0)
    if r > 0.9 and g > 0.4 and b < 0.2:
        return "warning"

    return None


def is_white_or_light(fills: List[Dict]) -> bool:
    """Check if the fill is white or very light"""
    if not fills or len(fills) == 0:
        return False
    fill = fills[0]
    if fill.get("type") != "SOLID":
        return False
    color = fill.get("color", {})
    return (color.get("r", 0) >= 0.9 and
            color.get("g", 0) >= 0.9 and
            color.get("b", 0) >= 0.9)


# ============================================================================
# 스타일 적용 함수
# ============================================================================

def apply_header_style(frame: Dict, stats: Dict) -> bool:
    """Apply Front design system to Header frames"""
    # Header는 흰색 배경 + 하단 border
    frame["fills"] = [
        {
            "type": "SOLID",
            "color": {**DESIGN_SYSTEM["colors"]["white"], "a": 1}
        }
    ]

    # 하단 border shadow
    frame["effects"] = [
        {
            "type": "DROP_SHADOW",
            "color": DESIGN_SYSTEM["shadows"]["sm"]["color"],
            "offset": DESIGN_SYSTEM["shadows"]["sm"]["offset"],
            "radius": DESIGN_SYSTEM["shadows"]["sm"]["radius"],
            "visible": True
        }
    ]

    stats["headers"] += 1
    return True


def apply_card_style(frame: Dict, stats: Dict) -> bool:
    """Apply Front design system to Card/Container frames"""
    # Card border radius
    frame["cornerRadius"] = DESIGN_SYSTEM["border_radius"]["card"]

    # 흰색 배경
    if "fills" in frame and is_white_or_light(frame["fills"]):
        frame["fills"] = [
            {
                "type": "SOLID",
                "color": {**DESIGN_SYSTEM["colors"]["white"], "a": 1}
            }
        ]

    # Medium shadow for cards
    frame["effects"] = [
        {
            "type": "DROP_SHADOW",
            "color": DESIGN_SYSTEM["shadows"]["md"]["color"],
            "offset": DESIGN_SYSTEM["shadows"]["md"]["offset"],
            "radius": DESIGN_SYSTEM["shadows"]["md"]["radius"],
            "visible": True
        }
    ]

    stats["cards"] += 1
    return True


def apply_button_style(frame: Dict, stats: Dict) -> bool:
    """Apply Front design system to Button frames"""
    # Button border radius
    frame["cornerRadius"] = DESIGN_SYSTEM["border_radius"]["button"]

    # 버튼 색상 업데이트
    if "fills" in frame and len(frame["fills"]) > 0:
        fill = frame["fills"][0]
        if fill.get("type") == "SOLID":
            color_type = get_color_type(fill.get("color", {}))
            if color_type:
                # Front 디자인 시스템 색상으로 변경
                frame["fills"] = [
                    {
                        "type": "SOLID",
                        "color": {**DESIGN_SYSTEM["colors"][color_type], "a": 1}
                    }
                ]

    # Button shadow
    frame["effects"] = [
        {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0, "b": 0, "a": 0.1},
            "offset": {"x": 0, "y": 2},
            "radius": 8,
            "visible": True
        }
    ]

    stats["buttons"] += 1
    return True


def apply_input_style(frame: Dict, stats: Dict) -> bool:
    """Apply Front design system to Input/Search frames"""
    # Input border radius
    frame["cornerRadius"] = DESIGN_SYSTEM["border_radius"]["input"]

    # 흰색 배경
    frame["fills"] = [
        {
            "type": "SOLID",
            "color": {**DESIGN_SYSTEM["colors"]["white"], "a": 1}
        }
    ]

    # Border 스타일 (stroke)
    if "strokes" not in frame:
        frame["strokes"] = []

    frame["strokes"] = [
        {
            "type": "SOLID",
            "color": {**DESIGN_SYSTEM["colors"]["border"], "a": 1}
        }
    ]
    frame["strokeWeight"] = 1

    # Small shadow
    frame["effects"] = [
        {
            "type": "DROP_SHADOW",
            "color": DESIGN_SYSTEM["shadows"]["sm"]["color"],
            "offset": DESIGN_SYSTEM["shadows"]["sm"]["offset"],
            "radius": DESIGN_SYSTEM["shadows"]["sm"]["radius"],
            "visible": True
        }
    ]

    stats["inputs"] += 1
    return True


def apply_text_color(frame: Dict, stats: Dict) -> bool:
    """Apply Front design system text colors"""
    if "fills" not in frame or len(frame["fills"]) == 0:
        return False

    fill = frame["fills"][0]
    if fill.get("type") != "SOLID":
        return False

    # 텍스트가 회색 계열이면 text_secondary, 검정 계열이면 text_primary
    color = fill.get("color", {})
    r, g, b = color.get("r", 0), color.get("g", 0), color.get("b", 0)

    # 회색 계열 (0.4 ~ 0.6)
    if 0.3 < r < 0.7 and 0.3 < g < 0.7 and 0.3 < b < 0.7:
        frame["fills"] = [
            {
                "type": "SOLID",
                "color": {**DESIGN_SYSTEM["colors"]["text_secondary"], "a": 1}
            }
        ]
        stats["texts_secondary"] += 1
        return True

    # 검정 계열 (< 0.3)
    if r < 0.4 and g < 0.4 and b < 0.4:
        frame["fills"] = [
            {
                "type": "SOLID",
                "color": {**DESIGN_SYSTEM["colors"]["text_primary"], "a": 1}
            }
        ]
        stats["texts_primary"] += 1
        return True

    return False


def apply_role_specific_colors(frame: Dict, stats: Dict) -> bool:
    """Apply role-specific colors (Caregiver/Senior)"""
    frame_name = frame.get("name", "")

    if has_keyword(frame_name, ["Caregiver", "보호자"]):
        if "fills" in frame:
            frame["fills"] = [
                {
                    "type": "SOLID",
                    "color": {**DESIGN_SYSTEM["colors"]["caregiver"], "a": 0.2}
                }
            ]
            stats["caregiver_elements"] += 1
            return True

    if has_keyword(frame_name, ["Senior", "시니어", "노인"]):
        if "fills" in frame:
            frame["fills"] = [
                {
                    "type": "SOLID",
                    "color": {**DESIGN_SYSTEM["colors"]["senior"], "a": 0.2}
                }
            ]
            stats["senior_elements"] += 1
            return True

    return False


def apply_front_design_system(frame: Dict, stats: Dict):
    """Recursively apply Front design system to frames"""
    if not isinstance(frame, dict):
        return

    frame_name = frame.get("name", "")
    frame_type = frame.get("type", "")

    # 1. Header 스타일
    if frame_name == "Header" or has_keyword(frame_name, ["Header", "헤더"]):
        apply_header_style(frame, stats)

    # 2. Card 스타일
    elif has_keyword(frame_name, ["Card", "Container", "Item", "카드"]):
        apply_card_style(frame, stats)

    # 3. Button 스타일
    elif has_keyword(frame_name, ["Button", "Btn", "버튼"]):
        apply_button_style(frame, stats)

    # 4. Input/Search 스타일
    elif has_keyword(frame_name, ["Input", "Search", "TextField", "입력"]):
        apply_input_style(frame, stats)

    # 5. Role-specific colors
    elif apply_role_specific_colors(frame, stats):
        pass

    # 6. Text 색상 (TEXT 타입인 경우)
    elif frame_type == "TEXT":
        apply_text_color(frame, stats)

    # Recursively process children
    if "children" in frame:
        for child in frame["children"]:
            apply_front_design_system(child, stats)


# ============================================================================
# 메인 실행
# ============================================================================

def main():
    """메인 실행 함수"""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Input/Output 파일 경로
    input_file = os.path.join(script_dir, "..", "v2", "silvercare-part1-auth-dashboard.json")
    output_dir = os.path.join(script_dir, "output")

    # 명령줄 인자로 파일 지정 가능
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    if len(sys.argv) > 2:
        output_dir = sys.argv[2]

    # Output 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 80)
    print("V3 Figma Export - Front Design System Applier")
    print("=" * 80)
    print()

    # 파일 존재 확인
    if not os.path.exists(input_file):
        print(f"❌ Error: 입력 파일을 찾을 수 없습니다: {input_file}")
        print()
        print("사용법:")
        print(f"  python3 {os.path.basename(__file__)} [input_file] [output_dir]")
        print()
        print("예시:")
        print(f"  python3 {os.path.basename(__file__)} ../v2/silvercare-part1-auth-dashboard.json ./output")
        sys.exit(1)

    # Load the JSON file
    print(f"📂 입력 파일: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Statistics
    stats = {
        "headers": 0,
        "cards": 0,
        "buttons": 0,
        "inputs": 0,
        "texts_primary": 0,
        "texts_secondary": 0,
        "caregiver_elements": 0,
        "senior_elements": 0,
    }

    # Process all screens
    screens_count = len(data.get("screens", []))
    print(f"📊 화면 수: {screens_count}개")
    print()
    print("🎨 Front 디자인 시스템 적용 중...")
    print()

    for screen in data.get("screens", []):
        apply_front_design_system(screen, stats)

    # Save the modified JSON
    output_file = os.path.join(
        output_dir,
        os.path.basename(input_file).replace(".json", "-front-v3.json")
    )

    print(f"💾 출력 파일: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print statistics
    print()
    print("=" * 80)
    print("✅ Front Design System 적용 완료!")
    print("=" * 80)
    print()
    print(f"📊 처리 결과:")
    print(f"  • 화면 수: {screens_count}개")
    print(f"  • Headers: {stats['headers']}개")
    print(f"  • Cards/Containers: {stats['cards']}개")
    print(f"  • Buttons: {stats['buttons']}개")
    print(f"  • Inputs/Search: {stats['inputs']}개")
    print(f"  • Text (Primary): {stats['texts_primary']}개")
    print(f"  • Text (Secondary): {stats['texts_secondary']}개")
    print(f"  • Caregiver 요소: {stats['caregiver_elements']}개")
    print(f"  • Senior 요소: {stats['senior_elements']}개")
    print()
    print(f"📁 총 스타일 적용: {sum(stats.values())}개 요소")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
