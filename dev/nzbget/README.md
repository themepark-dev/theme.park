# Local NZBGet theme development

Run these commands from the repository root with Docker Compose and Python 3:

```sh
docker compose -f dev/nzbget/compose.yaml up -d
python3 dev/nzbget/seed.py
```

Wait for NZBGet to finish starting before seeding. Open http://localhost:16789
and log in with username `nzbget` and password `tegbzn6789`. The seed script adds
three paused dummy downloads. It needs no Usenet account and downloads no files.
Running it again adds another three entries.

The official Docker mod injects HTML stylesheet links pointing at
http://localhost:18765. The CSS server mounts this checkout's `css` and
`resources` directories read-only and sends `Cache-Control: no-store`. Edit
`css/base/nzbget/nzbget-base.css` and refresh the app to see changes.
Compose binds both ports to loopback. The browser resolves `localhost` in
`TP_DOMAIN`. In WSL, open the URL from the same desktop.

Change the theme or app version by recreating the app container:

```sh
TP_THEME=dracula docker compose -f dev/nzbget/compose.yaml up -d
TP_THEME=catppuccin-latte TP_COMMUNITY_THEME=true docker compose -f dev/nzbget/compose.yaml up -d
NZBGET_TAG=version-v26.3 docker compose -f dev/nzbget/compose.yaml up -d
```

The default version is 25.2, as reported in issue #694. NZBGet's own light and
dark modes are separate from `TP_THEME`. Check both native modes.

Select one row and check that the header shows a minus. Select all rows and
check that the header shows a checkmark. Then clear the selection.
Also check a download's Files table and the narrow layout.
Capture before/after screenshots using the same theme, selection, and viewport.

## Modal color checks

Test Nord, Aquamarine, and Hotline in both native appearance modes. Check Plex
when working on layered page backgrounds. A light option such as Catppuccin
Latte also helps expose text contrast problems.

| Dialog | How to open it | What to inspect |
| --- | --- | --- |
| Edit download | Click a seeded download's name. | Header, body, footer, inputs, and the statistics table. |
| Files | Open Edit download, then Files. | Scrollable content, row selection, and the footer on a narrow viewport. |
| Add | Click Add above the queue. | The URL input, file controls, and the modal background. Close without submitting. |
| Speed limit | Click the speed display beside the NZBGet logo. | A smaller dialog with the same shared modal styles. Close without saving. |

Use the native appearance control separately from `TP_THEME`. Version 25.2 has
`#ThemeToggle`. Version 26.3 puts the light/dark choices in the preferences menu.
Inspect `link#ThemeStyleSheet` to confirm which native stylesheet loaded.

The container's upstream styles are in `/app/nzbget/webui/style.css`,
`dark-theme.css`, `light-theme.css`, and `lib/bootstrap.css`. Inspect the loaded
styles and the theme.park override together. The app may request Bootstrap and
`style.css` through a combined CSS URL.

### Findings from the local trial

The native dark stylesheet gives `.modal-body` a `#212529` background. Coloring
`.modal` alone leaves that child panel covering the theme background. The fix
makes the body transparent so the dialog shell supplies its background.

The footer previously passed `--modal-footer-color` to `background-color`.
That worked with hex colors but failed with a gradient value. A transparent
footer could still appear correct because the dialog behind it used the same
gradient. The header also read the footer variable. Check these sections with
three different temporary header, body-background, and footer values when
verifying their variables. Each section has its own color choice; they do not
need to match.

The checkbox issue had a different cause. Native dark mode moved the checkmark
and partial-selection icon to positions that do not match theme.park's sprite.
Inspect both `background-image` and `background-position`, including the header
checkbox. A selected row class alone does not prove the checkmark is visible.

At a 390 by 400 viewport, the Add dialog in 25.2 and 26.3 scrolls with the page.
Its `.modal-body` is as tall as its contents. Scroll the footer into view and
check the document's scroll position rather than assuming the body will scroll.

Trial screenshots and browser results belong under
`dev/artifacts/nzbget/<issue-or-description>/`. For the modal investigation,
use `modal-colors`. Compare screenshots with the same native mode, theme, and
viewport. Record the app version separately because this setup can run either
25.2 or 26.3.

## Button hover checks

Hover Add and the other queue toolbar buttons, then open Add and hover Select
files, Cancel, and Submit. Open Edit download to check its tabs and footer.
In Messages, check the selected All filter as well as unselected filters.
In Settings, check the section controls and Save all changes. Open System to
hover Reload and Shutdown without clicking them. Move the pointer away again
and confirm the resting colors return. Hovering an action button
does not require clicking it or changing the queue or configuration.

The native dark rule `.btn-default:hover:not(.btn-active)` overrides the
theme's simpler `.btn:hover`. It sets the background to `#212529` and the text
to `inherit`. Match that selector in the shared theme hover rule so default
buttons use `--button-color-hover` and `--button-text-hover` across the app.
Keep the selected-button exclusion. Some Settings controls have their own
transparency or status colors, so do not assert that every button must have
the generic accent color.

Use actual pointer hover in browser automation, check both native modes, and
include Nord, Aquamarine, and Hotline. Save matching before/after screenshots
under `dev/artifacts/nzbget/button-hover/`. NZBGet can show an update dialog
asynchronously; close it before testing hover so it does not cover the target.
Settings can contain duplicate `Config_Save` IDs, so choose a visible instance
when automating that control.

### Play/pause icon hover

The large round status control is separate from `.btn`. Hover the orange
paused icon in `#PlayButton` and the green ready icon in `#PauseButton`.
`#PlayPauseButton` identifies only the orange control. Both use
`.PlayBlockInner` with a child sprite image.

Upstream hover rules move those images from row `-80px` to `-133px`. The
theme.park sprite has no button images at those hover positions, so the icons
disappear. Keep the green icon at `-113px -80px` and the orange one at
`-177px -80px` on hover. The native `opacity: 0.9` still gives hover feedback.

Check both states, both native modes, gradient and solid themes, and the narrow
layout. In this disposable setup, first confirm every sample download remains
individually paused. Toggle only the global download pause through JSON-RPC
`pausedownload` and `resumedownload` to expose both icons, then restore the
original state. The main button also changes post-processing and scanning, so
clicking it is not equivalent. Active transfers have a separate animation
layer and need an additional check if that layer is changed.

Record screenshots under `dev/artifacts/nzbget/play-pause-hover/`. When replacing
an app's sprite sheet, inspect the coordinates for every affected interaction
state. A correct image URL and a visible element do not prove that the selected
rectangle contains any pixels.

## Stopping the setup

Stop the setup with:

```sh
docker compose -f dev/nzbget/compose.yaml down
```

To discard this setup's disposable app configuration and queue as well, use
`docker compose -f dev/nzbget/compose.yaml down -v`.
