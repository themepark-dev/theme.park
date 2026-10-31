# Local SABnzbd theme development

Run these commands from the repository root with Docker Compose and Python 3:

```sh
docker compose -f dev/sabnzbd/compose.yaml up -d
python3 dev/sabnzbd/seed.py
```

Open http://localhost:18080. There is no login. SABnzbd's login is optional
and this setup leaves it off. The API key is `themeparkdevapikey00000000000000`.

The LinuxServer image loads the theme.park Docker mod, which adds stylesheet
links pointing at http://localhost:18766. That CSS server mounts this checkout's
`css` and `resources` read-only and sends `Cache-Control: no-store`. Edit
`css/base/sabnzbd/sabnzbd-base.css` and refresh. The default theme is
Aquamarine. The docs require Glitter Light, and `sabnzbd.ini` sets it.

## Sample data

`init-config.sh` copies `sabnzbd.ini` into the config volume on first start.
That skips the setup wizard and adds two news servers, both running
`fake_nntp.py`:

| Server | Priority | Behavior |
| --- | --- | --- |
| `fake-nntp-serve` | 0 | Returns a 16 KiB yEnc body for every article. Message IDs containing `missing` get `430 no such article`. |
| `fake-nntp` | 1, optional | Answers every connection with `502 connection limit (50) reached`, which SABnzbd logs as a warning. |

`seed.py` takes about a minute. It adds three jobs:

- `themepark-complete` downloads and lands in History as Completed.
- `themepark-missing` has only missing articles and lands in History as Failed.
- `themepark-queued` is 6 MB and stays paused in the queue for the Files modal.

SABnzbd keeps warnings in memory, so recreating the container clears them.
Run `python3 dev/sabnzbd/seed.py --warnings` to bring them back without adding
History rows. It turns `fake-nntp` on, queues a throwaway job until a warning
appears, deletes the job, and turns the server off again.

Turning the server off matters. After a 502, SABnzbd ignores that server for
5 to 10 minutes but keeps waiting for it before failing an article. A job with
missing articles stays in the queue until the server is disabled. The server
settings API is `mode=set_config&section=servers&keyword=fake-nntp&enable=0`.
`mode=config&name=set_config` returns "not implemented" for servers.

Keep queue jobs above roughly 0.01 MB. Glitter treats a job with `mb` of
0.00 as still grabbing and will not open its Files modal. LinuxServer prints a
"not owned by root" notice for `/custom-cont-init.d` because the script is
bind-mounted from the checkout. It still runs.

## Themes and versions

Change the theme or app version by recreating the app container, then restore
the warnings:

```sh
TP_THEME=nord docker compose -f dev/sabnzbd/compose.yaml up -d sabnzbd
python3 dev/sabnzbd/seed.py --warnings
TP_THEME=catppuccin-latte TP_COMMUNITY_THEME=true docker compose -f dev/sabnzbd/compose.yaml up -d sabnzbd
SABNZBD_TAG=<tag> docker compose -f dev/sabnzbd/compose.yaml up -d sabnzbd
```

Wait until the page source links the new theme file before running scripts.
The mod downloads again on every recreate. The default tag is `latest`. On
2026-10-31 it ran SABnzbd 5.1.3. Check `/api?mode=version` and record the
version with any results.

## Browser checks

Run the scripts with a Playwright install, for example
`uv run --with playwright python dev/sabnzbd/sweep.py ...`.

`sweep.py OUTDIR LABEL` turns on Glitter's tabbed layout and screenshots 29
states: the Queue, History and Warnings tabs, the row details dropdowns, the
navbar menus, every Glitter modal and each Config page. Pass `--states` to run
a subset. It prints visible elements with a light opaque background or a
bright border, which is how unmapped Glitter colors show up on dark themes.
On a light theme most of that list is noise. The list also misses contrast
problems such as dim icons, so read the screenshots too. The RSS page always
reports `tr.even` with a light border that the browser does not draw.

`check_warnings.py OUTDIR LABEL [WIDTH HEIGHT]` screenshots the Warnings tab
at rest and with a real pointer on the first warning, and prints the row colors.

The sweep opens modals with Bootstrap's `$(...).modal('show')` and clicks with
jQuery, so it does not test hover. Use a real pointer for hover states. The
Files icon in a queue row sits under the job name until the row is hovered,
so a Playwright click on it times out. The sweep calls `click()` on the
`showFiles` link from page JavaScript instead.

## Glitter 5 colors

SABnzbd 5 moved Glitter's colors into `--clr-*` variables at the top of
`glitter.css`, defined with `light-dark()`. theme.park maps them in the
`:root` block of the base CSS. A variable left unmapped keeps Glitter
Light's value, which shows as a white or gray patch on dark themes.
When a SABnzbd release changes `glitter.css`, compare its `--clr-*` list with
the base CSS `:root` block before chasing individual selectors.

Fixed on 5.1.3, verified on all 11 official theme options:

| Symptom | Cause | Fix |
| --- | --- | --- |
| White even rows in Warnings and the Files modal, with light text on them | Glitter 5 stripes every `.table`. Even rows use `--clr-table-bg`, which was unmapped (`#F5F5F5`). Queue and History only looked right because of their own `!important` row rules. | `--clr-table-bg: transparent` |
| Gray license text in Help and other secondary text | `--clr-text-muted` was unmapped (`#888888`). | Map it to `--text-muted`. |
| Warnings X buttons nearly invisible | Glitter dims `.hover-button` to 30%. theme.park colored it with the accent on a `--transparency-light-25` strip. | Dark strip, `--text` at 80%, accent on hover. |
| 3px white lines between rows in the Files modal | Glitter hardcodes `border-bottom: 3px solid white` on `.item-files-table td`. | Transparent border color. |
| White box behind the Help modal links | Glitter hardcodes `background-color: white` on `#modal-help table td`. | Transparent table and cells. |
| Flat gray disabled selects (Scripts in Add NZB and the queue row details) | theme.park's own `.form-control[disabled]` rule used `#919191`. | `--transparency-dark-25` at 50% opacity. Readonly stays at full opacity. |
| White line above modal footers (Pause for…, Purge History) | Bootstrap's `#e5e5e5` footer border. | `--transparency-light-20`. |
| Light line on top of accent `hr` separators (Categories, Help) | Bootstrap's `#eee` top border sits on theme.park's accent bottom border. | Transparent top border. |

Left alone on purpose: the empty Category, Priority and Processing selects in
Add NZB are Glitter's "use default" option with no label. `--clr-error`,
`--clr-progress-track` and `--clr-toggle-inactive` are still Glitter's values.
The error red is a status color, the base CSS already overrides `.progress`,
and the gray toggle track reads as "off" on every theme checked.

## Stopping the setup

```sh
docker compose -f dev/sabnzbd/compose.yaml down
```

Add `-v` to discard the config volume, queue, history and warnings as well.
