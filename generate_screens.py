#!/usr/bin/env python3
import json

# Color palette
COLORS = {
    "green": {"r": 0.3, "g": 0.69, "b": 0.31},
    "blue": {"r": 0.13, "g": 0.59, "b": 0.95},
    "red": {"r": 0.96, "g": 0.26, "b": 0.21},
    "orange": {"r": 1, "g": 0.6, "b": 0},
    "yellow": {"r": 1, "g": 0.9, "b": 0},
    "gray_bg": {"r": 0.98, "g": 0.98, "b": 0.98},
    "white": {"r": 1, "g": 1, "b": 1},
    "dark": {"r": 0.13, "g": 0.13, "b": 0.13},
    "gray": {"r": 0.5, "g": 0.5, "b": 0.5},
    "light_gray": {"r": 0.7, "g": 0.7, "b": 0.7},
    "border_gray": {"r": 0.88, "g": 0.88, "b": 0.88}
}

def create_shadow():
    return {
        "type": "DROP_SHADOW",
        "color": {"r": 0, "g": 0, "b": 0, "a": 0.08},
        "offset": {"x": 0, "y": 4},
        "radius": 12,
        "visible": True
    }

def create_bottom_nav(active_index=0):
    nav_items = [
        {"label": "홈", "id_offset": 0},
        {"label": "약관리", "id_offset": 10},
        {"label": "가족", "id_offset": 20},
        {"label": "설정", "id_offset": 30}
    ]

    children = []
    for idx, item in enumerate(nav_items):
        is_active = idx == active_index
        color = COLORS["green"] if is_active else COLORS["light_gray"]
        font_style = "SemiBold" if is_active else "Regular"
        text_color = COLORS["green"] if is_active else COLORS["gray"]

        children.append({
            "id": f"nav:{idx}",
            "name": f"Nav Item {idx + 1}",
            "type": "FRAME",
            "width": 100,
            "height": 48,
            "layoutMode": "VERTICAL",
            "primaryAxisAlignItems": "CENTER",
            "counterAxisAlignItems": "CENTER",
            "itemSpacing": 4,
            "fills": [],
            "children": [
                {
                    "id": f"nav:{idx}:icon",
                    "name": "Icon",
                    "type": "RECTANGLE",
                    "width": 28,
                    "height": 28,
                    "fills": [{"type": "SOLID", "color": color}],
                    "cornerRadius": 6
                },
                {
                    "id": f"nav:{idx}:label",
                    "name": "Label",
                    "type": "TEXT",
                    "width": 60,
                    "height": 20,
                    "characters": item["label"],
                    "fontSize": 14,
                    "fontName": {"family": "Inter", "style": font_style},
                    "textAlignHorizontal": "CENTER",
                    "fills": [{"type": "SOLID", "color": text_color}]
                }
            ]
        })

    return {
        "id": "bottom_nav",
        "name": "Bottom Navigation",
        "type": "FRAME",
        "width": 1200,
        "height": 80,
        "x": 0,
        "y": 720,
        "layoutMode": "HORIZONTAL",
        "primaryAxisSizingMode": "FIXED",
        "counterAxisSizingMode": "FIXED",
        "primaryAxisAlignItems": "SPACE_BETWEEN",
        "counterAxisAlignItems": "CENTER",
        "paddingTop": 16,
        "paddingRight": 40,
        "paddingBottom": 16,
        "paddingLeft": 40,
        "itemSpacing": 0,
        "fills": [{"type": "SOLID", "color": COLORS["white"]}],
        "strokes": [{"type": "SOLID", "color": COLORS["border_gray"]}],
        "strokeWeight": 2,
        "children": children
    }

# Now generate all screens
screens = []

# Screen 1: Kakao Login
screens.append({
    "id": "1:100",
    "name": "01_카카오_로그인",
    "type": "FRAME",
    "width": 1200,
    "height": 800,
    "backgroundColor": COLORS["white"],
    "fills": [{"type": "SOLID", "color": COLORS["white"]}],
    "children": [
        {
            "id": "1:101",
            "name": "Kakao Logo",
            "type": "RECTANGLE",
            "width": 120,
            "height": 120,
            "x": 540,
            "y": 120,
            "fills": [{"type": "SOLID", "color": COLORS["yellow"]}],
            "cornerRadius": 24
        },
        {
            "id": "1:102",
            "name": "App Title",
            "type": "TEXT",
            "width": 400,
            "height": 80,
            "x": 400,
            "y": 280,
            "characters": "실버케어",
            "fontSize": 64,
            "fontName": {"family": "Inter", "style": "Bold"},
            "textAlignHorizontal": "CENTER",
            "fills": [{"type": "SOLID", "color": COLORS["dark"]}]
        },
        {
            "id": "1:103",
            "name": "Subtitle",
            "type": "TEXT",
            "width": 500,
            "height": 40,
            "x": 350,
            "y": 380,
            "characters": "어르신을 위한 스마트 건강 관리",
            "fontSize": 20,
            "fontName": {"family": "Inter", "style": "Regular"},
            "textAlignHorizontal": "CENTER",
            "fills": [{"type": "SOLID", "color": COLORS["gray"]}]
        },
        {
            "id": "1:104",
            "name": "Kakao Login Button",
            "type": "FRAME",
            "width": 500,
            "height": 64,
            "x": 350,
            "y": 480,
            "layoutMode": "HORIZONTAL",
            "primaryAxisAlignItems": "CENTER",
            "counterAxisAlignItems": "CENTER",
            "paddingLeft": 24,
            "paddingRight": 24,
            "paddingTop": 16,
            "paddingBottom": 16,
            "fills": [{"type": "SOLID", "color": COLORS["yellow"]}],
            "cornerRadius": 12,
            "effects": [create_shadow()],
            "children": [
                {
                    "id": "1:105",
                    "name": "Button Text",
                    "type": "TEXT",
                    "width": 300,
                    "height": 32,
                    "characters": "카카오로 3초만에 시작하기",
                    "fontSize": 18,
                    "fontName": {"family": "Inter", "style": "SemiBold"},
                    "textAlignHorizontal": "CENTER",
                    "fills": [{"type": "SOLID", "color": COLORS["dark"]}]
                }
            ]
        },
        {
            "id": "1:106",
            "name": "Info Text",
            "type": "TEXT",
            "width": 500,
            "height": 60,
            "x": 350,
            "y": 580,
            "characters": "간편하게 카카오 계정으로\\n실버케어를 시작하세요",
            "fontSize": 16,
            "fontName": {"family": "Inter", "style": "Regular"},
            "textAlignHorizontal": "CENTER",
            "lineHeight": {"value": 150, "unit": "PERCENT"},
            "fills": [{"type": "SOLID", "color": {"r": 0.6, "g": 0.6, "b": 0.6}}]
        },
        {
            "id": "1:107",
            "name": "Decoration Circle 1",
            "type": "ELLIPSE",
            "width": 80,
            "height": 80,
            "x": 100,
            "y": 150,
            "fills": [{"type": "SOLID", "color": {**COLORS["green"], "a": 0.1}}]
        },
        {
            "id": "1:108",
            "name": "Decoration Circle 2",
            "type": "ELLIPSE",
            "width": 60,
            "height": 60,
            "x": 1040,
            "y": 600,
            "fills": [{"type": "SOLID", "color": {**COLORS["blue"], "a": 0.1}}]
        }
    ]
})

# Continue with rest of screens...
print(json.dumps({"version": "7.0", "description": "실버케어 MVP - 21개 모던 화면 + 카카오 OAuth 전용", "screens": screens}, indent=2, ensure_ascii=False))
