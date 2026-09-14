// Render the fixture's SVG artwork into images Jellyfin can scan.
const { firefox } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
    const browser = await firefox.launch();
    try {
        const page = await browser.newPage();
        const root = path.resolve(process.argv[2]);
        for (const directory of fs.readdirSync(root)) {
            for (const kind of ['poster', 'backdrop']) {
                const source = path.join(root, directory, kind + '.svg');
                await page.goto('file://' + source);
                await page.locator('svg').screenshot({ path: source.replace('.svg', '.png') });
            }
        }
    } finally {
        await browser.close();
    }
})().catch(error => { console.error(error); process.exitCode = 1; });
