# Nginx Proxy Manager development

This setup runs NPM 2.15.1 with SQLite and disposable volumes. Only the admin
port is exposed, on loopback. The sample hosts forward to the local CSS server;
no public proxy ports or real certificates are needed.

## Start and seed

Run from the repository root.

```sh
docker compose -f dev/nginx-proxy-manager/compose.yaml up -d
```

Open http://127.0.0.1:18084 and sign in with **admin@example.com / adminadmin**.
The maintainer's default is `admin` / `admin`. NPM's login form requires an
email address and at least eight password characters, so this setup uses the
documented fallback. `NPM_DEV_PASSWORD` can override the default password.
NPM applies the initial account variables only to an empty database.

```sh
python3 dev/nginx-proxy-manager/seed.py
```

The seed script creates `media.example.test`, `downloads.example.test`, and a
standard user `reviewer@example.test` for permission-dialog checks, once.
Refresh Proxy Hosts after seeding. Data persists in the Compose volumes.

## CSS injection

The [NPM theme documentation](https://docs.theme-park.dev/themes/nginx-proxy-manager/)
uses an executable startup script, not the LinuxServer `DOCKER_MODS` variable.
Compose mounts the repository's executable script at `/etc/cont-init.d/99-themepark`.
In 2.15.1 this inserts base and theme-option links at the end of
`/app/frontend/index.html`'s head. No proxy injection is needed.

The CSS host serves the current checkout at http://127.0.0.1:18867.
The browser must be able to reach that loopback address. This setup is for a
browser on the Docker host. Confirm requests for the base CSS, theme option,
`placeholders.css`, and `transparent.css` in the browser or CSS server logs.

```sh
docker compose -f dev/nginx-proxy-manager/compose.yaml logs css
```

Edit the base CSS and reload to test. To change the injected theme, recreate
NPM, since the startup script does not replace links already present in HTML.
Container recreation restores the image's original HTML before injection.

```sh
TP_THEME=nord docker compose -f dev/nginx-proxy-manager/compose.yaml up -d --force-recreate npm
```

Repeat the chosen `TP_THEME` override whenever recreating NPM. Compare native
styling by disabling both injected link elements in browser developer tools.
A full reload restores the injected styles.

## UI migration and issue 707

[Issue 707](https://github.com/themepark-dev/theme.park/issues/707) was opened
on November 4, 2025. It reports mismatched white and dark-blue areas, without
an app version, browser version, named theme, or injection method.
[NPM 2.13.0](https://github.com/NginxProxyManager/nginx-proxy-manager/releases/tag/v2.13.0)
introduced React, updated Tabler, and native light/dark modes. Do not treat
2.13.0 as the reporter's confirmed version.

The existing theme reproduces the mismatch on 2.15.1. In native light mode,
Proxy Hosts and Users tables have dark text on themed dark backgrounds.
The Add Proxy Host dialog has dark labels, white React Select controls and
switches, and a white tab strip. In native dark mode those controls and the
navigation retain NPM's blue-gray palette. The page and modal gradients load.
The modal contains a `.card` that applies its own text color and background,
so changing `.modal-content` alone cannot fix the labels.

The rewrite fixes these theme compatibility defects. The Users table repeats the same contrast defect
outside the reported host screen. The rewrite also removes filled backgrounds that the old broad
`[class*="btn-"]` rule incorrectly applied to ghost buttons.

Implementation notes:

- NPM sets `data-bs-theme` on the root element, `data-theme` and a light/dark
  class on the body, and stores its choice as `tabler-theme` in local storage.
- Tabler uses `--tblr-body-color`, `--tblr-bg-forms`, and surface, card, table,
  border and button variables. Map them to theme.park colors in both modes.
  Inspect component-local declarations before relying on root overrides.
- React Select exposes `.react-select__control`, `__menu`, `__option`, and
  `__multi-value` classes. Old `.selectize-*` rules do not cover it.
- Switches use `.form-check-input`, headers use `.navbar`, and modal close
  buttons use `.btn-close`. The old `.custom-switch-input`, `.header`, and
  `.close` selectors matched nothing on the inspected host page and dialog.
  Backwards compatibility was explicitly excluded by the maintainer.
- Preserve status colors and button variants. Use `background` for theme
  variables that can contain gradients. Inspect the modal's nested card,
  tabs, header and footer individually.

The browser review covers login/setup, navigation, populated and empty host tables,
host editors and their SSL/custom-location/advanced tabs, access lists,
certificates, users/permissions, audit logs, settings, notifications and errors.
The core verification runs in both native modes at desktop and mobile sizes,
with Chromium and Firefox. It checks Nord, Aquamarine, Hotline, and
Catppuccin Latte. Certificate issuance and real proxy traffic are outside the
CSS checks. The gray text baked into NPM's login/setup logo remains unchanged.

## Verify

Install Playwright in a temporary virtual environment, outside the repository.

```sh
python3 -m venv /tmp/npm-theme-tools
/tmp/npm-theme-tools/bin/pip install playwright
/tmp/npm-theme-tools/bin/playwright install chromium firefox
/tmp/npm-theme-tools/bin/python dev/nginx-proxy-manager/verify.py
/tmp/npm-theme-tools/bin/python dev/nginx-proxy-manager/verify_variables.py
```

`verify.py` saves screenshots and checks the loaded source CSS, imports, primary
button hover, domain selection, switch state, focus, disabled SSL controls,
editor, and independent modal backgrounds. Set `TP_THEME` to match the injected
theme. A run takes both browsers through light/dark mode and 1440x1000/390x844.
Inspect the screenshots as well as the results JSON.

`verify_variables.py` uses a temporary browser palette with distinct values for
every general theme variable. It checks navigation, footer and dashboard links
with a real pointer and keyboard focus, buttons, labels, menus, and independent
radial/linear/solid modal sections. Reload removes that diagnostic palette.

For the light community option:

```sh
TP_THEME=catppuccin-latte TP_COMMUNITY_THEME=true docker compose -f dev/nginx-proxy-manager/compose.yaml up -d --force-recreate npm
TP_THEME=catppuccin-latte /tmp/npm-theme-tools/bin/python dev/nginx-proxy-manager/verify.py
```

Restore the default review theme after testing:

```sh
docker compose -f dev/nginx-proxy-manager/compose.yaml up -d --force-recreate npm
```

Tabler's footer `.link-secondary` rules use `!important` in normal and hover
states. Mapping only `--tblr-link-hover-color` does not override them. Navigation
has separate local colors. Verify both components directly when changing links.
React Select's generated hover rule can also beat a control rule with equal
specificity. Its multi-value label has a four-class important selector in NPM.

NPM renders `.toast` and `.toast-header` inside a transparent Toastify wrapper.
Style those inner elements to avoid native white headers and transparent bodies.
Floating labels replace placeholders, so the shared placeholder import must not
make both labels visible. The editor sets `data-color-mode="dark"` regardless of
NPM mode; map its syntax variables and the `pre`/`code` foreground as well as the
container background. Keep the textarea overlay transparent.

## Stop or reset

```sh
docker compose -f dev/nginx-proxy-manager/compose.yaml down
```

Add `--volumes` only to reset this disposable instance and delete its users,
hosts and certificates. Run-specific screenshots and findings belong in ignored
`dev/artifacts/nginx-proxy-manager/707/`.

## Theme variable consumers

| theme.park variable | NPM consumer |
| --- | --- |
| `--main-bg-color` | Document background, using the full background shorthand. |
| `--modal-bg-color` | Modal shell/body; the nested editor card stays transparent. |
| `--modal-header-color` | Modal header. |
| `--modal-footer-color` | Modal footer. |
| `--drop-down-menu-bg` | Dropdowns, React Select menus, notifications, native select options. |
| `--button-color`, `--button-text` | Primary actions, file upload buttons, checked switches. |
| `--button-color-hover`, `--button-text-hover` | Primary action and upload hover/active states. |
| `--accent-color` | Focus rings, selected tab borders, selection and domain-label backgrounds. Remains an RGB triplet. |
| `--accent-color-hover` | Tab hover borders and the remove action on domain labels. Remains a CSS color. |
| `--link-color`, `--link-color-hover` | Navigation, dashboard links, footer and ordinary anchors, including keyboard focus. |
| `--label-text-color` | Text selection and domain-label foregrounds. |
| `--text` | Body, table, form and editor text; neutral buttons. |
| `--text-hover` | Headings, focused inputs, close-button hover and menu action hover. |
| `--text-muted` | Secondary text, placeholders, floating labels and neutral icons. |

Danger, warning and success actions and status badges keep their semantic colors.
Neutral Cancel buttons and ghost icon controls retain a separate style from
primary actions. App-specific specials such as `--arr-queue-color`,
`--plex-poster-unwatched`, `--petio-spinner`, `--gitea-color-primary-dark-4` and
`--overseerr-gradient` have no NPM consumers and are intentionally unused.
