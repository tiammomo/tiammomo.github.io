#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str, str]] = []
        self.json_ld: list[str] = []
        self._in_json_ld = False
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value for key, value in attrs if value is not None}
        for key in ("href", "src", "srcset"):
            if key in attr_map:
                self.refs.append((tag, key, attr_map[key]))
        if tag == "script" and attr_map.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_parts))
            self._in_json_ld = False


def is_external(ref: str) -> bool:
    return ref.startswith(("http://", "https://", "mailto:", "tel:", "#")) or ref == "/"


def strip_ref(ref: str) -> str:
    return ref.split("#", 1)[0].split("?", 1)[0]


def srcset_urls(value: str) -> list[str]:
    urls: list[str] = []
    for item in value.split(","):
        bits = item.strip().split()
        if bits:
            urls.append(bits[0])
    return urls


def check_local_ref(page: Path, ref: str, errors: list[str]) -> None:
    if is_external(ref):
        return
    clean = strip_ref(ref)
    if not clean:
        return
    target = (page.parent / clean).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        errors.append(f"{page.relative_to(ROOT)}: ref escapes project: {ref}")
        return
    if not target.exists():
        errors.append(f"{page.relative_to(ROOT)}: missing {ref} -> {target.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []

    html_files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "projects").glob("*.html"))
    for path in html_files:
        parser = RefParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for tag, key, ref in parser.refs:
            refs = srcset_urls(ref) if key == "srcset" else [ref]
            for item in refs:
                check_local_ref(path, item, errors)
        for index, payload in enumerate(parser.json_ld, start=1):
            try:
                json.loads(payload)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid JSON-LD #{index}: {exc}")

    try:
        json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"site.webmanifest: {exc}")

    try:
        ET.parse(ROOT / "sitemap.xml")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"sitemap.xml: {exc}")

    try:
        projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
        if not isinstance(projects, list):
            errors.append("data/projects.json: expected a list")
        else:
            for index, project in enumerate(projects):
                label = project.get("id", f"#{index}") if isinstance(project, dict) else f"#{index}"
                if not isinstance(project, dict):
                    errors.append(f"data/projects.json:{label}: expected object")
                    continue
                for field in ("id", "name", "status", "categories", "image", "summary", "tags"):
                    if field not in project:
                        errors.append(f"data/projects.json:{label}: missing {field}")
                image = project.get("image", {})
                if isinstance(image, dict):
                    ref = image.get("png")
                    if isinstance(ref, str):
                        check_local_ref(ROOT / "index.html", ref, errors)
                    else:
                        errors.append(f"data/projects.json:{label}: missing image.png")
                    ref = image.get("webp")
                    if isinstance(ref, str) and ref:
                        check_local_ref(ROOT / "index.html", ref, errors)
                for field in ("caseUrl", "githubUrl"):
                    ref = project.get(field)
                    if isinstance(ref, str):
                        check_local_ref(ROOT / "index.html", ref, errors)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"data/projects.json: {exc}")

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    for match in re.finditer(r"url\(['\"]?([^'\")]+)['\"]?\)", css):
        ref = match.group(1)
        if not is_external(ref):
            target = (ROOT / ref).resolve()
            if not target.exists():
                errors.append(f"styles.css: missing {ref}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"validated {len(html_files)} HTML files and site metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
