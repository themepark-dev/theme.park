# Ombi development

Run from the repository root:

```sh
docker compose -f dev/ombi/compose.yaml up -d
```

Open http://localhost:18085. The default image is
`lscr.io/linuxserver/ombi:version-v4.53.4`, the version reported in issue #715.
The app stores its SQLite databases in the Compose project's `config` volume.
The CSS server uses http://localhost:18868 and mounts this checkout read-only.
Check both ports before starting.

Complete the wizard with SQLite, skip the media server connection, and create a
local administrator. Choose your own password. No Plex, Sonarr, or Radarr server
is needed to inspect Customization or the Discover genre controls. Discover
loads public media metadata over the network. Its posters and ordering can
change between captures. Do not submit media requests during theme checks.

## Load local CSS

Ombi requires its built-in Custom CSS setting. Its
[theme documentation](https://docs.theme-park.dev/themes/ombi/) explicitly rules
out reverse-proxy subfilter injection.

Open Settings, Configuration, Customization, or navigate directly to
http://localhost:18085/Settings/Customization. Paste this into Custom CSS,
click Submit, and reload:

```css
@import url("http://localhost:18868/css/base/ombi/ombi-base.css");
@import url("http://localhost:18868/css/community-theme-options/catppuccin-latte.css");
```

For Nord, Aquamarine, or Hotline, replace the second import with
`http://localhost:18868/css/theme-options/<theme>.css`.
Confirm the browser loads both imports plus `css/defaults/placeholders.css`
and `css/defaults/transparent.css` from port 18868. The server sends
`Cache-Control: no-store`, so source edits appear after reloading.
The saved CSS applies to all users, including the login page. Separate browser
contexts still share this setting.

## Reproduce and check text colors

On 4.53.4, open `/discover` and inspect the genre buttons, the Combined, Movies,
and TV filters, and the profile name. Open `/Settings/Customization` to inspect
empty field labels, hints, field outlines, and focused or filled inputs.
`/Settings/Ombi` provides another use of the outlined Material fields. Avoid
publishing screenshots of its API key.

Ombi's component selectors add Angular attributes and set the Discover toggle
groups to white. The theme's group color needs to override that specificity.
The child toggles inherit the group color. Keep the selected filter's foreground
and background paired through `--button-text` and `--button-color`.

Material sets dark-mode field labels, hints, and outlines to translucent white.
Map outlined field labels and hints to theme text variables. Keep invalid and
disabled fields out of the normal label and outline selectors. The search bar
uses a different field appearance and should retain its existing rules.
Customization's URL inputs did not enter Angular's invalid state when given
malformed URLs, so they are not a useful validation-error test.

Use real pointer hover and click each filter. Test empty and filled fields,
focus, and a phone viewport with scrolling. Wait for imports, fonts, and color
transitions before screenshots. One early Firefox capture showed labels and
buttons mid-transition even though hints had reached their final colors.

The #715 checks used Chrome 142 and Firefox 155, with 1495 by 900 and 390 by 844
viewports. Chrome covered Catppuccin Latte, Nord, Aquamarine, and Hotline.
Firefox covered Latte. The app used its default native dark mode.

## Version differences and remaining defects

The 4.53.10 stable release already contains the redesigned navigation and
Discover components covered by the base CSS's section named "v5". Do not infer
the app version from that comment. The new Discover page has no
`.discover-filter-buttons-group` elements. Its Customization page still uses
the outlined Material fields and benefits from the same text fix.

The #715 patch fixes the reported v4 genre and filter labels, profile name,
and Customization labels, hints, and outlines. Other observed Latte defects
remain separate:

- In 4.53.4, card type labels use dark text over near-black poster strips.
- The unselected sidebar advanced-search icon is white on a light background.
- In 4.53.10, the hero uses dark text over dark artwork, and some Discover
  section headings and genre category labels remain white.
- Some theme accents and search-bar colors still have low contrast in Latte.

These checks do not establish full light-theme support across Ombi. Keep
run-specific screenshots and results under `dev/artifacts/ombi/`.

## Change versions or stop

To try another image:

```sh
OMBI_TAG=version-v4.53.10 docker compose -f dev/ombi/compose.yaml up -d ombi
```

Use disposable configuration for version comparisons. Back up a populated
volume before upgrading, since database migrations may prevent downgrading.
Check the running version with:

```sh
curl http://localhost:18085/api/v1/Status/info
```

Stop the task's services and retain configuration:

```sh
docker compose -f dev/ombi/compose.yaml down
```

To discard this test instance's configuration as well, add `--volumes`.
