#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "images" / "replacements"
OUTPUT_DIR = ROOT / "assets" / "images" / "generated"
EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


@dataclass(frozen=True)
class ImageSlot:
    source_name: str
    output_base: str
    main_width: int
    webp_quality: int = 78
    thumb_width: int = 760
    thumb_quality: int = 74


SLOTS = [
    ImageSlot("portfolio-og", "anime-portfolio-og", 1440),
    ImageSlot("modelport", "anime-cover-modelport", 1200),
    ImageSlot("quantpilot", "anime-cover-quantpilot", 1200),
    ImageSlot("travel-agent", "anime-cover-travel-agent", 1200),
    ImageSlot("mamoji", "anime-cover-mamoji", 1200),
    ImageSlot("reviewpilot", "anime-cover-reviewpilot", 1200),
    ImageSlot("stock-assistant", "anime-cover-stock-assistant", 1200),
]


def import_pillow():
    try:
        from PIL import Image
    except ModuleNotFoundError:
        print(
            "Pillow is required for image processing.\n"
            "Install it in a temporary virtual environment, for example:\n\n"
            "  python3 -m venv /tmp/portfolio-image-tools\n"
            "  /tmp/portfolio-image-tools/bin/python -m pip install pillow\n"
            "  /tmp/portfolio-image-tools/bin/python scripts/build_project_images.py\n",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return Image


def find_source(slot: ImageSlot) -> Path | None:
    for ext in EXTENSIONS:
        path = SOURCE_DIR / f"{slot.source_name}{ext}"
        if path.exists():
            return path
    return None


def crop_to_ratio(image, ratio: float):
    width, height = image.size
    current = width / height
    if abs(current - ratio) < 0.001:
        return image

    if current > ratio:
        new_width = round(height * ratio)
        left = (width - new_width) // 2
        return image.crop((left, 0, left + new_width, height))

    new_height = round(width / ratio)
    top = (height - new_height) // 2
    return image.crop((0, top, width, top + new_height))


def resize_width(Image, image, width: int):
    if image.width <= width:
        return image
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def build_slot(Image, slot: ImageSlot, source: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    original = Image.open(source).convert("RGB")
    cropped = crop_to_ratio(original, 16 / 9)

    main = resize_width(Image, cropped, slot.main_width)
    thumb = resize_width(Image, cropped, slot.thumb_width)

    png_path = OUTPUT_DIR / f"{slot.output_base}.png"
    webp_path = OUTPUT_DIR / f"{slot.output_base}.webp"
    thumb_path = OUTPUT_DIR / f"{slot.output_base}-thumb.webp"

    main.save(png_path, "PNG", optimize=True)
    main.save(webp_path, "WEBP", quality=slot.webp_quality, method=6)
    thumb.save(thumb_path, "WEBP", quality=slot.thumb_quality, method=6)

    print(f"{source.relative_to(ROOT)} -> {png_path.relative_to(ROOT)} {main.size}")
    print(f"{source.relative_to(ROOT)} -> {webp_path.relative_to(ROOT)} {main.size}")
    print(f"{source.relative_to(ROOT)} -> {thumb_path.relative_to(ROOT)} {thumb.size}")


def list_slots() -> None:
    print("Expected replacement source files:")
    for slot in SLOTS:
        names = ", ".join(f"{slot.source_name}{ext}" for ext in EXTENSIONS)
        print(f"- {slot.source_name}: {names}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build optimized portfolio image assets.")
    parser.add_argument("--strict", action="store_true", help="Fail if any slot source image is missing.")
    parser.add_argument("--list", action="store_true", help="List expected source image names and exit.")
    args = parser.parse_args()

    if args.list:
        list_slots()
        return 0

    Image = import_pillow()

    processed = 0
    missing: list[str] = []
    for slot in SLOTS:
        source = find_source(slot)
        if source is None:
            missing.append(slot.source_name)
            continue
        build_slot(Image, slot, source)
        processed += 1

    if missing:
        print("Missing source slots: " + ", ".join(missing))
        if args.strict:
            return 1

    if processed == 0:
        print(f"No replacement images found in {SOURCE_DIR.relative_to(ROOT)}.")
        list_slots()
    else:
        print(f"Processed {processed} image slot(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
