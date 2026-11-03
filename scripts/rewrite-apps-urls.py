#!/usr/bin/env python3
"""Point the copied apps site at https://bashfra.me/apps."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "apps"
APPS = "https://bashfra.me/apps"
LODGE = "https://bashfra.me/lodge"
DMG = "https://dl.bashfra.me/lodge/Lodge-1.0.dmg"
TEXT_SUFFIXES = {".html", ".css", ".js", ".md", ".svg", ".json", ".txt", ".yml", ".yaml"}
NOINDEX = re.compile(
    r"""\s*<meta\s+name=["']robots["']\s+content=["']noindex["']\s*/?>\s*""",
    re.IGNORECASE,
)
REFRESH = re.compile(
    r"""\s*<meta\s+http-equiv=["']refresh["'][^>]*>\s*""",
    re.IGNORECASE,
)
DMG_NEW_TAB = re.compile(
    r"""(href=["']""" + re.escape(DMG) + r"""["'])(?:\s+target=["']_blank["']|\s+rel=["']noopener["'])+""",
    re.IGNORECASE,
)


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return APPS + "/"
    return f"{APPS}/{rel}"


def rewrite_text(text: str) -> str:
    text = text.replace("https://bashcrandicoot.github.io/apps/", APPS + "/")
    text = text.replace("https://bashcrandicoot.github.io/apps", APPS)
    text = text.replace("https://bashcrandicoot.github.io/Lodge/", LODGE + "/")
    text = text.replace("https://bashcrandicoot.github.io/Lodge", LODGE)
    text = text.replace("https://bashfra.me/lodge-dmg/", DMG)
    text = text.replace("https://bashfra.me/lodge-dmg", DMG)
    text = NOINDEX.sub("\n", text)
    text = REFRESH.sub("\n", text)
    text = DMG_NEW_TAB.sub(r"\1", text)
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
    if 'name="twitter:image"' not in text:
        image = re.search(r'<meta property="og:image" content="([^"]+)">', text)
        if image:
            tag = f'  <meta name="twitter:image" content="{image.group(1)}">\n'
            card = '<meta name="twitter:card" content="summary_large_image">\n'
            if card in text:
                text = text.replace(card, card + tag, 1)
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
