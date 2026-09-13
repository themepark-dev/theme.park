# Local theme development

Use the setups in this folder to reproduce CSS bugs and develop app themes.
Follow the [theme.park setup guide](https://docs.theme-park.dev/setup/) and the
app's instructions in [tp-docs](https://github.com/themepark-dev/tp-docs).
Record the local startup commands and verification steps in `dev/<app>/README.md`.

## Current setup

The [NZBGet setup](nzbget/README.md) uses Compose to run the official app Docker
mod with local CSS. Its seed script creates paused dummy downloads.

[serve.py](serve.py) uses Python's standard HTTP server and adds
`Cache-Control: no-store`. The Compose service mounts the checkout's CSS and
resources read-only. File edits appear on refresh without a build.

There is no shared nginx proxy or theme.park image setup yet. Add and test one
when an app task needs it, using the guidance below.

## Choose hosting and injection separately

The CSS host serves stylesheets. The injection method makes the app load them.
The theme.park image handles hosting. The app still needs a way to load the CSS.

| CSS host | When to use it |
| --- | --- |
| Local Python server | Edit source CSS and refresh the app. Load the app base CSS followed by the chosen theme option. |
| theme.park Docker image | Check packaged files, generated theme URLs, startup, or subfolder handling. Build from the checkout to test local edits. |

The documented image is `ghcr.io/themepark-dev/theme.park`. See the
[Docker setup](https://docs.theme-park.dev/setup/#docker) for tags, ports,
configuration, and `TP_URLBASE`. A pulled release image does not contain edits
in this checkout.

The current [image startup script](../docker/root/etc/s6-overlay/s6-rc.d/init-themepark/run)
copies bundled files from `/app/themepark` into `/config/www`, runs `themes.py`,
and changes configuration ownership. Use disposable configuration when testing
the image. Do not mount the working checkout at `/config/www`. Startup can
overwrite its files or change their ownership. Rebuild after editing files,
or set up and verify a way to copy those edits into the test container.

The image's [nginx configuration](../docker/root/defaults/nginx/site-confs/default.conf)
disables caching and rewrites asset paths for its subfolder endpoint.
The Python server does neither subfolder rewriting nor theme generation.
When editing source CSS, link the base stylesheet and theme option separately.
To test a generated `<app>/<theme>.css` URL, generate wrappers in a temporary
directory or use the image. Confirm the browser loads every imported file.

| Documentation marker | Injection method |
| --- | --- |
| 🐳 | LinuxServer Docker mod, configured to load the local CSS host. |
| 🔥 | Documented Hotio/S6 startup script mount; do not assume `DOCKER_MODS` works. |
| ⚙️ | The app's built-in CSS setting, using locally served styles. |
| No method marker | Local reverse proxy using the subfiltering guide. |
| ⚠️ | Read the app-specific setup requirements in addition to the chosen method. |

Reproduce the reporter's installation method where supported. You can try
styles in the browser during investigation. Verify the final files through
the chosen installation method after reloading the page.

## Local reverse proxy

Use an nginx container on the application's Compose network. The browser opens
the proxy's loopback-bound port. Nginx forwards requests to the app's service
name and internal port. Stylesheet links must use an address the browser can
reach. Docker service names usually resolve only inside Docker networks.
Inside the nginx container, `localhost` refers to that container.

Follow the [nginx subfilter recipe](https://docs.theme-park.dev/setup/#nginx):
request uncompressed upstream content, inject once, and keep injection out of
API locations. Start with the app and CSS host on separate ports
so their `/css` and `/resources` paths do not collide.

Make the injection point and proxy exceptions app-specific. For example,
[Sonarr](https://docs.theme-park.dev/themes/sonarr/) documents `</body>` injection.
Other apps may need CSP adjustments or a separate unbuffered API location.
Apply exceptions only where required by the app's documented setup. Verify
login, redirects, and stylesheet order in the running app. Check streaming and
WebSockets if the app uses them. Use the app's documented injection point.

## Workflow for an app task

Start a task branch from freshly fetched `origin/develop` and merge the finished
work back into `develop`. Use `testing` only for potentially breaking changes
that could disrupt users of `develop`. Ordinary fixes do not need to pass
through `testing`; disruption for users of that branch is accepted.
The maintainer's explicit authorization is still required before pushing or
publishing changes.

1. Read the report and docs. Record the app version, injection method, theme,
   browser, viewport, and steps needed to reach the problem.
2. Reuse `dev/<app>`. If absent, add a minimal Compose file and README. Record
   the image tag, local ports, dependencies, setup and login steps, injection
   method, and commands to stop or reset the app. Check occupied ports before starting.
3. Give the test instance its own configuration. Add dummy data or a seed script
   when an empty installation cannot display the affected screen. Keep real
   credentials and private data out of tracked files. If an app needs an
   existing instance or user-provided access, record that requirement.
4. Confirm local CSS and assets load, reproduce the bug, and capture the
   original appearance before editing. Record unrelated existing defects.
5. Inspect DOM and computed styles, compare upstream changes when useful, and
   make the smallest appropriate source change using theme variables.
6. Reload through the real injection method. Exercise relevant states such as
   hover, focus, selection, dialogs, and empty/populated views. Check native
   light/dark modes where supported. Use the background checks below to choose
   theme options, plus a light community palette when relevant. Include the reported browser and
   responsive layout where practical. Record any substitutions.
7. Inspect screenshots as well as computed styles. For shared CSS changes,
   check other apps that import it. Run relevant generation and build checks
   in a temporary directory.
8. Record the cause, patch, image tag, app version, browser,
   theme, viewport, reproduction steps, evidence, and gaps. Store screenshots
   and run-specific results under ignored `dev/artifacts/<app>/<issue>/`.
   Put reusable setup instructions in `dev/<app>/README.md`.
9. Keep PR descriptions short and apply the `unslop` skill. State the fixes and
   relevant validation. Before/after screenshots can be attached but are not
   mandatory for bug-fix PRs; keep local visual evidence for verification.
10. Leave changes local for review. Report which test services remain running
   and how to stop them. Stop only services created for the task. Delete saved
   configuration only when resetting the test instance. Never push or deploy without
   the maintainer's explicit instruction.

For a new theme.park application, also add the app base stylesheet,
any required resources, and the appropriate documentation/navigation entries in
`tp-docs`. Follow [CONTRIBUTING.md](../.github/CONTRIBUTING.md), including screenshots
of all official theme options. Adding a local environment for an already
supported app does not require adding another application theme.

## Older issues and UI replacements

Record the issue date and reported app version separately. When the report
omits a version, do not infer an exact release from its date or screenshot.
Check the current stable release, its UI migration notes, and the history of
the app's base CSS before writing selectors for an old screenshot.

Run the current app with its native CSS and with the existing theme. Compare
the affected component plus other main screens. Distinguish a missing selector
from a replaced component system. Inspect the current DOM, framework, and color
variables. Zero matches for old selectors are evidence for the inspected
screens, not proof that those selectors are unused on every supported version.

If the UI was broadly rebuilt, report whether support needs a theme rebuild
instead of a small bug fix. Explain the broken areas, reusable styling hooks,
and verification scope. Let the maintainer decide whether that investment fits
continued support. Do not silently deprecate the app or present a partial
sidebar patch as restored support. Keep the working local setup and findings
available for that decision.

## Background checks

Test background types as well as colors. Use at least these cases when changing
backgrounds, transparency, dialogs, or panels:

| Theme | What it checks |
| --- | --- |
| Nord | Solid colors, including distinct modal body and header/footer colors. |
| Aquamarine | A radial page gradient and a linear modal gradient. |
| Hotline | A linear page gradient with a different direction from its modal gradient. |
| Plex, when layers matter | Several page gradients with a solid fallback color. |

Read the component's variables before testing. A radial page background does
not imply a radial modal background. If no existing option exercises the value
needed for a check, use a temporary custom option and label it in the results.

Variables such as `--main-bg-color` and `--modal-bg-color` can contain a full
background declaration, including an image, position, size, repeat, and
attachment. Use `background` to accept that value. `background-color` accepts
only a color, while `background-image` cannot accept the extra background
settings. A declaration with an incompatible variable can fail after variable
substitution even though the browser parsed the stylesheet.

Inspect the visible element and its children. A solid child panel can cover the
correct gradient on its parent. Compare the dialog shell, body, header, and
footer separately. The header, body background, and footer can each have a
different color or gradient. Verify each against its own variable; matching
colors are not a requirement. If a theme gives them identical values, test with
three distinct temporary values to expose accidental variable substitutions.
Check text contrast and borders in each section.
Resize and scroll the dialog to catch gradient seams, repeated backgrounds,
or transparent areas that reveal the page instead of the dialog.
Check which element actually scrolls. A phone layout may scroll the document
instead of the modal body. Confirm that the scroll position changed.

Wait for stylesheet loads, fonts, and modal animations before taking screenshots.
When switching themes in the browser, reload the final setup through its normal
injection method as well. Inspect the screenshots after the computed-style checks.

For hover bugs, move a real browser pointer onto the control. Dispatching a
`mouseover` event from JavaScript does not activate CSS `:hover`. Compare the
background and text before hover, during hover, and after moving away. Inspect
the winning selectors, including classes inside `:not()`, before adding
specificity or `!important`. Check other uses of the same button class and keep
selected, disabled, and status-colored controls distinguishable.
Include custom controls such as clickable icon containers in the inspection;
an app's shared `.btn` rules may not cover them. For sprite icons, check both
the image URL and the rectangle selected by each state's background position.

## Defects found while investigating

App updates often affect more than the component named in an issue. Inspect
nearby controls and at least one other use of a shared component. Keep a short
record of each additional defect, its reproduction steps, and whether it is
part of the current fix. Tell the maintainer about remaining defects rather
than treating them as covered by the original issue.

Save reusable navigation and debugging notes in the app README. Keep screenshots
and detailed results in the ignored artifact directory. A useful note names the
element, the rule that caused the problem, and the checks that exposed it.

## Publishing development files

The Pages workflow publishes the repository root and excludes `dev` and
`AGENTS.md` from all three deployment branches. This also excludes local
artifacts nested under `dev`. Keep those exclusions when changing deployment
steps; Git ignore rules alone do not control the published files.
The application Dockerfiles copy specific asset paths, which exclude these
development files. Keep tooling changes separate from CSS fixes for review.

## Component libraries and CSS modules

Bazarr's Mantine update replaced the old `bazarr-*` classes, but retained public
classes such as `mantine-Button-root`. Check the app's theme provider and rendered
DOM before treating generated CSS-module names as a support blocker. Prefer
public component classes, state attributes and semantic containers. Document any
module-name prefix you still need in the app README.

Check for collisions between theme variables and the component library's local
variables. Bazarr's `--button-color` means text color in Mantine and background
color in theme.park. A theme alias resolved at the document root avoids the
component's local override. Test normal, hover and disabled states after changing
variable mappings, and preserve explicit status colors.
