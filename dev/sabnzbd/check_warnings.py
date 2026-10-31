"""Screenshot the Warnings tab and record row colors. Usage: check_warnings.py OUTDIR LABEL [WIDTH HEIGHT]"""
import json, sys
from playwright.sync_api import sync_playwright

outdir, label = sys.argv[1], sys.argv[2]
w, h = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1912, 400)
ROWS = """() => [...document.querySelectorAll('#queue-messages tbody tr')].filter(r => r.offsetHeight).map(r => {
  const td = r.querySelector('td.table-messages-label'); return {text: r.innerText.trim().slice(0, 40),
  bg: getComputedStyle(r).backgroundColor, color: td && getComputedStyle(td.querySelector('.queue-message-text')).color}; })"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("http://localhost:18080/", wait_until="networkidle")
    pg.evaluate("localStorage.setItem('displayTabbed', 'true')")
    pg.reload(wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.click("a[href='#queue-messages']")
    pg.mouse.move(w - 5, h - 5); pg.wait_for_timeout(500)
    res = {"rest": pg.evaluate(ROWS)}
    pg.screenshot(path=f"{outdir}/{label}-warnings-{w}.png")
    rows = pg.locator("#queue-messages td.table-messages-label")
    if rows.count():
        rows.first.hover(); pg.wait_for_timeout(300)
        res["hover-first"] = pg.evaluate(ROWS)
        pg.screenshot(path=f"{outdir}/{label}-warnings-hover-{w}.png")
    pg.mouse.move(w - 5, h - 5)
    # Every visible striped .table row on the page, with its background.
    res["tables"] = pg.evaluate("""() => [...document.querySelectorAll('table.table')].map(t => ({cls: t.className,
      rows: [...t.querySelectorAll(':scope > tbody > tr')].filter(r => r.offsetHeight).slice(0,4).map(r => getComputedStyle(r).backgroundColor)}))""")
    print(json.dumps(res, indent=1))
    b.close()
