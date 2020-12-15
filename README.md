# Docker Mods

## Docker mods for linuxserver.io containers to inject theme.park stylesheets.

Add -e `DOCKER_MODS=gilbn/theme.park:<app>` e.g. `gilbn/theme.park:sonarr`

These are the **default** values for all envs. 

| Environment Variable | Example Value | Description |
| -------------------- | ------------- | ----------- |
| `DOCKER_MODS` | `gilbn/theme.park:<app>` | Replace \<app> |
| `TP_DOMAIN` | `gilbn.github.io` | Defaults to the example. |
| `TP_THEME` | `organizr-dark` | Defaults to the example. |

