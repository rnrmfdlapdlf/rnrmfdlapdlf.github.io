#!/usr/bin/env python3
"""Reorder the Korean patch cards in index.html by latest release date (newest first).

Only cards with data-category="patch" move, and only among the slots they already
occupy. Cards of other categories stay exactly where they are. Patch repositories
without a published release keep their relative order after the ones that have one.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "rnrmfdlapdlf")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

CARD_RE = re.compile(
    r'^      <!-- (?P<repo>[\w.-]+) -->\n'
    r'      <article class="project-card" id="(?P=repo)" data-category="(?P<category>[\w-]+)".*?\n'
    r'      </article>\n',
    re.M | re.S,
)


def latest_release_date(repo: str) -> str | None:
    """Return the published_at of the latest (non-draft, non-prerelease) release, or None."""
    request = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{repo}/releases/latest",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "sort-patch-cards"},
    )
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response).get("published_at")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")
    cards = list(CARD_RE.finditer(text))
    patch_cards = [card for card in cards if card.group("category") == "patch"]
    if not patch_cards:
        print("no patch cards found; index.html structure may have changed", file=sys.stderr)
        return 1

    dated = []
    for position, card in enumerate(patch_cards):
        repo = card.group("repo")
        published = latest_release_date(repo)
        print(f"{repo}: {published or 'no release'}")
        dated.append((published, position, card))

    # Newest first; repositories without a release go last, keeping their original order.
    with_release = sorted((d for d in dated if d[0]), key=lambda d: (d[0], -d[1]), reverse=True)
    without_release = [d for d in dated if not d[0]]
    ordered = [d[2].group(0) for d in with_release + without_release]

    # Put the sorted card blocks back into the slots the patch cards occupied.
    pieces = []
    cursor = 0
    for slot, block in zip(patch_cards, ordered):
        pieces.append(text[cursor:slot.start()])
        pieces.append(block)
        cursor = slot.end()
    pieces.append(text[cursor:])
    new_text = "".join(pieces)

    if new_text == text:
        print("order unchanged")
        return 0
    with INDEX.open("w", encoding="utf-8", newline="") as handle:
        handle.write(new_text)
    print("index.html reordered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
