#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "content" / "notes" / "ai-knowledge-topics.json"
POSTER_DIR = ROOT / "assets" / "images" / "writing" / "generated"
SCENE_DIR = POSTER_DIR / "fantasy-scenes"
HEADER_IMAGE = SCENE_DIR / "knowledge-map-header-fantasy.png"

FONT_REGULAR = Path("/home/tiammomo/.local/share/fonts/NotoSansCJK-Regular.ttc")
FONT_BOLD = Path("/home/tiammomo/.local/share/fonts/NotoSansCJK-Bold.ttc")
FONT_SERIF_BOLD = Path("/home/tiammomo/.local/share/fonts/NotoSerifCJK-Bold.ttc")

CANVAS_W = 1800
CANVAS_H = 1030
MARGIN = 22
GAP = 8

INK = (10, 31, 70)
BLUE = (18, 76, 150)
MUTED = (70, 88, 120)
LIGHT_MUTED = (111, 128, 154)
PAPER = (255, 252, 244)
PAPER_COOL = (248, 252, 255)
CARD = (255, 255, 252)
BORDER = (197, 209, 226)
TEAL = (31, 155, 154)
CYAN = (67, 184, 219)
GOLD = (220, 158, 52)
ORANGE = (236, 112, 38)
GREEN = (67, 160, 104)
VIOLET = (104, 96, 196)
RED = (218, 86, 96)


def load_topics() -> list[dict[str, Any]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def font(size: int, *, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_SERIF_BOLD if serif else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(str(path), size)


def text_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=face)
    return bbox[2] - bbox[0]


def wrap_by_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for char in paragraph:
            trial = current + char
            if current and text_width(draw, trial, face) > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return lines


def draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    x: int,
    y: int,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    *,
    line_gap: int = 5,
    max_lines: int | None = None,
) -> int:
    selected = lines if max_lines is None else lines[:max_lines]
    for line in selected:
        draw.text((x, y), line, font=face, fill=fill)
        y += face.size + line_gap
    return y


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int] | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def alpha_paste(canvas: Image.Image, image: Image.Image, xy: tuple[int, int], opacity: int) -> None:
    layer = image.convert("RGBA")
    alpha = layer.getchannel("A").point(lambda value: value * opacity // 255)
    layer.putalpha(alpha)
    canvas.alpha_composite(layer, xy)


def header_banner(size: tuple[int, int]) -> Image.Image | None:
    if not HEADER_IMAGE.exists():
        return None
    source = Image.open(HEADER_IMAGE).convert("RGB")
    banner = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    banner = ImageEnhanceLike(banner).soften()
    return banner.convert("RGBA")


class ImageEnhanceLike:
    def __init__(self, image: Image.Image) -> None:
        self.image = image

    def soften(self) -> Image.Image:
        img = self.image.filter(ImageFilter.GaussianBlur(0.25)).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (255, 252, 244, 54))
        img.alpha_composite(overlay)
        return img


def draw_fantasy_frame(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((12, 12, CANVAS_W - 12, CANVAS_H - 12), outline=(202, 171, 113), width=2)
    draw.rectangle((20, 20, CANVAS_W - 20, CANVAS_H - 20), outline=(222, 203, 166), width=1)
    corner = 92
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        ox = 20 if sx == 1 else CANVAS_W - 20
        oy = 20 if sy == 1 else CANVAS_H - 20
        draw.line((ox, oy + sy * corner, ox + sx * corner, oy), fill=(202, 171, 113), width=2)
        draw.arc((ox - 42, oy - 42, ox + 42, oy + 42), start=0, end=360, fill=(222, 203, 166), width=1)


def draw_small_icon(draw: ImageDraw.ImageDraw, x: int, y: int, kind: int, accent: tuple[int, int, int]) -> None:
    if kind % 6 == 0:
        draw.polygon([(x + 20, y), (x + 38, y + 22), (x + 20, y + 54), (x + 2, y + 22)], fill=(229, 246, 250), outline=accent)
        draw.line((x + 20, y, x + 20, y + 54), fill=accent, width=2)
        draw.line((x + 2, y + 22, x + 38, y + 22), fill=accent, width=2)
    elif kind % 6 == 1:
        rounded(draw, (x, y + 4, x + 50, y + 56), 7, (255, 250, 236), accent, 2)
        draw.line((x + 25, y + 4, x + 25, y + 56), fill=accent, width=2)
        draw.line((x + 9, y + 18, x + 20, y + 18), fill=(184, 152, 97), width=2)
        draw.line((x + 31, y + 18, x + 43, y + 18), fill=(184, 152, 97), width=2)
    elif kind % 6 == 2:
        draw.ellipse((x, y + 2, x + 54, y + 56), fill=(247, 252, 255), outline=accent, width=2)
        draw.line((x + 27, y + 10, x + 27, y + 48), fill=accent, width=2)
        draw.line((x + 9, y + 29, x + 45, y + 29), fill=accent, width=2)
        draw.polygon([(x + 27, y + 12), (x + 33, y + 29), (x + 27, y + 46), (x + 21, y + 29)], outline=GOLD, fill=None)
    elif kind % 6 == 3:
        rounded(draw, (x + 4, y + 8, x + 50, y + 48), 8, (246, 250, 255), accent, 2)
        draw.rectangle((x + 15, y + 1, x + 39, y + 12), fill=(255, 250, 236), outline=accent)
        draw.line((x + 14, y + 24, x + 40, y + 24), fill=LIGHT_MUTED, width=2)
        draw.line((x + 14, y + 34, x + 34, y + 34), fill=LIGHT_MUTED, width=2)
    elif kind % 6 == 4:
        draw.polygon([(x + 27, y + 2), (x + 50, y + 12), (x + 45, y + 42), (x + 27, y + 58), (x + 9, y + 42), (x + 4, y + 12)], fill=(244, 252, 248), outline=accent)
        draw.line((x + 17, y + 29, x + 25, y + 38), fill=accent, width=3)
        draw.line((x + 25, y + 38, x + 39, y + 19), fill=accent, width=3)
    else:
        draw.ellipse((x + 3, y + 16, x + 39, y + 52), fill=(249, 253, 255), outline=accent, width=2)
        draw.line((x + 36, y + 47, x + 52, y + 60), fill=accent, width=4)
        draw.line((x + 15, y + 2, x + 27, y + 16), fill=GOLD, width=2)
        draw.line((x + 32, y + 1, x + 30, y + 17), fill=GOLD, width=2)


def short_title(topic: dict[str, Any]) -> str:
    base = topic["cardTitle"].split("：", 1)[0]
    return f"一张图讲懂：{base}"


def draw_header(canvas: Image.Image, draw: ImageDraw.ImageDraw, topic: dict[str, Any]) -> None:
    x1, y1, x2, y2 = MARGIN, 20, CANVAS_W - MARGIN, 154
    rounded(draw, (x1, y1, x2, y2), 16, (255, 251, 241), (212, 192, 151), 2)

    banner = header_banner((x2 - x1 - 20, y2 - y1 - 20))
    if banner:
        alpha_paste(canvas, banner, (x1 + 10, y1 + 10), 178)
        veil = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        veil_draw = ImageDraw.Draw(veil)
        veil_draw.rounded_rectangle((x1 + 380, y1 + 14, x2 - 380, y2 - 14), radius=12, fill=(255, 252, 244, 198))
        canvas.alpha_composite(veil)

    title = short_title(topic)
    title_face = font(48, bold=True, serif=True)
    sub_face = font(22)
    title_w = text_width(draw, title, title_face)
    draw.text(((CANVAS_W - title_w) // 2, y1 + 18), title, font=title_face, fill=INK)
    english = topic["cardTitle"].split("：", 1)[-1] if "：" in topic["cardTitle"] else topic["category"]
    english_face = font(25, bold=True, serif=True)
    english_w = text_width(draw, english, english_face)
    draw.text(((CANVAS_W - english_w) // 2, y1 + 74), english, font=english_face, fill=BLUE)
    subtitle = topic["subtitle"]
    sub_lines = wrap_by_width(draw, subtitle, sub_face, 1280)
    sub_w = max(text_width(draw, line, sub_face) for line in sub_lines[:1])
    draw_lines(draw, sub_lines[:1], (CANVAS_W - sub_w) // 2, y1 + 108, sub_face, INK, max_lines=1)

    for dx in (-440, 440):
        cx = CANVAS_W // 2 + dx
        cy = y1 + 66
        draw.line((cx - 42, cy, cx + 42, cy), fill=(173, 193, 218), width=1)
        draw.polygon([(cx - 2, cy - 5), (cx + 5, cy), (cx - 2, cy + 5), (cx - 9, cy)], fill=CYAN)
        draw.text((cx - 72, cy - 22), "✧", font=font(22), fill=CYAN)


def draw_panel(
    draw: ImageDraw.ImageDraw,
    index: int,
    title: str,
    bullets: list[str],
    box: tuple[int, int, int, int],
    *,
    accent: tuple[int, int, int],
    icon: bool = True,
    max_bullets: int = 4,
    dense: bool = False,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, 12, CARD, BORDER, 1)
    draw.rectangle((x1 + 1, y1 + 1, x2 - 1, y1 + 31), fill=(247, 251, 255))
    number_face = font(17, bold=True)
    draw.ellipse((x1 + 14, y1 + 10, x1 + 42, y1 + 38), fill=accent)
    draw.text((x1 + 28 - text_width(draw, str(index), number_face) // 2, y1 + 10), str(index), font=number_face, fill=(255, 255, 255))
    title_face = font(20 if len(title) < 13 else 18, bold=True)
    draw.text((x1 + 52, y1 + 10), title, font=title_face, fill=BLUE)

    if icon:
        draw_small_icon(draw, x2 - 62, y1 + 48, index, accent)

    body_face = font(15 if dense else 16)
    yy = y1 + 54
    text_max = x2 - x1 - (108 if icon else 42)
    for bullet in bullets[:max_bullets]:
        if yy > y2 - 28:
            break
        draw.ellipse((x1 + 22, yy + 8, x1 + 29, yy + 15), fill=accent)
        wrapped = wrap_by_width(draw, bullet, body_face, text_max)
        yy = draw_lines(draw, wrapped, x1 + 38, yy, body_face, INK if dense else MUTED, line_gap=3, max_lines=2)
        yy += 3
    if bullets and y2 - yy > 44:
        note = f"重点：{bullets[-1]}"
        note_face = font(13, bold=True)
        rounded(draw, (x1 + 22, y2 - 42, x2 - 22, y2 - 12), 7, (255, 249, 236), (230, 201, 150), 1)
        draw_lines(draw, wrap_by_width(draw, note, note_face, x2 - x1 - 70), x1 + 34, y2 - 34, note_face, INK, line_gap=1, max_lines=1)


def flow_bullets(topic: dict[str, Any]) -> list[str]:
    steps = topic["flow"]
    return [f"{idx}. {step}" for idx, step in enumerate(steps, start=1)]


def merged_bullets(*sections: dict[str, Any], limit: int = 5) -> list[str]:
    bullets: list[str] = []
    for section in sections:
        bullets.extend(section["bullets"])
    return bullets[:limit]


def draw_flow_panel(draw: ImageDraw.ImageDraw, index: int, topic: dict[str, Any], box: tuple[int, int, int, int], accent: tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, 12, CARD, BORDER, 1)
    draw.rectangle((x1 + 1, y1 + 1, x2 - 1, y1 + 32), fill=(247, 251, 255))
    number_face = font(17, bold=True)
    draw.ellipse((x1 + 14, y1 + 10, x1 + 42, y1 + 38), fill=accent)
    draw.text((x1 + 28 - text_width(draw, str(index), number_face) // 2, y1 + 10), str(index), font=number_face, fill=(255, 255, 255))
    draw.text((x1 + 52, y1 + 10), "典型工作流 / 运行闭环", font=font(20, bold=True), fill=BLUE)

    steps = topic["flow"][:8]
    sx = x1 + 24
    sy = y1 + 56
    usable_w = x2 - x1 - 48
    step_gap = 8
    step_w = (usable_w - step_gap * (len(steps) - 1)) // len(steps)
    step_h = 70
    for idx, step in enumerate(steps):
        bx = sx + idx * (step_w + step_gap)
        fill = (255, 252, 243) if idx % 2 else (242, 252, 252)
        outline = (230, 201, 150) if idx % 2 else (167, 219, 217)
        rounded(draw, (bx, sy, bx + step_w, sy + step_h), 8, fill, outline, 1)
        draw.text((bx + 10, sy + 9), str(idx + 1), font=font(17, bold=True), fill=ORANGE if idx % 2 else TEAL)
        lines = wrap_by_width(draw, step, font(16, bold=True), step_w - 44)
        yy = draw_lines(draw, lines, bx + 34, sy + 9, font(16, bold=True), INK, line_gap=2, max_lines=2)
        section = topic["sections"][idx % len(topic["sections"])]
        detail = section["bullets"][0]
        detail_lines = wrap_by_width(draw, detail, font(12), step_w - 24)
        draw_lines(draw, detail_lines, bx + 12, max(yy + 5, sy + 38), font(12), MUTED, line_gap=1, max_lines=2)
        if idx < len(steps) - 1:
            ax = bx + step_w + 2
            ay = sy + step_h // 2
            draw.line((ax, ay, ax + 6, ay), fill=(143, 164, 193), width=2)
            draw.polygon([(ax + 6, ay), (ax + 1, ay - 4), (ax + 1, ay + 4)], fill=(143, 164, 193))

    quote = topic["quote"]
    lines = wrap_by_width(draw, quote, font(16, bold=True), x2 - x1 - 60)
    rounded(draw, (x1 + 24, y2 - 58, x2 - 24, y2 - 18), 8, (255, 249, 236), (230, 201, 150), 1)
    draw_lines(draw, lines, x1 + 42, y2 - 49, font(16, bold=True), INK, line_gap=2, max_lines=2)


def draw_footer(draw: ImageDraw.ImageDraw, topic: dict[str, Any]) -> None:
    y = CANVAS_H - 48
    rounded(draw, (MARGIN, y, CANVAS_W - MARGIN, CANVAS_H - 18), 10, (255, 255, 252), (222, 203, 166), 1)
    line = f"{topic['cardTitle']} = 结构化知识 + 可执行流程 + 工程边界"
    face = font(21, bold=True)
    draw.text(((CANVAS_W - text_width(draw, line, face)) // 2, y + 5), line, font=face, fill=BLUE)


def panel_specs(topic: dict[str, Any]) -> list[dict[str, Any]]:
    sections = topic["sections"]
    return [
        {"title": sections[0]["title"], "bullets": sections[0]["bullets"], "icon": True},
        {"title": sections[1]["title"], "bullets": sections[1]["bullets"], "icon": True},
        {"title": sections[2]["title"], "bullets": sections[2]["bullets"], "icon": True},
        {"title": sections[3]["title"], "bullets": sections[3]["bullets"], "icon": True},
        {"title": "典型工作流", "bullets": flow_bullets(topic), "flow": True},
        {"title": sections[4]["title"], "bullets": sections[4]["bullets"], "icon": True},
        {"title": sections[5]["title"], "bullets": sections[5]["bullets"], "icon": True},
        {"title": sections[6]["title"], "bullets": sections[6]["bullets"], "icon": True},
        {"title": "风险与工程落地", "bullets": merged_bullets(sections[7], sections[8], limit=5), "icon": True},
        {"title": "快速心法", "bullets": topic["checklist"], "icon": True},
    ]


def render_poster(topic: dict[str, Any]) -> Path:
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), PAPER + (255,))
    draw = ImageDraw.Draw(canvas)

    for x in range(0, CANVAS_W, 48):
        draw.line((x, 0, x, CANVAS_H), fill=(246, 239, 226), width=1)
    for y in range(0, CANVAS_H, 48):
        draw.line((0, y, CANVAS_W, y), fill=(246, 239, 226), width=1)

    draw_fantasy_frame(draw)
    draw_header(canvas, draw, topic)

    accents = [BLUE, TEAL, VIOLET, GREEN, GOLD, ORANGE, CYAN, (78, 119, 218), RED, (43, 146, 106)]
    specs = panel_specs(topic)

    row1_y = 164
    row1_h = 224
    row1_w = (CANVAS_W - MARGIN * 2 - GAP * 3) // 4
    for i in range(4):
        x = MARGIN + i * (row1_w + GAP)
        draw_panel(draw, i + 1, specs[i]["title"], specs[i]["bullets"], (x, row1_y, x + row1_w, row1_y + row1_h), accent=accents[i], max_bullets=5, dense=True)

    row2_y = row1_y + row1_h + GAP
    row2_h = 204
    draw_flow_panel(draw, 5, topic, (MARGIN, row2_y, CANVAS_W - MARGIN, row2_y + row2_h), accents[4])

    row3_y = row2_y + row2_h + GAP
    row3_h = 176
    row3_w = (CANVAS_W - MARGIN * 2 - GAP * 2) // 3
    for offset, spec_idx in enumerate((5, 6, 7)):
        x = MARGIN + offset * (row3_w + GAP)
        draw_panel(draw, spec_idx + 1, specs[spec_idx]["title"], specs[spec_idx]["bullets"], (x, row3_y, x + row3_w, row3_y + row3_h), accent=accents[spec_idx], max_bullets=5, dense=True)

    row4_y = row3_y + row3_h + GAP
    row4_h = 156
    row4_w = row3_w
    draw_panel(draw, 9, specs[8]["title"], specs[8]["bullets"], (MARGIN, row4_y, MARGIN + row4_w, row4_y + row4_h), accent=accents[8], max_bullets=5, dense=True)
    x_mid = MARGIN + row4_w + GAP
    draw_panel(draw, 10, specs[9]["title"], specs[9]["bullets"], (x_mid, row4_y, x_mid + row4_w, row4_y + row4_h), accent=accents[9], max_bullets=5, dense=True)
    x_right = MARGIN + 2 * (row4_w + GAP)
    final_bullets = [
        f"先落地：{topic['flow'][0]} → {topic['flow'][1]}",
        f"再增强：{topic['flow'][2]} → {topic['flow'][3]}",
        f"最后治理：{topic['flow'][-2]} → {topic['flow'][-1]}",
        "所有改动沉淀到数据源、Trace 和回归样本",
    ]
    draw_panel(draw, 11, "落地顺序", final_bullets, (x_right, row4_y, x_right + row4_w, row4_y + row4_h), accent=VIOLET, max_bullets=4, dense=True)

    draw_footer(draw, topic)

    out = POSTER_DIR / topic["poster"]
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    return out


def poster_path(topic: dict[str, Any]) -> Path:
    return POSTER_DIR / topic["poster"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build AI knowledge posters from structured topic data.")
    parser.add_argument("slugs", nargs="*", help="Optional topic slugs to generate. Omit to generate all topics.")
    parser.add_argument("--overwrite-posters", action="store_true", help="Overwrite existing poster images with deterministic draft posters.")
    args = parser.parse_args()

    selected = set(args.slugs)
    topics = load_topics()
    if selected:
        topics = [topic for topic in topics if topic["slug"] in selected]
        missing = selected - {topic["slug"] for topic in topics}
        if missing:
            raise SystemExit(f"Unknown topic slug(s): {', '.join(sorted(missing))}")

    posters: list[Path] = []
    skipped_posters: list[Path] = []
    for topic in topics:
        current_poster = poster_path(topic)
        if args.overwrite_posters or not current_poster.exists():
            posters.append(render_poster(topic))
        else:
            skipped_posters.append(current_poster)

    print("Generated posters:")
    for path in posters:
        print(f"- {path.relative_to(ROOT)}")
    if skipped_posters:
        print("Skipped existing posters:")
        for path in skipped_posters:
            print(f"- {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
