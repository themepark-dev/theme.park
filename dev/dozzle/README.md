# Local Dozzle theme development

This setup was added for [issue #559](https://github.com/themepark-dev/theme.park/issues/559).
The report dates from April 28, 2024 and shows Dracula with barely visible
stack labels. It does not name an app version or injection method.

The refresh targets Dozzle v11.0.1. Its
[UI redesign notes](https://dozzle.dev/guide/whats-new) cover the sidebar,
dashboard, log viewer, settings, and menus. The maintainer explicitly excluded
backward compatibility from this task, so the base stylesheet replaces the old
Bulma/Buefy rules. Older Dozzle releases are not supported by this refresh.

## Start and compare

Run from this checkout's root:

```sh
docker compose -f dev/dozzle/compose.yaml up -d
```

| Address | Purpose |
| --- | --- |
| http://localhost:18080 | Native Dozzle without theme.park injection. |
| http://localhost:18081 | Same app through nginx with theme.park CSS. |
| http://localhost:18865 | Live CSS and resources from this checkout. |

All published ports bind to loopback. No login is configured. Dozzle reads the
local Docker socket and filters its UI to containers labeled
`dev.themepark.sample=dozzle`. The filter limits what it displays, not socket
permissions. A read-only socket mount does not restrict Docker API operations.
Container actions and shell access are disabled. Analytics is disabled and the
instance is not linked to Dozzle Cloud.

The two running samples emit synthetic JSON logs with debug, info, warning, and
error levels, nested fields, multiline text, and ANSI colors. Display-name labels
keep their names short without changing their Compose stack group. `sample-stopped` exits with code 1 intentionally, providing an
exited container to inspect. It is not a setup failure. The samples share a
Compose project, which produces the sidebar stack group without external data.

For development, edit `css/base/dozzle/dozzle-base.css` and refresh port 18081.
The CSS server mounts source files read-only and sends `Cache-Control: no-store`.
There is no image rebuild needed for CSS edits. The default theme is Dracula.
To change the injected option:

```sh
TP_THEME=aquamarine docker compose -f dev/dozzle/compose.yaml up -d proxy
TP_THEME=catppuccin-latte TP_THEME_FOLDER=community-theme-options docker compose -f dev/dozzle/compose.yaml up -d proxy
```

`DOZZLE_TAG` can select another release. Record the exact version tested; this
setup has only been verified with v11.0.1. Recreate the proxy after replacing
Dozzle because nginx resolves the upstream service at startup:

```sh
DOZZLE_TAG=v11.0.1 docker compose -f dev/dozzle/compose.yaml up -d dozzle
docker compose -f dev/dozzle/compose.yaml up -d --force-recreate proxy
```

## Injection and streaming

The proxy follows the [theme.park setup guide](https://docs.theme-park.dev/setup/#nginx)
and [Dozzle-specific instructions](https://docs.theme-park.dev/themes/dozzle/):

- Request uncompressed HTML and insert the base CSS and theme option before
  `</head>`. Confirm each link occurs once in the response.
- Remove upstream `Content-Security-Policy` and `X-WebKit-CSP` headers on the
  themed route, as documented for Dozzle. The direct port retains native CSP.
- Keep `/api` separate with buffering and caching off for live event/log streams.
  Do not inject anything into those responses.
- Use a separate CSS origin so absolute imports such as `/css/defaults/transparent.css`
  resolve to theme.park files instead of colliding with application routes.

Test a newly arriving heartbeat as well as existing log rows. Seeing old logs
does not verify that the proxy streams updates. The heartbeat message repeats,
so compare the timestamp in the same rendered row rather than the message text
alone. This setup does not enable or
validate shell/attach WebSockets, authentication, a URL subfolder, Swarm,
Kubernetes, or remote agents.

## Navigation and inspection

1. On the homepage, expand and collapse the Compose group in the sidebar.
   Open its More options menu and enable Show all containers to include the
   stopped sample. Alternatively use the corresponding setting on `/settings`.
2. Select sample-web to open the log viewer. Inspect selected and hovered rows,
   the group label, timestamps, log severity, the toolbar, and stream background.
3. Open `/settings` directly or use the homepage gear. The gear is not present
   in every log-view layout. Compare controls, labels, and section backgrounds.
4. Change native appearance separately from the injected theme. v11 stores
   profile settings on the server, shared by the direct and proxy URLs. A
   native mode switch can affect other open tabs. Automated comparisons should
   set the profile before opening a fresh page to avoid reload races.
5. At phone width, use `[data-testid="hamburger"]` to open the sidebar. The
   desktop and mobile layouts use the same SideMenu component.

Useful v11 selectors are `[data-testid="side-menu"]`, `.nav-group-toggle`,
`.nav-item`, `.nav-item.is-active`, and `.btn`. The historical `.menu-list`
selector does not reach this sidebar. Read upstream `assets/main.css`,
`assets/components/nav/NavGroup.vue`, and `NavItem.vue` before adding overrides.
Avoid copying Vue's generated `data-v-*` attributes into new theme rules.

Save screenshots, source snapshots, and browser results under
`dev/artifacts/dozzle/559/`. Browser versions, screenshots, and run results are stored in that ignored
directory. Do not add upstream source checkouts or screenshots to the CSS host
or the tracked fixture.

## Styling hooks and pitfalls

Dozzle 11 uses Tailwind 4 and DaisyUI 5. Prefer public component classes and
attributes over Vue's generated `data-v-*` attributes. The base stylesheet maps
DaisyUI colors at `html[data-theme]`, so theme.park controls the palette in both
native light and dark modes. The native choice still controls browser appearance.

- Keep `--color-base-*` values color-only. They feed `color-mix()` and utility
  classes. Use full `background` declarations for page gradients, floating menus,
  mobile navigation, sticky log headers, and dialogs. A transparent base color
  needs explicit opaque backgrounds wherever content floats over logs.
- The search dialog has a padded, transparent `.modal-box` around its visible
  panel. Theme that inner panel and its header/footer separately. Ordinary
  `.modal-box` elements and the `.modal-right` drawer need their own background.
  Notification form actions use `.sticky.bottom-0` inside the drawer.
  Drawer headers are inset within the body, without an edge-to-edge divider.
  Keep them transparent so the modal background continues through the heading.
  The maintainer explicitly approved skipping `--modal-header-color` here after
  gradient themes exposed a separate rectangle inside the modal padding.
  The search dialog still uses its separate header and footer variables.
- `.nav-group-toggle` is the stack label from issue #559. `.nav-item.is-active`
  and `.is-merged` mark selected streams. Use readable text with an accent border
  and tint; dark accent colors alone can disappear against gradient backgrounds.
- DaisyUI status buttons expose `--btn-color` and `--btn-fg`. Preserve those for
  danger/status controls. Dozzle's generic hover rule otherwise replaces their
  backgrounds with `--color-base-100`. Disabled buttons use `pointer-events: none`.
- Expression errors use the literal class `input-error!`. Its error border must
  beat the normal `:focus-within` border. CodeMirror exposes `.cm-editor` and
  semantic color variables, so generated syntax-token classes are unnecessary.
- ANSI log colors use `--ansi-*`. Native light-mode colors can become too dark
  after injecting a dark theme. The theme mixes terminal hues with its text color
  and reuses them for JSON and editor highlighting. Log severity indicators retain
  Dozzle's error, warning, info, and debug colors.
- Theme changes animate text and buttons. Wait for link loading and transitions
  before checking exact colors or capturing screenshots.
- Log lists expose `data-logs`. Use that attribute for their darker transparent
  background, not `highlight-errors`, which is an optional row-highlighting
  setting. Keep row hover and severity tints visible over the list background.
  The details drawer's `.field-row code` values stay transparent; the general
  inline-code background otherwise paints a separate box behind each value.

## Interaction paths

| Area | Steps |
| --- | --- |
| Container search | Home, Search containers. Type a nonexistent name for the empty state. Escape closes it. |
| Log details | Open sample-web, hover an error row, then its ellipsis, then Show details. Inspect nested JSON and field toggles. |
| Settings dropdown | Settings, one of the Auto dropdowns. Check the open menu and selected option. |
| Notification form | Notifications, Add alert. Try the log, metric, and event types. Type `name ???` into the container expression to see validation. |
| Discard confirmation | Change an alert field, then Cancel. Keep editing or Discard affects only the unsaved form. |
| Destination form | Notifications, Destinations tab, Add destination. Inspect the payload editor without testing or saving a webhook. |
| Phone menu | At 390 by 844, open the hamburger, select sample-web, and open log details. Scroll the actual drawer to reach its lower fields. |

Notifications uses buttons with `role="tab"` for Alerts and Destinations. Locate
those as tabs in browser automation. The discard button's English name is
`Discard`, and the disabled form action is `Create Alert`.

Log action menus close 150 ms after the pointer leaves them. Move a real pointer
into the open panel before waiting for its animation and clicking an item.
Otherwise an automation stability wait can outlast the hover menu. For phone
checks, emulate touch as well as viewport width. Dozzle uses a click toggle when
`hover: hover` is false. Wait for initial log loading to settle before opening a
row menu; automatic scrolling can move its anchor. A long-running sample can
push the initial ANSI/nested examples outside the first log batch. Use the
stopped sample for fixed data, load older logs, or recreate only the synthetic
sample services when fresh captures are needed.

## Verification for issue #559

The September 2026 refresh was checked on `amir20/dozzle:v11.0.1`, digest
`sha256:8d88ee5cb7f7144bc5d42f11181e576a321d5d084101c0ae3db7227a8d84967e`.
The report is from April 2024 and names neither a version nor an injection method.
The refresh intentionally targets the current UI, not the historical screenshot.

Firefox 155.0 checks cover all 11 official theme options in both native modes,
plus Catppuccin Latte. They include dashboard, stack labels, button hover,
container search, logs, and the details drawer. Nord, Aquamarine, and Hotline
also have 390 by 844 touch checks, including drawer scrolling and page overflow.
Chromium 152.0.7977.65 in T3 Code was checked on the dashboard and search dialog.

Additional checks cover toggles, keyboard focus, empty search, invalid expression
borders, disabled buttons, discard-button hover, notification forms, and a fresh
heartbeat arriving through nginx. A temporary option also checks a radial modal body, a solid header, and a
linear footer with distinct colors. CSS injection, imports, served file bytes,
nginx configuration, and production minification are checked separately.

The PR for this refresh must include screenshots of every official theme option,
as requested by the maintainer. Matching `after-dark-<theme>-home.png`, `-logs.png`,
`-search.png`, and `-details.png` files are kept in `dev/artifacts/dozzle/559/`.
Keep screenshots out of the production asset tree.

Not covered: authenticated sessions, linked Cloud features, shell/attach,
container actions, remote agents, Swarm, Kubernetes, URL subfolders, every
community palette, and older Dozzle versions. Notification forms were inspected
without saving destinations, testing webhooks, or sending notifications.
The unlinked `/api/cloud/config` response is 404 in native and themed runs.
That is not a theme regression.

## Stop

```sh
docker compose -f dev/dozzle/compose.yaml down
```

This removes the task's containers and network, including the log samples.
Add `-v` only to discard the disposable Dozzle profile volume as well.
