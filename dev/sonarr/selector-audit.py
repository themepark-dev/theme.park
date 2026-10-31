#!/usr/bin/env python3
"""Check theme.park class selectors against the class names in a Servarr UI build.

Usage:
    python3 -I dev/sonarr/selector-audit.py css/base/sonarr/sonarr-base.css \
        dev/artifacts/sonarr/v5-audit/ui-v4 dev/artifacts/sonarr/v5-audit/ui-v5

The first argument is the entry stylesheet. Its local @import chain is followed.
Each further argument is a copy of an app's UI directory, for example from
`docker compose cp v5:/app/sonarr/bin/UI ...`. The script collects class names
from the build's CSS files and reports which attribute selectors such as
[class*="PageHeader-logo-"] match at least one class in each build.

Matching uses individual class names, not rendered class attributes, so a
selector that matches here can still miss the elements on a given screen.
Confirm important results in the browser.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMPORT_RE = re.compile(r'@import\s+url\(["\']?(/[^"\')]+)["\']?\)')
ATTR_RE = re.compile(r'\[class\s*([*^$]?)=\s*["\']?([^"\'\]]+)["\']?\s*\]')
CLASS_RE = re.compile(r"\.(-?[_a-zA-Z][_a-zA-Z0-9-]*)")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def stylesheet_chain(entry, seen=None):
    seen = seen if seen is not None else []
    path = Path(entry).resolve()
    if path in seen or not path.exists():
        return seen
    seen.append(path)
    for target in IMPORT_RE.findall(path.read_text(encoding="utf-8")):
        stylesheet_chain(ROOT / target.lstrip("/"), seen)
    return seen


def build_classes(ui_dir):
    classes = set()
    for css in Path(ui_dir).rglob("*.css"):
        text = COMMENT_RE.sub("", css.read_text(encoding="utf-8", errors="replace"))
        classes.update(CLASS_RE.findall(text))
    return classes


def matches(op, value, classes):
    if op == "*":
        return any(value in c for c in classes)
    if op == "^":
        return any(c.startswith(value) for c in classes)
    if op == "$":
        return any(c.endswith(value) for c in classes)
    return value in classes


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    builds = {Path(d).name: build_classes(d) for d in argv[2:]}
    names = list(builds)
    print("file\tselector\t" + "\t".join(names))
    totals = {n: 0 for n in names}
    count = 0
    for sheet in stylesheet_chain(argv[1]):
        text = COMMENT_RE.sub("", sheet.read_text(encoding="utf-8"))
        selectors = sorted(set(ATTR_RE.findall(text)), key=lambda s: s[1])
        for op, value in selectors:
            count += 1
            hits = []
            for n in names:
                ok = matches(op, value, builds[n])
                totals[n] += ok
                hits.append("yes" if ok else "-")
            print(f"{sheet.relative_to(ROOT)}\t[class{op}=\"{value}\"]\t" + "\t".join(hits))
    print("\nmatched\t" + "\t".join(f"{n}: {totals[n]}/{count}" for n in names))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
