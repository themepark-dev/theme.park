"""Check NPM's injected theme in Chromium/Firefox and save visual evidence.

Requires Playwright and its chromium/firefox browsers. Run after Compose and seed.py.
TP_THEME must match the theme currently injected by the container.
"""
import hashlib
import json
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
THEME = os.environ.get('TP_THEME', 'aquamarine')
OUT = ROOT / 'dev/artifacts/nginx-proxy-manager/707' / THEME
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:18084'
results = []


def color(page, variable):
    return page.evaluate('''variable => {
        const probe = document.createElement('i');
        probe.style.color = `var(${variable})`; document.body.append(probe);
        const value = getComputedStyle(probe).color; probe.remove(); return value;
    }''', variable)


def style(locator, property):
    value = locator.evaluate('(el,p)=>getComputedStyle(el).getPropertyValue(p)', property)
    return re.sub(r'rgba\((\d+, \d+, \d+), 1\)', r'rgb(\1)', value)


with sync_playwright() as playwright:
    for engine in ('chromium', 'firefox'):
        browser = getattr(playwright, engine).launch()
        for mode in ('light', 'dark'):
            for width, height in ((1440, 1000), (390, 844)):
                context = browser.new_context(viewport={'width': width, 'height': height}, color_scheme=mode)
                page = context.new_page()
                page.set_default_timeout(10000)
                loaded = {}
                page.on('response', lambda response: loaded.update({response.url.split('?')[0]: response.status}) if '/css/' in response.url else None)
                prefix = f'{engine}-{mode}-{width}'

                def shot(name):
                    page.wait_for_timeout(250)
                    page.screenshot(path=str(OUT / f'{prefix}-{name}.png'), full_page=True)

                page.goto(URL)
                page.locator('input[name=email]').wait_for()
                shot('login')
                page.locator('input[name=email]').fill('admin@example.com')
                page.locator('input[name=password]').fill(os.environ.get('NPM_DEV_PASSWORD', 'adminadmin'))
                page.get_by_role('button', name='Sign in', exact=True).click()
                page.get_by_text('0 Redirection Hosts', exact=True).wait_for()
                assert page.locator('html').get_attribute('data-bs-theme') == mode
                page.goto(URL + '/nginx/proxy')
                page.get_by_role('button', name='Add Proxy Host', exact=True).wait_for()
                expected = color(page, '--text')
                assert style(page.locator('.table tbody td').nth(2), 'color') == expected
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Page overflows horizontally'
                shot('table')
                add = page.get_by_role('button', name='Add Proxy Host', exact=True)
                add.hover(); page.wait_for_timeout(250)
                assert style(add, 'background-color') == color(page, '--button-color-hover')
                assert style(add, 'color') == color(page, '--button-text-hover')
                shot('hover')
                add.click()
                page.locator('.modal-content').wait_for()
                assert style(page.locator('.modal-body .card'), 'background-color') == 'rgba(0, 0, 0, 0)'
                assert style(page.locator('.modal-body .card'), 'color') == expected
                for selector, variable in (('.modal-content','--modal-bg-color'),('.modal-header','--modal-header-color'),('.modal-footer','--modal-footer-color')):
                    actual = page.locator(selector).evaluate('''(el,variable)=>{
                        const probe=document.createElement('i');probe.style.background=`var(${variable})`;el.append(probe);
                        const expected=getComputedStyle(probe);const actual=getComputedStyle(el);
                        const result={color:actual.backgroundColor===expected.backgroundColor,image:actual.backgroundImage===expected.backgroundImage};probe.remove();return result;
                    }''', variable)
                    assert all(actual.values()), (selector, actual)
                domain = page.locator('#domainNames input[role=combobox]')
                domain.fill('preview.example.test');page.keyboard.press('Enter')
                assert page.locator('.react-select__multi-value').count() == 1
                page.locator('#cachingEnabled').check();page.wait_for_timeout(650)
                assert style(page.locator('#cachingEnabled'), 'background-color') == color(page, '--button-color'), (page.locator('#cachingEnabled').evaluate('(x)=>x.outerHTML'), style(page.locator('#cachingEnabled'), 'background-color'),color(page, '--button-color'))
                page.locator('#forwardHost').fill('css')
                page.locator('#forwardPort').fill('8000')
                page.locator('#forwardHost').focus();page.wait_for_timeout(250)
                assert style(page.locator('#forwardHost'), 'border-top-color') == color(page, '--tblr-primary')
                shot('dialog')
                page.locator('.react-select__control').nth(1).click();page.wait_for_timeout(250)
                assert style(page.locator('.react-select__control').nth(1), 'border-top-color') == color(page, '--tblr-primary')
                shot('select');page.keyboard.press('Escape')
                page.get_by_role('tab', name='SSL', exact=True).click()
                assert page.locator('.modal input:disabled').count() > 0
                shot('ssl-disabled')
                page.locator('.modal a[title=Settings]').click()
                page.locator('.w-tc-editor textarea').fill('# local preview\nproxy_set_header X-Theme "preview";')
                assert style(page.locator('.w-tc-editor code'), 'color') == expected
                shot('editor')
                page.locator('.modal .btn-close').click()
                page.locator('.modal').wait_for(state='hidden')
                # Compare actual downloaded source, not a browser-only style prototype.
                base='http://127.0.0.1:18867/css/base/nginx-proxy-manager/nginx-proxy-manager-base.css'
                assert hashlib.sha256(page.request.get(base).body()).digest() == hashlib.sha256((ROOT/'css/base/nginx-proxy-manager/nginx-proxy-manager-base.css').read_bytes()).digest()
                for suffix in ('base/nginx-proxy-manager/nginx-proxy-manager-base.css','defaults/placeholders.css','defaults/transparent.css'):
                    assert loaded.get('http://127.0.0.1:18867/css/'+suffix) == 200, loaded
                assert any(url.endswith('/'+THEME+'.css') and code==200 for url,code in loaded.items()), loaded
                results.append({'browser':engine,'version':browser.version,'mode':mode,'viewport':[width,height],'theme':THEME,'checks':'passed'})
                print(prefix, 'passed', flush=True)
                context.close()
        browser.close()
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
