from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parent
FIGMA_EXPORT_DIR = REPO_ROOT / "figma-exports" / "v2"
OUTPUT_FILE = FIGMA_EXPORT_DIR / "repository-markdown-library.json"

FONT_PRIMARY = {"family": "Inter", "style": "Bold"}
FONT_BODY = {"family": "Inter", "style": "Regular"}
FONT_MONO = {"family": "IBM Plex Mono", "style": "Regular"}

BACKGROUND_GRADIENT = {
    "type": "GRADIENT_LINEAR",
    "gradientTransform": [[1, 0, 0], [0, 1, 0]],
    "gradientStops": [
        {"color": {"r": 0.96, "g": 0.98, "b": 1.0, "a": 1}, "position": 0},
        {"color": {"r": 0.89, "g": 0.94, "b": 1.0, "a": 1}, "position": 1},
    ],
}

CARD_FILL = {
    "type": "SOLID",
    "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 0.92},
}

CARD_SHADOW = {
    "type": "DROP_SHADOW",
    "color": {"r": 0.11, "g": 0.2, "b": 0.4, "a": 0.08},
    "offset": {"x": 0, "y": 12},
    "radius": 40,
    "visible": True,
}

TEXT_FILL_PRIMARY = {
    "type": "SOLID",
    "color": {"r": 0.1, "g": 0.12, "b": 0.18, "a": 1},
}

TEXT_FILL_MUTED = {
    "type": "SOLID",
    "color": {"r": 0.35, "g": 0.4, "b": 0.52, "a": 1},
}


def collect_markdown_files() -> List[Path]:
    markdown_files = sorted(
        path
        for path in REPO_ROOT.rglob("*.md")
        if path.is_file()
    )
    return markdown_files


def flush_paragraph(paragraph: List[str], blocks: List[Dict[str, Any]]) -> None:
    if paragraph:
        text = " ".join(line.strip() for line in paragraph if line.strip())
        if text:
            blocks.append({"type": "paragraph", "text": text})
        paragraph.clear()


def flush_list(items: Optional[List[str]], blocks: List[Dict[str, Any]]) -> Optional[List[str]]:
    if items:
        cleaned = [item for item in items if item]
        if cleaned:
            blocks.append({"type": "list", "items": cleaned})
    return None


def parse_markdown(content: str) -> List[Dict[str, Any]]:
    lines = content.replace("\r\n", "\n").split("\n")
    blocks: List[Dict[str, Any]] = []
    paragraph: List[str] = []
    list_items: Optional[List[str]] = None
    in_code_block = False
    code_lines: List[str] = []

    def flush_code_block() -> None:
        nonlocal code_lines, in_code_block
        if code_lines:
            blocks.append({"type": "code", "text": "\n".join(code_lines)})
            code_lines = []
        in_code_block = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code_block:
                flush_code_block()
            else:
                flush_paragraph(paragraph, blocks)
                list_items = flush_list(list_items, blocks)
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        if not stripped:
            flush_paragraph(paragraph, blocks)
            list_items = flush_list(list_items, blocks)
            continue

        if stripped.startswith("#"):
            flush_paragraph(paragraph, blocks)
            list_items = flush_list(list_items, blocks)
            level = len(stripped) - len(stripped.lstrip("#"))
            heading_text = stripped[level:].strip()
            if heading_text:
                blocks.append({"type": "heading", "level": level, "text": heading_text})
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_paragraph(paragraph, blocks)
            if list_items is None:
                list_items = []
            list_items.append(stripped[2:].strip())
            continue

        if list_items:
            list_items = flush_list(list_items, blocks)

        paragraph.append(line)

    flush_paragraph(paragraph, blocks)
    list_items = flush_list(list_items, blocks)
    if in_code_block:
        flush_code_block()

    return blocks


def create_text_node(
    name: str,
    text: str,
    *,
    font: Dict[str, str],
    font_size: int,
    line_height: int,
    fills: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    return {
        "name": name,
        "type": "TEXT",
        "characters": text,
        "fontSize": font_size,
        "fontName": font,
        "fills": fills or [TEXT_FILL_PRIMARY],
        "lineHeightPx": line_height,
    }


def build_list_children(items: List[str]) -> List[Dict[str, Any]]:
    children = []
    for index, item in enumerate(items, start=1):
        children.append(
            create_text_node(
                name=f"목록 항목 {index}",
                text=f"• {item}",
                font=FONT_BODY,
                font_size=18,
                line_height=26,
                fills=[TEXT_FILL_PRIMARY],
            )
        )
    return children


def build_content_children(blocks: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    children: List[Dict[str, Any]] = []
    for idx, block in enumerate(blocks, start=1):
        if block["type"] == "heading":
            level = block.get("level", 1)
            font_size = 40 if level == 1 else 28 if level == 2 else 22
            line_height = 48 if level == 1 else 34 if level == 2 else 28
            children.append(
                create_text_node(
                    name=f"제목 {idx}",
                    text=block.get("text", ""),
                    font=FONT_PRIMARY if level <= 2 else FONT_BODY,
                    font_size=font_size,
                    line_height=line_height,
                )
            )
        elif block["type"] == "paragraph":
            children.append(
                create_text_node(
                    name=f"본문 {idx}",
                    text=block.get("text", ""),
                    font=FONT_BODY,
                    font_size=18,
                    line_height=28,
                )
            )
        elif block["type"] == "list":
            list_children = build_list_children(block.get("items", []))
            children.append(
                {
                    "name": f"목록 {idx}",
                    "type": "FRAME",
                    "layoutMode": "VERTICAL",
                    "primaryAxisSizingMode": "AUTO",
                    "counterAxisSizingMode": "FIXED",
                    "counterAxisAlignItems": "MIN",
                    "itemSpacing": 12,
                    "fills": [],
                    "strokes": [],
                    "children": list_children,
                }
            )
        elif block["type"] == "code":
            children.append(
                {
                    "name": f"코드 블록 {idx}",
                    "type": "FRAME",
                    "layoutMode": "VERTICAL",
                    "primaryAxisSizingMode": "AUTO",
                    "counterAxisSizingMode": "FIXED",
                    "counterAxisAlignItems": "MIN",
                    "paddingTop": 24,
                    "paddingRight": 28,
                    "paddingBottom": 24,
                    "paddingLeft": 28,
                    "itemSpacing": 0,
                    "cornerRadius": 20,
                    "fills": [
                        {
                            "type": "SOLID",
                            "color": {"r": 0.08, "g": 0.1, "b": 0.16, "a": 0.92},
                        }
                    ],
                    "effects": [
                        {
                            "type": "INNER_SHADOW",
                            "color": {"r": 0.35, "g": 0.48, "b": 0.92, "a": 0.24},
                            "offset": {"x": 0, "y": 0},
                            "radius": 2,
                            "visible": True,
                        }
                    ],
                    "children": [
                        create_text_node(
                            name=f"코드 내용 {idx}",
                            text=block.get("text", ""),
                            font=FONT_MONO,
                            font_size=16,
                            line_height=24,
                            fills=[
                                {
                                    "type": "SOLID",
                                    "color": {"r": 0.8, "g": 0.85, "b": 0.94, "a": 1},
                                }
                            ],
                        )
                    ],
                }
            )

    return children or [
        create_text_node(
            name="본문", text="(내용이 비어 있습니다)", font=FONT_BODY, font_size=18, line_height=28
        )
    ]


def estimate_height(text: str, blocks: Iterable[Dict[str, Any]]) -> int:
    line_count = text.count("\n") + 1
    block_bonus = sum(
        80
        if block["type"] == "heading"
        else 64
        if block["type"] == "paragraph"
        else 72
        if block["type"] == "list"
        else 96
        for block in blocks
    )
    estimated = 360 + line_count * 18 + block_bonus
    return max(800, min(5000, estimated))


def build_screen(markdown_path: Path) -> Dict[str, Any]:
    relative_path = markdown_path.relative_to(REPO_ROOT)
    content = markdown_path.read_text(encoding="utf-8")
    normalized_content = content.replace("\r\n", "\n")
    blocks = parse_markdown(normalized_content)
    height = estimate_height(normalized_content, blocks)
    line_count = content.count("\n") + 1

    metadata_text = f"경로: {relative_path}\n총 줄 수: {line_count}"

    content_children = build_content_children(blocks)

    screen = {
        "name": str(relative_path),
        "type": "FRAME",
        "width": 1440,
        "height": height,
        "layoutMode": "VERTICAL",
        "primaryAxisSizingMode": "FIXED",
        "counterAxisSizingMode": "FIXED",
        "primaryAxisAlignItems": "MIN",
        "counterAxisAlignItems": "MIN",
        "paddingTop": 80,
        "paddingRight": 96,
        "paddingBottom": 120,
        "paddingLeft": 96,
        "itemSpacing": 32,
        "cornerRadius": 56,
        "fills": [BACKGROUND_GRADIENT],
        "strokes": [],
        "effects": [
            {
                "type": "BACKGROUND_BLUR",
                "radius": 24,
                "visible": True,
            },
            CARD_SHADOW,
        ],
        "children": [
            {
                "name": "문서 제목",
                "type": "TEXT",
                "characters": relative_path.name,
                "fontSize": 54,
                "fontName": FONT_PRIMARY,
                "fills": [TEXT_FILL_PRIMARY],
                "lineHeightPx": 60,
            },
            {
                "name": "문서 정보",
                "type": "TEXT",
                "characters": metadata_text,
                "fontSize": 20,
                "fontName": FONT_BODY,
                "fills": [TEXT_FILL_MUTED],
                "lineHeightPx": 28,
            },
            {
                "name": "콘텐츠",
                "type": "FRAME",
                "layoutMode": "VERTICAL",
                "primaryAxisSizingMode": "AUTO",
                "counterAxisSizingMode": "FIXED",
                "counterAxisAlignItems": "MIN",
                "itemSpacing": 28,
                "paddingTop": 40,
                "paddingRight": 48,
                "paddingBottom": 48,
                "paddingLeft": 48,
                "cornerRadius": 32,
                "fills": [CARD_FILL],
                "strokes": [
                    {
                        "type": "SOLID",
                        "color": {"r": 0.85, "g": 0.88, "b": 0.95, "a": 1},
                    }
                ],
                "effects": [CARD_SHADOW],
                "children": content_children,
            },
        ],
    }

    return screen


def build_document() -> Dict[str, Any]:
    markdown_files = collect_markdown_files()
    screens = [build_screen(path) for path in markdown_files]

    document = {
        "version": "6.0",
        "description": "Repository Markdown Documentation Library",
        "screens": screens,
    }
    return document


def main() -> None:
    document = build_document()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(document, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Exported {len(document['screens'])} markdown screens to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
