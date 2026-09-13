# Bazarr CSS development

Run commands from the repository root. This setup uses LinuxServer's image and
[the documented Docker mod](https://docs.theme-park.dev/setup/#docker-mods).
Follow the [Bazarr theme instructions](https://docs.theme-park.dev/themes/bazarr/)
and select Bazarr's native dark appearance in Settings > UI.

## Start and populate

```sh
docker compose -f dev/bazarr/compose.yaml up -d
```

Wait for Bazarr to start at <http://localhost:16767>. The mod injects stylesheets
from <http://localhost:18965>, served directly from this checkout. Refresh after
editing `css/base/bazarr/bazarr-base.css`. No SSH or remote CSS host is needed.
The browser must be on the machine that publishes these loopback ports.

After the first startup, populate the disposable configuration volume:

```sh
docker compose -f dev/bazarr/compose.yaml stop bazarr
docker compose -f dev/bazarr/compose.yaml run --rm seed
docker compose -f dev/bazarr/compose.yaml start bazarr
```

The fixture enables the series/movie pages and dark appearance, disables
analytics, and adds 35 series, 105 episodes, 35 movies, subtitle history and an
English/Norwegian profile. It creates no media files and connects to no Sonarr,
Radarr or subtitle-provider account. Connection health warnings are expected.
Do not configure real services in this instance. Run the seed only while Bazarr
is stopped and only against this development volume. It refuses libraries with
paths outside `/themepark-fixtures/`.

## Versions, themes and add-ons

The default image tag is `latest`, matching the maintainer's installation.
Record the resolved build before testing because the tag changes:

```sh
docker image inspect lscr.io/linuxserver/bazarr:latest --format '{{index .Config.Labels "build_version"}} {{index .RepoDigests 0}}'
```

Set `BAZARR_TAG=version-v1.4.4` to test the first release reported broken in
[issue 658](https://github.com/themepark-dev/theme.park/issues/658). Use a fresh
configuration volume for each older version. Do not downgrade a newer database.
The seed supports the subtitle tables in both 1.4.4 and 1.6.0.

Maroon is the default theme because it exposes partial theming clearly.
For another theme or the optional add-ons:

```sh
TP_THEME=nord docker compose -f dev/bazarr/compose.yaml up -d bazarr
TP_ADDON='bazarr-darker|bazarr-4k-logo' docker compose -f dev/bazarr/compose.yaml up -d bazarr
```

Use `TP_COMMUNITY_THEME=true` with a name from `css/community-theme-options`.
Keep the same environment values on later `up` commands if you want to retain
them. Browser-only theme switching is useful for comparisons; reload through
the normal mod injection for the final check.

## Inspection paths

- Series and Movies: table links, subtitle badges, row hover, pagination, wrench
  editor, Mass Edit checkboxes and profile selector. The fixture spans two pages.
- Series > Sample series 01: episode groups, missing/present subtitles, Edit
  Series, Upload, manual search and episode history dialogs.
- Movies > Sample movie 01: missing subtitles and Edit Movie. Sample movie 02
  also has an existing subtitle for subtitle tools and deletion confirmation.
- Settings > Languages: multi-select pills, Add New Profile, validation errors,
  Add Language and switches. Profile removal changes the staged settings without
  a confirmation dialog; leave the page without saving after checking it.
- Settings > Providers: click the plus card, select OpenSubtitles.com, inspect
  the password field and switches. No account credentials are needed for this.
- History > Statistics: chart axes, legend and tooltip. Preserve series/movie
  colors. System > Status, Tasks and Logs exercise other tables and messages.
- Header: search suggestions, system menu and Jobs Manager drawer. Opening the
  menu is sufficient; do not trigger restart/shutdown to test its styling.

Check Nord, Aquamarine, Hotline and Plex, plus Maroon from the issue. For broad
component changes, check every built-in palette. Compare modal body, header and
footer against their separate variables. Temporarily give those three variables
different values if the selected palette uses identical ones.
On phones, test the navigation overlay and scroll the language-profile dialog
to its Save button. Confirm the scroll container actually moved.

## Findings from issue 658

Bazarr 1.4.4 uses Mantine 7; 1.6.0 uses Mantine 9. Both expose stable
`mantine-Component-part` classes even though Bazarr's custom styles have generated
module names. Prefer the public classes and state attributes. The old
`bazarr-*` rules remain for pre-1.4.4 installations.

The toolbar and provider card lack public classes of their own. Their overrides
match the `_group_` or `_card_` module-name prefix within the main area. Recheck
those two selectors when Bazarr changes the component source. Do not copy hash
suffixes such as `_13q4v_32` into production CSS.

Mantine defines `--button-color` locally for text, colliding with theme.park's
background variable. Resolve the theme's value at the document root into
`--bazarr-button-background`, then use that alias on buttons. Inspect both the
variable's value and where it is defined before diagnosing a transparent or
white button. Check real hover, disabled controls and red destructive actions.

Keep warning, highlight and disabled subtitle badges distinct. Inline status
colors on action icons must survive the generic icon rules. Mantine's native
display rules also expose some controls marked `hidden`, including the new
provider's Disable button and the zero-change badge. The base CSS restores the
hidden state for those controls.

Most dialogs have a content shell and a header. Item editors and provider
settings put their footer actions in the final Group inside the body Stack.
The language-profile dialog ends with a standalone Save button instead. Avoid
styling every Group or every final button as a modal footer.

Save screenshots, DOM captures, downloaded upstream source and detailed check
results under `dev/artifacts/bazarr/<issue>/`. Keep these out of commits.
Actual subtitle downloads, authentication and external integrations require
separate functional checks; the fixture covers their available UI controls.

## Stop or discard

```sh
docker compose -f dev/bazarr/compose.yaml down
```

Add `--volumes` only when discarding this disposable database. CSS edits remain
in the checkout.

## Validation on 2026-09-14

LinuxServer `latest` resolved to Bazarr `1.6.0-ls363`, built 2026-09-08.
Bazarr 1.4.4 was checked in a separate container and configuration volume.
Both used the real Docker mod with local CSS and native dark appearance.

Firefox 155 passed checks for all 11 built-in palettes on both versions,
including header backgrounds, button text/background/hover, modal body, header,
footer and dropdown backgrounds. Screenshots were inspected for contrast and
layout. Chromium 152 in the T3 preview was also checked on series details and
the editor modal.

The current version also passed disabled-button hover, validation errors,
checkbox selection, pagination, provider fields, upload metadata, manual-search
layout, chart tooltips and separate temporary modal colors. The 390px phone
layout had no document-width overflow; navigation and a scrolled profile editor
were checked. Both add-ons loaded through Docker-mod injection. The production
`minify@7.2.2` output passed the Maroon button/modal checks.

No subtitle download, upload submission, real media scan or external account
connection was performed. Pre-1.4.4 selectors were retained but that frontend
was not retested. Native light appearance and every community palette were not
part of this check.
