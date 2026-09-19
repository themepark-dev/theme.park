# Local Jellyfin theme development

This fixture is for [issue #724](https://github.com/themepark-dev/theme.park/issues/724),
which contains only the title "Jellyfin 12 update?". It does not identify a theme,
browser, injection method, or specific broken screen.

The target is stable Jellyfin Server and Web 12.0, released September 8, 2026.
The official `jellyfin/jellyfin:12.0` image was tested at digest
`sha256:baba630419915985442f315f08b0cf46d9f4c8a0cc4bd38e94a6d35751dd5ef5`.
The maintainer does not require older-release compatibility for this refresh.

## Start

The optional sample generator needs Python, Docker, Node, and Playwright Firefox.
Keep browser dependencies outside the checkout:

```sh
npm install --prefix /tmp/themepark-browser playwright
/tmp/themepark-browser/node_modules/.bin/playwright install firefox
NODE_PATH=/tmp/themepark-browser/node_modules python3 dev/jellyfin/seed-media.py
docker compose -f dev/jellyfin/compose.yaml up -d
```

Wait for `http://localhost:18086/System/Info/Public` to return JSON, then run:

```sh
python3 dev/jellyfin/setup.py
```

The setup script completes the first-run wizard only on an unconfigured instance.
It adds a Sample Movies library if missing and installs Aquamarine only if the
Custom CSS setting is empty. It does not reset an existing profile or theme.
New fixtures use `admin` / `admin`. The existing review instance retains
`themepark` / `themepark-local`; it predates the shared login convention. To rerun
setup there, set `JELLYFIN_DEV_USER=themepark` and
`JELLYFIN_DEV_PASSWORD=themepark-local`. Jellyfin
12 requires a nonempty initial password. Remote access is enabled for Docker's
bridge connection, but only the loopback HTTP port is published. Automatic port
mapping is disabled.

| Address | Purpose |
| --- | --- |
| http://localhost:18086/web/ | Jellyfin UI. |
| http://localhost:18087/web/ | Nginx injection, including the dashboard. |
| http://localhost:18869 | Local CSS and resources. |

The generator creates six fictional movies with SVG artwork rendered to PNG,
local NFO metadata, and a short test-pattern video. Movie metadata and image
fetchers are disabled. Media is mounted read-only. Generated files stay in
ignored `dev/artifacts/jellyfin/724/media`. Do not rerun the generator during
maintainer review; it replaces the sample files.

## Injection

Use **Dashboard > Branding > Custom CSS code** in Jellyfin 12:

```css
@import url("http://localhost:18869/css/base/jellyfin/jellyfin-base.css");
@import url("http://localhost:18869/css/theme-options/aquamarine.css");
```

Edit the source stylesheet and refresh. The local CSS server disables caching.
These imports follow the app's built-in Custom CSS method. Generated theme URLs
are not needed for source development.

Jellyfin 12 mounts its `CustomCss` component in the modern and legacy client
layouts, but not the admin dashboard layout. Opening `/web/#/dashboard` removes
the injected style element. The direct port therefore keeps the native dashboard
theme. The docs' older
**General > Branding** path also needs updating to the separate Branding page.

### Subfiltering for the dashboard

Open http://localhost:18087/web/#/dashboard to include admin pages. The nginx
service follows the [subfiltering guide](https://docs.theme-park.dev/setup/#nginx).
It inserts the base stylesheet and Aquamarine links before `</head>`, once per
HTML response. It requests uncompressed HTML under `/web/`. API, media, and
WebSocket requests use a separate location without injection. No CSP change
was needed. The original port 18086 stays available for built-in CSS comparisons.

The injected links survive navigation between home and the dashboard. The
fixture retains its existing Branding imports so the direct port stays themed.
This means the client pages load the same theme through both methods on the
proxy. Keep both theme choices aligned; for a deployment using only
subfiltering, omit the duplicate Branding imports. Do not clear a maintainer's
settings during review. Dashboard checks load only the proxy's two links.

Change the theme-option URL in `nginx.conf` to switch the proxy theme, then run:

```sh
docker compose -f dev/jellyfin/compose.yaml exec proxy nginx -t
docker compose -f dev/jellyfin/compose.yaml exec proxy nginx -s reload
```

The published proxy port and CSS URLs are for local development. They do not
configure a public deployment or a Jellyfin base URL.

## Styling hooks

Jellyfin 12 uses `--jf-palette-*` variables in both Material UI and older client
components. Inspect `src/themes/_base/theme.ts` and `_theme.scss` in the matching
web release. Use public `Mui*` component/state classes rather than generated
`css-*` names. Existing legacy rules still serve detail pages and action sheets.

Keep palette background variables color-only. Apply full theme backgrounds to
page, app bar, drawer, and dialog elements so gradient options work. Popovers
need an opaque dropdown background to cover the content behind them. Dialog
headers and actions use their own theme variables.

MUI puts channel variables inside `rgba(channel / opacity)`. theme.park's accent
is comma-separated, so copying it directly into a channel breaks selected and
focus backgrounds. The mapping uses relative RGB channels, such as
`from rgb(var(--accent-color)) r g b`. Test the resulting selected/hover colors
in the browser and after minification. This requires a browser with relative
RGB color support.

Exclude `.MuiButtonBase-root` from the old global anchor override. MUI uses
anchors for navigation and menu items; forcing every anchor to the link color
otherwise overrides their component states. Preserve semantic error/status
palettes when mapping primary and secondary controls.

The dashboard's Material React Table components calculate background colors
from the JavaScript theme instead of the overridden CSS palette. Devices and
Activity therefore kept native dark table backgrounds even after injection.
Scoped table rules cover the shell, toolbars, rows, cells, and menu lists. The
column menu also sets a native background on its inner list, covering the themed
popover beneath it. Keep sticky
headers and pinned cells opaque so scrolling content does not show through.
Device artwork fallback colors and severity badges remain app-defined.

Users cards and the permission groups in Profile, Parental Control, and Add
User still use legacy `.visualCardBox` and `.paperList` elements. The native
theme stylesheet loads after nginx's injected links and applies compiled
background colors. Mapping `--jf-palette-surface-overlay` does not affect these
rules. Scoped overrides restore `--card-background` without changing profile
images. Check the user editing tabs as well as the Users listing; they use
different components.

Users cards, menu-button hover, action sheets, and mobile views were checked
with Aquamarine, Nord, and Hotline in Firefox 155. The same themes cover Profile,
Parental Control, Add User, and narrow Profile views. No permissions were saved.
Check stylesheet order after opening a route, not only on the initial page.

## Navigation and checks

- Home: `/web/#/home`. Open User Menu to inspect the new MUI menu.
- Library: use the Sample Movies navigation link. Open Filter, Sort, and View
  settings. The library URL includes `topParentId`; do not hard-code sample IDs
  in reusable tools.
- Movie: open a card, then More for the legacy action sheet. Delete media opens
  a confirmation; cancel it without deleting a sample.
- Display settings: use User Menu > Settings. Direct navigation to
  `#/mypreferencesdisplay` requires `?userId=<current-user-id>`. Without that
  parameter the tested release remained on its loading spinner.
- Close a menu with Escape before navigating programmatically to another route.
  An open menu can leave the underlying page hidden from accessible locators.
- Wait for dropdown animations to finish. Intermediate opacity can make a solid
  menu look translucent in a screenshot.
- Find visible Play/Resume buttons by accessible name. Detail pages also contain
  hidden replay buttons with the title Play.

Keep the maintainer's selected theme and profile intact. Test other palettes by
substituting the theme-option response in a separate browser context, then
verify the final source through the unchanged built-in injection. Native theme
selection is stored locally under `<userId>-appTheme`; change only the test
context's value. Do not reuse a browser device/session for simultaneous playback
checks, especially while the maintainer is testing SyncPlay.

## Verification scope

Firefox 155 desktop checks cover all 11 official options and Catppuccin Latte:
home, user menus, display settings, button hover, and selected dropdown items.
Aquamarine, Nord, and Hotline also cover native light mode and 390 by 844 touch
viewports. The mobile checks load production-minified CSS. Source imports and
rendered screenshots were checked as well as computed colors.

Library controls, movie details, action sheets, and the confirmation dialog
were inspected in Aquamarine. Chromium 152.0.7977.65 in T3 Code also received
a basic Aquamarine login, home, and detail-page check.

The nginx path was checked in Firefox 155 with Aquamarine, Nord, and Hotline.
Dashboard, General, Branding, Users, Devices, Activity, Plugins, Networking,
and Scheduled Tasks received desktop captures. The dashboard also received
390 by 844 checks. General settings dropdowns and Save hover, plus Activity
row hover and the column menu, were checked in all three themes. The final
table checks used minified CSS and included a narrow viewport. These are
appearance checks, not validation of every admin
action. No server settings were saved. HTTP and API forwarding passed; WebSocket
upgrade forwarding is configured but its handshake has not been verified. The dashboard's absent Custom CSS was
confirmed in the browser and upstream source. Screenshots and results are under ignored
`dev/artifacts/jellyfin/724/`.

Automated video playback did not start, with or without theme CSS. The video
remained at time zero with no decoded dimensions. The cause is unresolved, so
playback and its on-screen controls are not verified. Also untested: the full Chromium interaction matrix, TV layout, music/books/live TV, older Jellyfin versions, and the rest
of the community palettes. Do not treat the library checks as covering those.

## Stop

```sh
docker compose -f dev/jellyfin/compose.yaml down
```

Use `down -v` only to discard this fixture's configuration and cache. Remove its
ignored media directory separately only when you intend to regenerate samples.
