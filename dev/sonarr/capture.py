#!/usr/bin/env python3
"""Screenshot the main Sonarr screens of the dev/sonarr instances.

Needs Python Playwright with Chromium, installed outside the repository:
    uv venv /tmp/sonarr-theme-tools
    VIRTUAL_ENV=/tmp/sonarr-theme-tools uv pip install playwright
    /tmp/sonarr-theme-tools/bin/playwright install chromium

Usage, from the repository root:
    /tmp/sonarr-theme-tools/bin/python -I dev/sonarr/capture.py OUT_DIR [options]

Options:
    --versions v4,v5    services to capture (default: both)
    --native            block the theme.park CSS host to show the app's own styles
    --scheme dark       prefers-color-scheme for the browser (dark or light)
    --theme aquamarine  swap the injected theme option at request time
    --community         the --theme name is a community theme option
    --pages a,b         capture only these pages; "none" skips them, "extra"
                        adds statistics, settings and system subpages
    --interactions      also open menus, dropdowns, tooltips and modals
    --width 1440 --height 900
    --host NAME         host name for the apps and CSS host (default: $DEV_HOST or localhost)

Each screenshot is OUT_DIR/<version>-<page>.png. OUT_DIR/report.json lists the
stylesheets each page loaded, so you can confirm the local theme.park files and
their imports arrived. Keep OUT_DIR under the ignored dev/artifacts/ directory.
"""

import argparse
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

PORTS = {"v4": 18989, "v5": 18990}
PAGES = [
    ("series", "/"),
    ("series-details", "/series/breaking-bad"),
    ("calendar", "/calendar"),
    ("queue", "/activity/queue"),
    ("history", "/activity/history"),
    ("missing", "/wanted/missing"),
    ("add-new", "/add/new?term=the%20office"),
    ("settings", "/settings"),
    ("settings-media", "/settings/mediamanagement"),
    ("settings-profiles", "/settings/profiles"),
    ("settings-ui", "/settings/ui"),
    ("system-status", "/system/status"),
    ("system-logs", "/system/events"),
]
# More screens, captured with --pages extra or by name.
EXTRA_PAGES = [
    ("statistics", "/statistics"),
    ("blocklist", "/activity/blocklist"),
    ("library-import", "/add/import"),
    ("settings-quality", "/settings/quality"),
    ("settings-customformats", "/settings/customformats"),
    ("settings-indexers", "/settings/indexers"),
    ("settings-downloadclients", "/settings/downloadclients"),
    ("settings-general", "/settings/general"),
    ("settings-tags", "/settings/tags"),
    ("system-tasks", "/system/tasks"),
    ("system-backups", "/system/backups"),
    ("system-updates", "/system/updates"),
    ("system-logfiles", "/system/logs/files"),
]


def login(page, base):
    page.goto(f"{base}/login")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('button[type="submit"]')
    page.wait_for_url(lambda u: "/login" not in u)


def settle(page):
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(700)


def sheets(page):
    return page.evaluate(
        """() => [...document.styleSheets].map(s => {
            let rules = null;
            try { rules = s.cssRules.length } catch (e) {}
            return {href: s.href, rules};
        }).filter(s => s.href)"""
    )


def interactions(page, base, out, version, report):
    """Open menus, dropdowns and modals that the page captures miss."""
    steps = []

    def shot(name, action):
        try:
            action()
            page.wait_for_timeout(700)
            page.screenshot(path=out / f"{version}-{name}.png")
            steps.append(name)
        except Exception as exc:  # keep going; record what failed
            steps.append(f"{name}: FAILED {str(exc).splitlines()[0]}")
        page.keyboard.press("Escape")
        page.mouse.click(5, 5)

    page.goto(base + "/")
    settle(page)
    if page.viewport_size["width"] <= 768:
        shot("sidebar-open", lambda: page.locator('[class*="PageHeader-module_sidebarToggle_"]').click())
    shot("menu-view", lambda: page.locator('[class*="ToolbarMenuButton-module_menuButton_"]', has_text="View").click())
    def table():
        page.locator('[class*="ToolbarMenuButton-module_menuButton_"]', has_text="View").click()
        page.wait_for_timeout(300)
        page.get_by_role("menuitem", name="Table").or_(page.get_by_text("Table", exact=True)).first.click()

    shot("series-table", table)
    shot("header-search", lambda: page.locator('[class*="SeriesSearchInput-module_input_"]').fill("s"))

    page.goto(base + "/series/breaking-bad")
    settle(page)

    def episode():
        page.locator('[class*="SeriesDetailsSeason-module_expandButton_"]').first.click()
        page.wait_for_timeout(500)
        page.locator('[class*="EpisodeTitleLink-module_link_"]').first.click()

    shot("modal-episode", episode)
    page.goto(base + "/series/breaking-bad")
    settle(page)

    def select():
        page.get_by_role("button", name="Edit").first.click()
        page.wait_for_timeout(700)
        page.locator('[class*="ModalBody"] [class*="EnhancedSelectInput-module_enhancedSelect_"]').nth(1).click()

    shot("modal-select-open", select)
    page.goto(base + "/series/breaking-bad")
    settle(page)
    shot("tooltip-season", lambda: page.locator('[class*="SeriesDetailsSeason-module_seasonStats_"]').first.hover())

    page.goto(base + "/calendar")
    settle(page)
    shot("calendar-month", lambda: page.get_by_role("button", name="Month").click())
    report[f"{version}-interactions"] = steps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--versions", default="v4,v5")
    ap.add_argument("--native", action="store_true")
    ap.add_argument("--theme", help="swap the injected theme option for this one")
    ap.add_argument("--community", action="store_true", help="--theme is a community theme")
    ap.add_argument("--pages", help="comma-separated page names to capture (default: all, 'none' for none)")
    ap.add_argument("--interactions", action="store_true", help="also open menus, dropdowns and modals")
    ap.add_argument("--scheme", default="dark", choices=["dark", "light"])
    ap.add_argument("--host", default=os.environ.get("DEV_HOST", "localhost"))
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report = {"args": vars(args)}
    css_host = f"http://{args.host}:18877"
    wanted = None if not args.pages else set(args.pages.split(","))
    if wanted and "extra" in wanted:
        wanted |= {name for name, _ in EXTRA_PAGES}
    pages = [pg for pg in PAGES + EXTRA_PAGES if (wanted is None and pg in PAGES) or (wanted and pg[0] in wanted)]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        report["browser"] = f"chromium {browser.version}"
        for version in args.versions.split(","):
            base = f"http://{args.host}:{PORTS[version]}"
            ctx = browser.new_context(
                viewport={"width": args.width, "height": args.height},
                color_scheme=args.scheme,
            )
            if args.native:
                ctx.route(f"{css_host}/**", lambda route: route.abort())
            elif args.theme:
                kind = "community-theme-options" if args.community else "theme-options"
                target = f"{css_host}/css/{kind}/{args.theme}.css"
                ctx.route(f"{css_host}/css/*theme-options/*.css", lambda route: route.continue_(url=target))
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            failed = []
            page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if css_host in r.url and r.status >= 400 else None)

            page.goto(f"{base}/login")
            settle(page)
            if wanted is None or "login" in wanted:
                page.screenshot(path=out / f"{version}-login.png")
            login(page, base)

            for name, path in pages:
                page.goto(base + path)
                settle(page)
                page.screenshot(path=out / f"{version}-{name}.png")
                report[f"{version}-{name}"] = {"url": page.url, "sheets": sheets(page)}

            if wanted is None or "modal-edit-series" in wanted:
                page.goto(base + "/series/breaking-bad")
                settle(page)
                edit = page.get_by_role("button", name="Edit")
                if edit.count():
                    edit.first.click()
                    page.wait_for_timeout(900)
                    page.screenshot(path=out / f"{version}-modal-edit-series.png")
            if args.interactions:
                interactions(page, base, out, version, report)
            report[f"{version}-errors"] = errors
            report[f"{version}-css-failures"] = failed
            ctx.close()
        browser.close()

    (out / "report.json").write_text(json.dumps(report, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
