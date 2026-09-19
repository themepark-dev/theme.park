# Local Pi-hole theme development

This setup reproduces [issue #662](https://github.com/themepark-dev/theme.park/issues/662).
The reporter used Pi-hole v5.18.3 and replaced `lcars.css` with Aquamarine.
The fixture runs `pihole/pihole:2026.07.2`, with Core v6.4.3, FTL v6.7, and
Web v6.6. It keeps the native dark theme and uses the
[documented nginx injection method](https://docs.theme-park.dev/themes/pihole/).

## Start

Run from the checkout root:

```sh
docker compose -f dev/pihole/compose.yaml up -d
# Wait until the native web interface loads, then add synthetic devices:
python3 dev/pihole/seed.py
```

| Address | Purpose |
| --- | --- |
| http://localhost:18082/admin/network | Native Network page. |
| http://localhost:18083/admin/network | Network page with local theme.park CSS. |
| http://localhost:18866 | Source CSS and resources. |

The UI has no password and binds to loopback. DNS and DHCP ports are not
published. Configuration lives in a disposable Compose volume. The seed script
writes four synthetic devices into that fixture's database: a recent query,
a query about 12 hours ago, an older query, and a device that never queried.
It uses reserved example addresses and does not send DNS traffic.

Edit `css/base/pihole/pihole-base.css` and refresh the proxy URL. The server
sends `Cache-Control: no-store`. Change themes with:

```sh
TP_THEME=nord docker compose -f dev/pihole/compose.yaml up -d proxy
```

The default is Aquamarine. Repeat the selected theme override when recreating
the proxy. If the Pi-hole container is recreated, recreate the proxy too so
nginx resolves its new address.

The proxy requests uncompressed HTML, injects two stylesheet links before
`</head>`, and adjusts CSP to allow the local CSS origin. `/api` bypasses HTML
injection. Confirm both source files and their imports return successfully.

## Network colors are also JavaScript inputs

Web v6.6's `scripts/js/network.js` reads the computed background colors of
`.network-recent`, `.network-old`, `.network-older`, and `.network-never`.
Its `parseColor()` accepts opaque `rgb(r, g, b)` values only. It interpolates the
recent and old colors to paint rows according to the last query time.

Replacing the native theme removes these definitions. The computed value becomes
transparent, the parser returns no RGB array, and the row callback throws.
The table stays on Processing even though the API returned devices. An empty
database may hide the failure because no recent-query row reaches that callback.

Keep these colors opaque. Alpha colors, gradients, and modern color syntax
can break the parser even when the CSS is valid. The base CSS uses Pi-hole's
native dark status colors and restores the matching `.network-gradient` legend.
These indicate device activity, so they do not follow the theme's accent color.

For a replacement-method reproduction, back up the disposable container's
`/var/www/html/admin/style/themes/default-dark.css`, then replace it with the
base CSS and chosen option. Inline the two default imports, or host them at
working URLs; relative imports otherwise resolve against Pi-hole. Reload the
direct Network URL with seeded devices. Restore the native file afterward and
verify the final CSS through the proxy as well. Never replace files in a real
Pi-hole installation for this test.

## Verification for #662

Firefox 155 checks reproduced the Processing failure and JavaScript exception
when the native dark stylesheet was replaced. The patch loaded all four rows
with all 11 official options using production-minified CSS. Aquamarine, Nord,
and Hotline also passed through nginx injection, including search and successful
loads of both local stylesheets and their imports. A 390 by 844 touch viewport
also loaded all four rows without a JavaScript error. Before/after screenshots and
run results are under ignored `dev/artifacts/pihole/662/`.

The exact reported v5.18.3 release and LCARS selection were not tested. The
replacement test uses the documented native dark mode on the current release.
This is a Network page fix, not a full Pi-hole theme refresh. Authentication,
other browsers, and community light palettes remain outside this check.

## Shared borders in Web v6.6

The native dark stylesheet adds an opaque gray border to `.box` panels and
separate colors to `.box-header.with-border` and `.table-bordered`. The old
theme only overrode table cells, leaving the outer border and heading divider
in the native palette. Page titles also retain Bootstrap's bright divider.
The theme now uses `--transparency-light-15` for these shared borders.

The follow-up pass inspected Network, Groups, Dashboard, Query Log, and System
Settings. Use `/admin/settings-system`; `/admin/settings` returns a native 404.
Network was checked with Aquamarine, Nord, and Hotline after the border change.
Status-colored panel headers and device activity colors retain their meaning.
The query log was empty, so populated query rows and their details dialogs were
not covered by this pass. No additional defects were confirmed in the inspected
views.

## Stop

```sh
docker compose -f dev/pihole/compose.yaml down
```

Add `-v` only to discard this fixture's configuration and synthetic devices.
