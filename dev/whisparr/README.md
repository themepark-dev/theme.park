# Whisparr development

Run these commands from the theme.park checkout root. Docker Compose hosts
local CSS at http://127.0.0.1:18875 and starts disposable Hotio instances at
http://127.0.0.1:16969 for v2 and http://127.0.0.1:16970 for v3.
The pinned images contain Whisparr 2.2.0.231 and 3.5.0.1585.

```sh
TP_ADDON=whisparr-4k-logo docker compose -f dev/whisparr/compose.yaml up -d
```

On first launch, choose Forms authentication and create a local test account.
The logo checks work with an empty library. Do not add real media or indexers.
Configuration lives in separate Docker volumes.

The setup mounts the repository's Whisparr startup script into
`/etc/cont-init.d/98-themepark`, following the
[Hotio setup](https://docs.theme-park.dev/setup/#hotio-containers-s6-overlay-v3-images).
`TP_HOTIO=true` selects `/app/bin/UI`. The script injects the app base CSS,
theme option, and addon before `</body>` in both the app and login pages.
It does not use `DOCKER_MODS`.

To change themes, recreate both application containers. Restarting alone leaves
the old stylesheet links in their HTML because the script avoids duplicate injection.

```sh
TP_THEME=aquamarine TP_ADDON=whisparr-4k-logo \
  docker compose -f dev/whisparr/compose.yaml up -d --force-recreate v2 v3
```

Repeat with `TP_THEME=hotline` and `TP_THEME=nord`. Omit `TP_ADDON` when recreating
to capture the original logo. CSS and SVG edits appear on browser reload.
The CSS host sends `Cache-Control: no-store`.

## Logo checks

Check the desktop header, mobile header, open mobile menu, loading screen, and
Forms login page. Resize to 1280, 768, 752, 390, and 320 pixels wide. Check hover,
keyboard focus, home navigation, and opening and closing the menu.

Whisparr v2 uses `PageHeader-logo-` at every width. V3 uses
`PageHeader-logoFull-` on desktop, `PageHeader-logo-` on mobile, and a separate
`PageSidebar-logo-` in the open mobile menu. V2 does not have that sidebar image.
Both versions use `LoadingPage-logoFull-` and `.panel-header > img.logo`.

To inspect loading, delay the app's API requests in browser automation while
reloading an authenticated session. Release the requests after capturing the
real loading screen. Check asset requests for the addon SVG, base CSS, imported
Radarr and Servarr styles, defaults, and selected theme option.

Save screenshots and run details under ignored `dev/artifacts/whisparr/550/`.
Issue #550 reported Hotio versions 2.0.0.355 and 3.0.0.530. The pinned test images
are newer, so results do not establish compatibility with those exact builds.

## Artwork

`whisparr-4k.svg` uses the purple Whisparr SVG shipped in the pinned v3 image.
Its gold 4K image is the unchanged `Layer 3` inside the `sonarr-4k` group in
`css/addons/sonarr/sonarr-logo.psd`. The SVG embeds that layer so it needs no
external image request. Its square layout matches the Sonarr and Radarr addons.
Keep the upstream W paths and the existing gold lettering when changing placement.

## Stop and reset

```sh
docker compose -f dev/whisparr/compose.yaml down
```

To discard only these test configurations, add `--volumes` to that command.
