# Docker Mods

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/gilbn/theme.park?style=for-the-badge)](https://hub.docker.com/r/gilbn/theme.park/builds)
[![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/gilbn/theme.park?color=blue&style=for-the-badge)](https://hub.docker.com/r/gilbn/theme.park)
[![Docker Pulls](https://img.shields.io/docker/pulls/gilbn/theme.park?color=blue&style=for-the-badge)](https://hub.docker.com/r/gilbn/theme.park)
[![GitHub](https://img.shields.io/github/license/gilbn/theme.park?color=blue&style=for-the-badge)](https://github.com/gilbN/theme.park/blob/master/LICENSE)
[![Discord](https://img.shields.io/discord/591352397830553601?color=blue&style=for-the-badge)](https://discord.gg/HSPa4cz)
[![](https://img.shields.io/badge/Blog-technicalramblings.com-blue?style=for-the-badge)](https://technicalramblings.com/)

## Docker mods for linuxserver.io containers to inject theme.park stylesheets.

Add -e `DOCKER_MODS=gilbn/theme.park:<app>` e.g. `gilbn/theme.park:sonarr`

These are the **default** values for all envs. So if you want to use the `organizr-dark` theme, you only need to add the `DOCKER_MODS` variable. 

| Environment Variable | Example Value | Description |
| -------------------- | ------------- | ----------- |
| `DOCKER_MODS` | `gilbn/theme.park:<app>` | Replace \<app> |
| `TP_DOMAIN` | `gilbn.github.io` | Defaults to the example. |
| `TP_THEME` | `organizr-dark` | Defaults to the example. |
| `TP_ADDON` | `radarr-4k-logo` | See wiki for more info on addons |



Applications that support Docker Mods installation.
 
| | | |
|----------------------------|------------------------------------|--------------------------------|
| [Sonarr][sonarr]           | [Transmission][transmission]       | [Deluge][deluge]               |
| [Radarr][radarr]           | [Calibre-web][calibreweb]          | [The Lounge][thelounge]        |
| [Lidarr][lidarr]           | [ruTorrent][rutorrent]             | [Portainer][portainer]         |
| [Bazarr][bazarr]           | [Synclounge][synclounge]           | [Lazylibrarian][lazylibrarian] |
| [Readarr][readarr]         | [Jackett][jackett]                 |                                |
| [Plex][plex]               | [Librespeed][html5speedtest]       |                                |
| [Jellyfin/Emby][jelly]     | [NZBGet][nzbget]                   |                                |
| [Tautulli][tautulli]       | [SABnzbd][sabnzbd]                 |                                |


[sonarr]: https://github.com/gilbN/theme.park/wiki/Sonarr
[radarr]: https://github.com/gilbN/theme.park/wiki/Radarr
[lidarr]: https://github.com/gilbN/theme.park/wiki/Lidarr
[readarr]: https://github.com/gilbN/theme.park/wiki/Readarr
[bazarr]: https://github.com/gilbN/theme.park/wiki/Bazarr
[plex]: https://github.com/gilbN/theme.park/wiki/Plex
[jelly]: https://github.com/gilbN/theme.park/wiki/Jellyfin-Emby
[ombi]: https://github.com/gilbN/theme.park/wiki/Ombi
[tautulli]: https://github.com/gilbN/theme.park/wiki/Tautulli
[organizr]: https://github.com/gilbN/theme.park/wiki/Organizr
[grafana]: https://github.com/gilbN/theme.park/wiki/Grafana
[sabnzbd]: https://github.com/gilbN/theme.park/wiki/SABnzbd
[nzbget]: https://github.com/gilbN/theme.park/wiki/NZBGet
[nzbhydra2]: https://github.com/gilbN/theme.park/wiki/NZBHydra-2
[deluge]: https://github.com/gilbN/theme.park/wiki/Deluge
[qbit]: https://github.com/gilbN/theme.park/wiki/qBittorrent
[guacamole]: https://github.com/gilbN/theme.park/wiki/Guacamole
[rutorrent]: https://github.com/gilbN/theme.park/wiki/ruTorrent
[netdata]: https://github.com/gilbN/theme.park/wiki/Netdata
[jackett]: https://github.com/gilbN/theme.park/wiki/Jackett
[html5speedtest]: https://github.com/gilbN/theme.park/wiki/Librespeed
[filebrowser]: https://github.com/gilbN/theme.park/wiki/Filebrowser
[monitorr]: https://github.com/gilbN/theme.park/wiki/Monitorr
[logarr]: https://github.com/gilbN/theme.park/wiki/Logarr
[plpp]: https://github.com/gilbN/theme.park/wiki/PLPP
[Synclounge]: https://github.com/gilbN/theme.park/wiki/Synclounge
[theLounge]: https://github.com/gilbN/theme.park/wiki/The-Lounge
[portainer]: https://github.com/gilbN/theme.park/wiki/Portainer
[lazylibrarian]: https://github.com/gilbN/theme.park/wiki/Lazylibrarian
[calibreweb]: https://github.com/gilbN/theme.park/wiki/Calibre-Web
[transmission]: https://github.com/gilbN/theme.park/wiki/Transmission
[requestrr]: https://github.com/gilbN/theme.park/wiki/Requestrr
[pihole]: https://github.com/gilbN/theme.park/wiki/Pi-hole
[adguard]: https://github.com/gilbN/theme.park/wiki/Adguard
[gaps]: https://github.com/gilbN/theme.park/wiki/Gaps
[bitwarden]: https://github.com/gilbN/theme.park/wiki/Bitwarden
[duplicacy]: https://github.com/gilbN/theme.park/wiki/Duplicacy
[kitana]: https://github.com/gilbN/theme.park/wiki/Kitana
[webtools]: https://github.com/gilbN/theme.park/wiki/Webtools
[resilio-sync]: https://github.com/gilbN/theme.park/wiki/Resilio-Sync
[gitea]: https://github.com/gilbN/theme.park/wiki/Gitea

***

### Hotio containers

The scripts in root\etc\cont-init.d will also work with containers made by Hotio. But you may need to change the path for the HTML file.

[https://hotio.dev/containers/sonarr/#executing-your-own-scripts](https://hotio.dev/containers/sonarr/#executing-your-own-scripts)
