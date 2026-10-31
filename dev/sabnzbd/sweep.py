"""Screenshot SABnzbd's main views, modals, dropdowns and Config pages.

Usage: sweep.py OUTDIR LABEL [--states a,b,c] [--width W --height H] [--full-page]

Each state is saved as OUTDIR/LABEL-<state>.png. For dark themes the script
also lists visible elements with a light opaque background or a bright border,
which is how unmapped Glitter colors usually show up. Light themes produce
false positives in that list, so read the screenshots too.
"""

import argparse
import json

from playwright.sync_api import sync_playwright

BASE = "http://localhost:18080"

LIGHT_PATCHES = """() => {
  const lum = c => { const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null;
    const [r, g, b, a = 1] = m[1].split(',').map(Number); return {l: (0.2126*r + 0.7152*g + 0.0722*b) / 255, a}; };
  const name = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') +
    (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\\s+/).join('.') : '');
  const out = [];
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect();
    if (r.width < 2 || r.height < 2 || r.bottom < 0 || r.top > innerHeight) continue;
    const cs = getComputedStyle(e);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const bg = lum(cs.backgroundColor);
    if (bg && bg.a >= 0.5 && bg.l > 0.75) out.push(['bg', name(e), cs.backgroundColor]);
    for (const side of ['Top', 'Bottom', 'Left', 'Right']) {
      const w = parseFloat(cs['border' + side + 'Width']); const c = lum(cs['border' + side + 'Color']);
      if (w >= 1 && cs['border' + side + 'Style'] !== 'none' && c && c.a >= 0.5 && c.l > 0.85) {
        out.push(['border-' + side.toLowerCase(), name(e), w + 'px ' + cs['border' + side + 'Color']]); break; }
    }
  }
  return out;
}"""


def modal(selector: str, tab: str | None = None) -> str:
    show = f"$('{selector}').modal('show');"
    if tab:
        show += f" $('a[href=\"{tab}\"]').tab('show');"
    return show


def files_modal() -> str:
    return ("[...document.querySelectorAll('a')].find(a => "
            "(a.getAttribute('data-bind') || '').includes('showFiles')).click();")


# name -> (url path, JavaScript to run after load or None)
STATES = {
    # Glitter's non-tabbed layout: warnings, queue and history on one page.
    "overview": ("/", None),
    "queue": ("/", "$('a[href=\"#queue-tab\"]').click();"),
    "history": ("/", "$('a[href=\"#history-tab\"]').click();"),
    "warnings": ("/", "$('a[href=\"#queue-messages\"]').click();"),
    "main-menu": ("/", "$('a[aria-label][data-toggle=\"dropdown\"][onclick]').last().dropdown('toggle');"),
    "pause-menu": ("/", "$('.navbar-btn.dropdown-toggle').first().dropdown('toggle');"),
    "speed-menu": ("/", "$('.navbar-speed').dropdown('toggle');"),
    "history-details": ("/", "$('a[href=\"#history-tab\"]').click(); setTimeout(() => $('.history-table a[data-toggle=\"dropdown\"]').first().click(), 300);"),
    "queue-details": ("/", "$('a[href=\"#queue-tab\"]').click(); setTimeout(() => $('.queue-table a[data-toggle=\"dropdown\"][aria-label]').first().click(), 300);"),
    "queue-multiedit": ("/", "$('a[href=\"#queue-tab\"]').click(); setTimeout(() => $('.queue .multioperations-selector, .queue [data-bind*=\"isMultiEditing\"] input').first().click(), 300); $('.queue .hover-button.glyphicon-tasks, .queue a[data-bind*=\"MultiEdit\"]').first().click();"),
    "modal-add": ("/", modal("#modal-add-nzb")),
    "modal-status": ("/", modal("#modal-options", "#options-status")),
    "modal-connections": ("/", modal("#modal-options", "#options_connections")),
    "modal-orphans": ("/", modal("#modal-options", "#options-orphans")),
    "modal-interface": ("/", modal("#modal-options", "#options-interface")),
    "modal-help": ("/", modal("#modal-help")),
    "modal-files": ("/", "$('a[href=\"#queue-tab\"]').click(); " + files_modal()),
    "modal-custom-pause": ("/", modal("#modal-custom-pause")),
    "modal-purge-history": ("/", modal("#modal-purge-history")),
    "config": ("/config/", None),
    "config-general": ("/config/general/", None),
    "config-folders": ("/config/folders/", None),
    "config-server": ("/config/server/", None),
    "config-categories": ("/config/categories/", None),
    "config-switches": ("/config/switches/", None),
    "config-sorting": ("/config/sorting/", None),
    "config-notify": ("/config/notify/", None),
    "config-scheduling": ("/config/scheduling/", None),
    "config-rss": ("/config/rss/", None),
    "config-special": ("/config/special/", None),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("outdir")
    parser.add_argument("label")
    parser.add_argument("--states", default=",".join(STATES))
    parser.add_argument("--width", type=int, default=1400)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--full-page", action="store_true")
    args = parser.parse_args()

    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(BASE + "/", wait_until="networkidle")
        for state in args.states.split(","):
            path, script = STATES[state]
            page.evaluate(f"localStorage.setItem('displayTabbed', '{str(state != 'overview').lower()}')")
            page.goto(BASE + path, wait_until="networkidle")
            page.wait_for_timeout(1200)
            if script:
                page.evaluate(script)
                page.wait_for_timeout(1200)
            page.mouse.move(args.width - 2, args.height - 2)
            page.screenshot(path=f"{args.outdir}/{args.label}-{state}.png", full_page=args.full_page)
            report[state] = page.evaluate(LIGHT_PATCHES)
        browser.close()
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
