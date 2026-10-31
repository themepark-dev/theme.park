# Sonarr development

Run these commands from the theme.park checkout root. Compose starts a local CSS
host and two disposable LinuxServer instances, so you can compare v4 and v5 side
by side with the same theme.

| Service | URL | Image |
| --- | --- | --- |
| CSS host | http://localhost:18877 | `python:3.12-alpine` running `dev/serve.py` |
| v4 | http://localhost:18989 | `lscr.io/linuxserver/sonarr:4.0.20.3014-ls2` |
| v5 | http://localhost:18990 | `lscr.io/linuxserver/sonarr:develop-5.0.0.2870-ls205` |

`compose.yaml` pins both images by digest. LinuxServer publishes v5
under the `develop` tag. Hotio had no `v5` tag on 2026-10-31.

```sh
docker compose -f dev/sonarr/compose.yaml up -d
python3 -I dev/sonarr/seed.py
```

The ports bind to 127.0.0.1 and the injected stylesheet links use `localhost`.
To open the apps from another machine, set `DEV_BIND_ADDRESS=0.0.0.0` to publish
the ports and `DEV_HOST` to a host name that machine resolves. The browser
fetches the stylesheets itself, so `DEV_HOST` must be reachable from it, not only
from Docker. Repeat both variables every time you recreate a container. The seed
script talks to 127.0.0.1 and works either way.

Log in to either instance with `admin` / `admin`. The seed script turns on Forms
login, adds `/tv` as a root folder, and adds Breaking Bad, Severance, The Simpsons
and Stranger Things from Sonarr's public metadata lookup. It then writes empty
placeholder episode files for some seasons and rescans. Sonarr imports these
files, so the UI shows downloaded, missing and unaired episodes. The script adds
no indexers or download clients and downloads nothing. Each version has its own
config and TV volume.

## Injection

Both services run this checkout's Docker mod. Compose mounts the s6 service files
from `docker-mods/sonarr` where the published mod installs them, so edits to the
mod script apply when a container is recreated. `TP_DOMAIN` points at the local
CSS host. The script inserts the base CSS and theme option before `</body>` in
`index.html` and `login.html`.

The script picks the base file by version. v5 ships its UI build in
`/app/sonarr/bin/UI/assets`, and when that folder exists the script injects
`css/base/sonarr/sonarr-v5-base.css`. Otherwise it injects `sonarr-base.css`.
The container log prints `Sonarr v5 UI detected` when it picks the v5 file.
The same check covers the Hotio path, `/app/bin/UI`, but no Hotio v5 image
existed to test it.

LinuxServer's `/custom-cont-init.d` would be simpler, but it skips scripts not
owned by root, and a bind mount from the checkout is owned by the user. To test
the published mod instead, set `DOCKER_MODS=ghcr.io/themepark-dev/theme.park:sonarr`
and remove the three mod mounts.

Change the theme by recreating both app containers. A restart keeps the old
links, because the script skips injection when it finds an existing one.
Recreate with Nord afterwards to leave the review instance as it was.

```sh
TP_THEME=aquamarine \
  docker compose -f dev/sonarr/compose.yaml up -d --force-recreate v4 v5
TP_THEME=catppuccin-latte TP_COMMUNITY_THEME=true \
  docker compose -f dev/sonarr/compose.yaml up -d --force-recreate v5
```

## Browser checks

`capture.py` logs in and screenshots the login page, 13 main screens and the Edit
Series dialog. It needs Python Playwright outside the repository.
`python3 -m venv` fails on hosts where `ensurepip` is missing. uv works there:

```sh
uv venv /tmp/sonarr-theme-tools
VIRTUAL_ENV=/tmp/sonarr-theme-tools uv pip install playwright
/tmp/sonarr-theme-tools/bin/playwright install chromium
C="/tmp/sonarr-theme-tools/bin/python -I dev/sonarr/capture.py"
$C dev/artifacts/sonarr/<task>/nord
$C dev/artifacts/sonarr/<task>/native --native
$C dev/artifacts/sonarr/<task>/hotline --versions v5 --theme hotline --interactions
$C dev/artifacts/sonarr/<task>/latte-390 --versions v5 \
  --theme catppuccin-latte --community --width 390 --height 844 --pages series,missing
```

- `--native` blocks the CSS host to show the app's own styles.
- `--theme` swaps the injected theme option at request time, so you can compare
  options without recreating the containers. Confirm the final result through
  the mod as well.
- `--pages extra` captures Statistics, Blocklist, Library Import, the settings
  subpages and the System pages. `--pages none` skips page captures.
- `--interactions` opens the View menu, table view, header search results, the
  episode modal, an open select inside the Edit dialog, a season popover and the
  month calendar. At 768 pixels or less it also opens the sidebar. On a phone
  width v5 hides Edit and Month, so those two steps fail at that width.

Playwright Firefox downloads but did not launch on the test host. It needs GTK
libraries such as `libgtk-3-0t64` that require sudo to install. The Playwright
MCP browser also fails, because it expects Google Chrome at
`/opt/google/chrome/chrome`.

The theme.park sheets are cross-origin, so `cssRules` reads as `null` in
`report.json`. The report's `css-failures` list records any request to the CSS
host that returned 400 or more.

Python Playwright passes `(route, request)` to a route handler that takes two
or more parameters. A handler written as `lambda r, theme=theme: ...` receives
the request object as `theme`. Build the handler in a function that returns a
one-argument lambda.

v5's own UI calls `/api/v5`, not `/api/v3`. To capture the loading screen, hold
every `**/api/**` request in a route handler, reload, take the screenshot and
close the context without releasing the requests.

## Selector audit

`selector-audit.py` follows the `@import` chain of a base stylesheet and checks
every `[class*=...]`, `[class^=...]` and `[class$=...]` selector against the class
names in a copy of the app's UI build.

```sh
mkdir -p dev/artifacts/sonarr/<task>
docker compose -f dev/sonarr/compose.yaml cp v5:/app/sonarr/bin/UI dev/artifacts/sonarr/<task>/ui-v5
python3 -I dev/sonarr/selector-audit.py css/base/sonarr/sonarr-base.css \
  dev/artifacts/sonarr/<task>/ui-v4 dev/artifacts/sonarr/<task>/ui-v5
```

It compares individual class names, not rendered elements. A match means the
class exists in the build, not that a given screen uses it. `servarr-base.css`
is shared with Radarr, Lidarr and Prowlarr, so selectors such as
`MovieDetails-` and `AppProfiles-` never match a Sonarr build.

## Sonarr v5 theme

v4 keeps `sonarr-base.css`. v5 uses `css/base/sonarr/sonarr-v5-base.css`, which
does not import `servarr-base.css` and does not touch any shared file. `themes.py`
still lists only `sonarr-base.css` as Sonarr's base, so the generated
`sonarr/<theme>.css` wrappers load the v4 theme. Users who inject by hand, such
as with nginx subfiltering, need to link `sonarr-v5-base.css` and the theme option
directly. The docs in tp-docs do not mention this yet.

### Why v4 selectors fail on v5

v4 builds with webpack and names CSS module classes `PageHeader-logo-a1b2c`. v5
builds with Vite and names them `PageHeader-module_logo_a1b2c`. The selector audit
found 205 of 221 theme.park selectors present in v4 and 3 in v5. Renaming them
mechanically would recover 168, but v5 is also a redesign. The sidebar has new
groups, the toolbar puts labels beside icons, settings use cards and the fonts
changed. Audit results are in `dev/artifacts/sonarr/v5-audit/`.

### How the v5 file works

v5 defines about 200 custom properties on `:root` and overrides them under
`[data-theme=dark]`. Most components read a small base palette directly:
`--ink` and `--inkMuted` for text, `--paperCard` and `--paperWarm` for surfaces,
`--hairline` for borders and `--accent`. The v5 file sets those and the semantic
variables in one `:root:root` block. Its specificity beats `[data-theme=dark]`
and `[data-header-color=gradient]`, so one block covers native light mode, dark
mode and both header modes.

The file keeps element rules for three cases:

- **Full backgrounds.** `--main-bg-color` and the modal variables can hold
  gradients, and v5 applies its variables with `background-color`. The page,
  modal content, header and footer get `background:` rules. Sticky bars on the
  calendar, Add New search and series overview get the page background with a
  fixed attachment, so gradients line up with the page behind them.
- **Opaque layers.** Menus, select dropdowns, header search results, popovers and
  tooltips use `--drop-down-menu-bg`. A translucent layer would show the content
  under it.
- **Button text.** `--defaultColor` colors plain text elsewhere, so default and
  primary buttons get `--button-text` from an element rule.
  `FormInputButton`, such as the `?` beside naming fields, is a primary button
  with its own background and stays out of that rule.

Decisions made while testing:

- Translucent lines, hovers and input fills are mixed from `--text` with
  `color-mix`. The `--transparency-light-*` values disappear on light palettes,
  which hid checkboxes and input borders under Catppuccin Latte. Header, sidebar,
  toolbar and cards keep the v4 dark overlays, so they look grey under Latte,
  as they do in v4.
- `--inkMuted` is `--text` at 75%, not `--text-muted`. v5 uses it 118 times for
  secondary text. Hotline's `--text-muted` is `#999`, which was hard to read on its
  gradient. The v4 theme also used `--text` for help text.
- `--white` keeps the app's value. v5 uses it for the series title over the
  backdrop image and for text on status buttons. Mapping it to `--text-hover`
  made the title dark under Latte.
- The page background is painted on `<html>`. v5's `login.html` gives `<html>`
  its own background, which stops a body background from covering the window.
- The sidebar container has an identity `transform`, which turns a fixed
  background into one sized to the sidebar. On wide screens the sidebar is
  transparent over the page. At 768 pixels or less it covers the content and
  gets the page background.
- Success, warning and danger buttons and labels keep the app's status colors.

### Verified

Sonarr 5.0.0.2870 from `lscr.io/linuxserver/sonarr:develop-5.0.0.2870-ls205`,
Chromium 156.0.8078.4, through the checkout's Docker mod, on 2026-10-31.

- Nord, Aquamarine, Hotline and Catppuccin Latte at 1440 by 900 on the main
  screens, the extra screens and the interactions above. Plex on series,
  series details, profiles and calendar. Nord and Aquamarine at 390 by 844,
  including the open sidebar.
- Rest, hover, after-hover and keyboard focus with a real pointer for toolbar,
  sidebar, table row, form input button and modal buttons under Nord, Hotline
  and Latte.
- Native light mode under Nord and Latte, color-impaired mode under Nord, and
  the gradient header under all four themes.
- The login page and the loading screen.
- Final checks through the mod with `TP_THEME=aquamarine` and with
  `TP_THEME=catppuccin-latte TP_COMMUNITY_THEME=true`. v4 still loads
  `sonarr-base.css` and looks as before.

Saving the gradient header from the UI settings page did not persist in this
build. The API returns `headerColor: null` after a save. The checks set
`data-header-color="gradient"` on `<html>`, which is what the app does when the
setting is on. UI appearance settings are stored on the server, so restore them
after testing. Save the original with `GET /api/v3/config/ui` first.

Screenshots and reports are in `dev/artifacts/sonarr/v5-theme/`. The `final-*`
runs are the checks through the mod.

### Not tested

- Firefox and Safari.
- Hotio images, which had no v5 tag.
- Interactive search and its sticky scroll bar, the queue with real downloads,
  and download client or indexer add dialogs with real providers.
- OIDC login and the password reset pages.
- Community themes other than Catppuccin Latte, and theme options other than the
  five above.

## Stop and reset

```sh
docker compose -f dev/sonarr/compose.yaml down
```

Add `--volumes` to discard both configs and the placeholder TV folders.
