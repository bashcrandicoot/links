#!/usr/bin/env python3
"""Point the copied Lodge docs at https://bashfra.me/lodge."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "lodge"
BASE = "https://bashfra.me/lodge"
TEXT_SUFFIXES = {".html", ".css", ".js", ".md", ".svg", ".json", ".txt", ".yml", ".yaml"}
NOINDEX = re.compile(
    r"""\s*<meta\s+name=["']robots["']\s+content=["']noindex["']\s*/?>\s*""",
    re.IGNORECASE,
)


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE + "/"
    return f"{BASE}/{rel}"


DMG = "https://dl.bashfra.me/lodge/Lodge-1.0.dmg"


def rewrite_text(text: str) -> str:
    text = text.replace("https://bashcrandicoot.github.io/Lodge/", BASE + "/")
    text = text.replace("https://bashcrandicoot.github.io/Lodge", BASE)
    text = text.replace("https://bashfra.me/lodge-dmg/", DMG)
    text = text.replace("https://bashfra.me/lodge-dmg", DMG)
    text = NOINDEX.sub("\n", text)
    return text


def ensure_urls(text: str, url: str) -> str:
    if 'rel="canonical"' not in text:
        needle = '<meta name="color-scheme" content="dark">\n'
        tag = f'  <link rel="canonical" href="{url}">\n'
        if needle in text:
            text = text.replace(needle, needle + tag, 1)
        else:
            text = text.replace("</head>", tag + "</head>", 1)
    if 'property="og:url"' not in text:
        canon = f'  <link rel="canonical" href="{url}">\n'
        tag = f'  <meta property="og:url" content="{url}">\n'
        if canon in text:
            text = text.replace(canon, canon + tag, 1)
        else:
            text = text.replace("</head>", tag + "</head>", 1)
    return text


def main() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        original = path.read_text(encoding="utf-8")
        updated = rewrite_text(original)
        if path.suffix.lower() == ".html":
            updated = ensure_urls(updated, page_url(path))
        if updated != original:
            path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
