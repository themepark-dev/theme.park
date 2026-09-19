"""Audit theme variable consumers with deliberately distinct values in real NPM.

The temporary palette is browser-only. Reload afterwards restores the injected
local theme. Screenshots complement the computed-style assertions.
"""
import json
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / 'artifacts/nginx-proxy-manager/707/variable-audit'
OUT.mkdir(parents=True, exist_ok=True)
PALETTE = {
    '--main-bg-color': 'linear-gradient(30deg, #102030, #304050) center/cover fixed',
    '--modal-bg-color': 'radial-gradient(ellipse at center, #304860, #182838) center/cover fixed',
    '--modal-header-color': 'linear-gradient(90deg, #403060, #283848) center/cover fixed',
    '--modal-footer-color': '#273941', '--drop-down-menu-bg': '#35475b',
    '--button-color': '#466078', '--button-color-hover': '#6c7e90',
    '--button-text': '#edf1f3', '--button-text-hover': '#ffedd0',
    '--accent-color': '150, 120, 200', '--accent-color-hover': 'rgba(180, 140, 220, .9)',
    '--link-color': '#abcdef', '--link-color-hover': '#fedcba',
    '--label-text-color': '#142536', '--text': '#d9e2ec',
    '--text-hover': '#f4f1de', '--text-muted': '#93a5b8',
}
records = []
with sync_playwright() as p:
    for engine in ('chromium', 'firefox'):
        browser = getattr(p, engine).launch()
        for mode in ('light', 'dark'):
            page = browser.new_page(viewport={'width':1440, 'height':1000},color_scheme=mode)
            page.goto('http://127.0.0.1:18084')
            page.locator('input[name=email]').fill('admin@example.com')
            page.locator('input[name=password]').fill(os.environ.get('NPM_DEV_PASSWORD','adminadmin'))
            page.get_by_role('button',name='Sign in',exact=True).click()
            page.get_by_text('0 Redirection Hosts',exact=True).wait_for()
            prefix = f'{engine}-{mode}'

            def palette():
                page.add_style_tag(content=':root {'+';'.join(k+':'+v for k,v in PALETTE.items())+'}')
                page.mouse.move(0,0);page.wait_for_timeout(650)

            def check(locator, prop, variable, label):
                result = locator.evaluate('''(el,args)=>{
                    const [prop,variable] = args;
                    const probe=document.createElement('i');probe.style.setProperty(prop.startsWith('background-')?'background':prop,`var(${variable})`);document.body.append(probe);
                    const expected=getComputedStyle(probe).getPropertyValue(prop), actual=getComputedStyle(el).getPropertyValue(prop);probe.remove();return {expected,actual};
                }''',[prop,variable])
                norm=lambda x:re.sub(r'rgba\((\d+, \d+, \d+), 1\)',r'rgb(\1)',x)
                assert norm(result['actual'])==norm(result['expected']), (prefix,label,prop,variable,result)
                records.append({'case':prefix,'consumer':label,'property':prop,'variable':variable,**result})

            def hover(locator):
                locator.hover();page.wait_for_timeout(650)

            def shot(name):
                page.wait_for_timeout(300);page.screenshot(path=str(OUT/f'{prefix}-{name}.png'),full_page=True)

            palette()
            check(page.locator('body'),'background-image','--main-bg-color','page')
            for name,loc in [('navigation',page.get_by_role('link',name='Access Lists',exact=True)),('footer',page.get_by_role('link',name='Fork me on Github',exact=True)),('dashboard',page.get_by_role('link',name='2 Proxy Hosts',exact=True))]:
                page.mouse.move(0,0);page.wait_for_timeout(350)
                check(loc,'color','--link-color',name)
                hover(loc);check(loc,'color','--link-color-hover',name+' hover');shot(name+'-hover')
                page.mouse.move(0,0);page.keyboard.press('Tab');loc.focus();page.wait_for_timeout(350)
                check(loc,'color','--link-color-hover',name+' focus')
                page.locator('body').click(position={'x':1,'y':200})
            page.goto('http://127.0.0.1:18084/nginx/proxy');page.get_by_role('button',name='Add Proxy Host',exact=True).wait_for();palette()
            add=page.get_by_role('button',name='Add Proxy Host',exact=True)
            check(add,'background-color','--button-color','primary button');check(add,'color','--button-text','primary button')
            hover(add);check(add,'background-color','--button-color-hover','primary hover');check(add,'color','--button-text-hover','primary hover')
            add.click();page.locator('.modal-content').wait_for();page.wait_for_timeout(400)
            for sel,var in [('.modal-content','--modal-bg-color'),('.modal-header','--modal-header-color'),('.modal-footer','--modal-footer-color')]:
                check(page.locator(sel),'background-image',var,sel);check(page.locator(sel),'background-color',var,sel)
            check(page.locator('.modal .form-label').first,'color','--text','form label')
            check(page.locator('.modal h4'),'color','--text-hover','heading')
            check(page.locator('.react-select__placeholder').first,'color','--text-muted','select placeholder')
            domain=page.locator('#domainNames input[role=combobox]');domain.fill('variables.example.test');page.keyboard.press('Enter');page.mouse.move(0,0)
            # accent-color is an RGB triplet, so its consumer needs rgb().
            chip=page.locator('.react-select__multi-value')
            assert chip.evaluate('(el)=>getComputedStyle(el).backgroundColor')=='rgb(150, 120, 200)'
            records.append({'case':prefix,'consumer':'domain chip background','variable':'--accent-color','actual':'rgb(150, 120, 200)'})
            check(page.locator('.react-select__multi-value__label'),'color','--label-text-color','domain label')
            remove=page.locator('.react-select__multi-value__remove');hover(remove);check(remove,'background-color','--accent-color-hover','domain remove hover')
            shot('labels')
            field=page.locator('#forwardHost');field.focus();page.wait_for_timeout(400);check(field,'color','--text-hover','focused input')
            page.locator('.react-select__control').nth(1).click();page.wait_for_timeout(400)
            check(page.locator('.react-select__menu'),'background-color','--drop-down-menu-bg','select menu');shot('menu')
            page.keyboard.press('Escape');page.get_by_role('tab',name='SSL',exact=True).click();shot('radial-body')
            page.locator('.modal a[title=Settings]').click()
            page.locator('.w-tc-editor textarea').fill('# preview\nproxy_set_header X-Theme test;')
            check(page.locator('.w-tc-editor code'),'color','--text','editor plain text')
            check(page.locator('.w-tc-editor .token.comment'),'color','--text-muted','editor comment')
            check(page.locator('.w-tc-editor .token.keyword'),'color','--text-hover','editor keyword')
            assert page.locator('.w-tc-editor textarea').evaluate('(el)=>getComputedStyle(el).webkitTextFillColor')=='rgba(0, 0, 0, 0)'
            shot('editor')
            page.locator('.modal .btn-close').click();page.locator('.modal').wait_for(state='hidden')
            # Reload removes the diagnostic palette and restores real injection.
            page.reload();page.get_by_role('button',name='Add Proxy Host',exact=True).wait_for()
            page.close()
        browser.close()
(OUT/'results.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(records)} variable consumer checks passed')
