#!/usr/bin/env python3
import json


def has_keyword(name, keywords):
    """Check if any keyword is in the frame name (case-insensitive)"""
    name_lower = name.lower()
    return any(keyword.lower() in name_lower for keyword in keywords)

def is_white_background(fills):
    """Check if the fill is white (r,g,b >= 0.95)"""
    if not fills or len(fills) == 0:
        return False
    fill = fills[0]
    if fill.get("type") != "SOLID":
        return False
    color = fill.get("color", {})
    return (color.get("r", 0) >= 0.95 and
            color.get("g", 0) >= 0.95 and
            color.get("b", 0) >= 0.95)

def has_green_or_blue_fill(fills):
    """Check if the fill is green or blue solid color"""
    if not fills or len(fills) == 0:
        return False
    fill = fills[0]
    if fill.get("type") != "SOLID":
        return False
    color = fill.get("color", {})
    # Check for blue (high b value) or green (high g value)
    return (color.get("b", 0) > 0.5 or color.get("g", 0) > 0.5)

def apply_header_style(frame):
    """Apply Vision Pro style to Header frames"""
    frame["fills"] = [
        {
            "type": "SOLID",
            "color": {"r": 1, "g": 1, "b": 1, "a": 0.7}
        }
    ]
    frame["effects"] = [
        {"type": "BACKGROUND_BLUR", "radius": 20, "visible": True},
        {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0, "b": 0, "a": 0.05},
            "offset": {"x": 0, "y": 1},
            "radius": 0,
            "visible": True
        }
    ]
    return True

def apply_card_style(frame):
    """Apply Vision Pro style to Card/Container/Item frames"""
    # Increase cornerRadius by 1.5x (max 30px)
    if "cornerRadius" in frame:
        new_radius = min(frame["cornerRadius"] * 1.5, 30)
        frame["cornerRadius"] = new_radius

    # If white background, set alpha to 0.9
    if "fills" in frame and is_white_background(frame["fills"]):
        frame["fills"][0]["color"]["a"] = 0.9

    # Apply effects
    frame["effects"] = [
        {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0, "b": 0, "a": 0.08},
            "offset": {"x": 0, "y": 8},
            "radius": 25,
            "visible": True
        },
        {
            "type": "INNER_SHADOW",
            "color": {"r": 0, "g": 0.48, "b": 1, "a": 0.1},
            "offset": {"x": 0, "y": 0},
            "radius": 2,
            "spread": 1,
            "visible": True
        }
    ]
    return True

def apply_button_style(frame):
    """Apply Vision Pro style to Button frames"""
    frame["cornerRadius"] = 25

    # Convert green/blue solid fills to gradient
    if "fills" in frame and has_green_or_blue_fill(frame["fills"]):
        frame["fills"] = [
            {
                "type": "GRADIENT_LINEAR",
                "gradientTransform": [[0, 1, 0], [1, 0, 0]],
                "gradientStops": [
                    {
                        "color": {"r": 0, "g": 0.48, "b": 1, "a": 1},
                        "position": 0
                    },
                    {
                        "color": {"r": 0.35, "g": 0.8, "b": 0.98, "a": 1},
                        "position": 1
                    }
                ]
            }
        ]

    # Apply effects
    frame["effects"] = [
        {
            "type": "DROP_SHADOW",
            "color": {"r": 0, "g": 0.48, "b": 1, "a": 0.4},
            "offset": {"x": 0, "y": 5},
            "radius": 20,
            "visible": True
        }
    ]
    return True

def apply_search_style(frame):
    """Apply Vision Pro style to Search frames (Cards + BACKGROUND_BLUR)"""
    # First apply card style
    apply_card_style(frame)

    # Add background blur to effects
    if "effects" not in frame:
        frame["effects"] = []
    frame["effects"].insert(0, {"type": "BACKGROUND_BLUR", "radius": 20, "visible": True})
    return True

def apply_vision_pro_style(frame, stats):
    """Recursively apply Vision Pro style to frames"""
    if not isinstance(frame, dict):
        return

    frame_name = frame.get("name", "")

    # Apply styles based on frame name
    if frame_name == "Header":
        if apply_header_style(frame):
            stats["headers"] += 1
    elif has_keyword(frame_name, ["Search"]):
        if apply_search_style(frame):
            stats["search_boxes"] += 1
    elif has_keyword(frame_name, ["Button", "버튼", "Btn"]):
        if apply_button_style(frame):
            stats["buttons"] += 1
    elif has_keyword(frame_name, ["Card", "Container", "Item"]):
        if apply_card_style(frame):
            stats["cards"] += 1

    # Recursively process children
    if "children" in frame:
        for child in frame["children"]:
            apply_vision_pro_style(child, stats)

def main():
    input_file = "/home/user/.github/figma-exports/all-screens-with-flows.json"

    # Load the JSON file
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Statistics
    stats = {
        "headers": 0,
        "cards": 0,
        "buttons": 0,
        "search_boxes": 0
    }

    # Process all screens
    screens_count = len(data.get("screens", []))
    print(f"Processing {screens_count} screens...")

    for screen in data.get("screens", []):
        apply_vision_pro_style(screen, stats)

    # Save the modified JSON
    print(f"Saving to {input_file}...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print statistics
    print("\nVision Pro Style Applied Successfully!")
    print(f"Screens processed: {screens_count}")
    print(f"Headers styled: {stats['headers']}")
    print(f"Cards/Containers styled: {stats['cards']}")
    print(f"Buttons styled: {stats['buttons']}")
    print(f"Search boxes styled: {stats['search_boxes']}")
    print(f"Total elements styled: {sum(stats.values())}")

if __name__ == "__main__":
    main()
