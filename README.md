<h1 align="center">
    <img src="https://i.imgur.com/OkX6Zup.png">
</h1>
<p align="center">
  A collection of themes/skins for use in conjunction with <a href="https://github.com/causefx/Organizr/" target="_blank">Organizr</a> or standalone.
<p align="center">
<a href="https://www.buymeacoffee.com/oY5Nk8GHK" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" >   </a><a href="https://discord.gg/HM5uUKU" rel="noopener"><img class="alignnone" title="theme.park!" src="https://img.shields.io/badge/chat-Discord-blue.svg?style=for-the-badge&logo=discord" alt="" height="37" /></a>
 </a><a href="https://technicalramblings.com/" rel="noopener"><img class="alignnone" title="technicalramblings!" src="https://img.shields.io/badge/blog-technicalramblings.com-informational.svg?style=for-the-badge" alt="" height="37" /></a>
    <br />
    <br />
    <a href="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/ombi/ombi1.png" rel="noopener"><img src="/Screenshots/ombi/ombi1.png" alt="Screen Shot 1" width="49.15%" /></a>
    <a href="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sonarr/sonarr2.jpg" rel="noopener"><img src="/Screenshots/sonarr/sonarr2.jpg" alt="Screen Shot 2" width="49.15%" /></a>
    <a href="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/deluge/deluge1.png" rel="noopener"><img src="/Screenshots/deluge/deluge1.png" alt="Screen Shot 3" width="49.15%" /></a>
    <a href="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plex1.jpg" rel="noopener"><img src="/Screenshots/plexorg/plex1.jpg" alt="Screen Shot 4" width="49.15%" /></a>
</p>

# Themes

![](/Screenshots/aquamarine_banner.png)
![](/Screenshots/hotline_banner.png)
![](/Screenshots/spacegray_banner.png)
![](/Screenshots/dark_banner.png)
![](/Screenshots/plex_banner.png)

# Setup

All apps have 5 themes to choose from.
`https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/<THEME_NAME>.css`
```css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
Example: `https://gilbn.github.io/theme.park/CSS/themes/sonarr/dark.css`

As  most of these apps doesn't have support for custom CSS you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx or a browser addon called Stylus.

## Subfilter method
### Nginx
Add this to your reverse proxy:

```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/THEME.css">
</head>';
sub_filter_once on;
```
Where `APP_NAME` is the app you want to theme and `THEME.css` is the name of the theme. e.g. `aquamarine.css`

#### Example:
```nginx
location /sonarr {
    proxy_pass http://localhost:8989/sonarr;
    include /config/nginx/proxy.conf;
	proxy_set_header Accept-Encoding "";
	sub_filter
	'</head>'
	'<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/sonarr/plex.css">
	</head>';
	sub_filter_once on;
  }
```

### Apache (Untested)
```apache
AddOutputFilterByType SUBSTITUTE text/html
   Substitute 's|</head> '<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/THEME.css">
</head>';|'
  ```

#### Example:
```apache
<Location /sonarr>
    ProxyPass http://localhost:8989/sonarr
    ProxyPassReverse http://localhost:8989/sonarr
AddOutputFilterByType SUBSTITUTE text/html
   Substitute 's|</head> '<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/sonarr/plex.css">
</head>';|'
  </Location>
  ```

## Stylus method
Stylus is a browser extention that can inject custom css to the webpage of your choosing.

Add this in the style page:

```css
@import "https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/THEME.css";
```
Example:  `@import "https://gilbn.github.io/theme.park/CSS/themes/sonarr/dark.css";`

Link to Chrome extention: https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne?hl=en
Link to Firefox extention: https://addons.mozilla.org/en-US/firefox/addon/styl-us/

## Blackberry Theme Installer method
[Blackberry Themes](https://github.com/Archmonger/Blackberry-Themes) provides a easy to use method of using JS to theme your Organizr tabs. This will only work if your Organizr tab is on a subdirectory (does not work with subdomains). These themes will only be applied when viewed within Organizr.
```js
$.getScript('https://archmonger.github.io/Blackberry-Themes/Extras/theme_installer.js', function(){
    // First variable is your Organizr tab name. Second variable is a link to the theme you want to apply.
    themeInstaller("<TAB_NAME>","https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/<THEME_NAME>.css");

    // You can also use this for multiple themes at once by simply calling themeInstaller again!
    themeInstaller("<TAB_NAME>","https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/<THEME_NAME>.css");
});
```

## [Feature requests](https://feathub.com/gilbN/theme.park)
[![Feature Requests](https://feathub.com/gilbN/theme.park?format=svg)](http://feathub.com/gilbN/theme.park)

## Current themes in the repo:
<ul>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#sonarr-v2v3---radarr---lidarr---bazarr-themes">Sonarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themeshttps://github.com/gilbN/theme.park/wiki/Themes#sonarr-v2v3---radarr---lidarr---bazarr-themes">Radarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#sonarr-v2v3---radarr---lidarr---bazarr-themes">Lidarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#sonarr-v2v3---radarr---lidarr---bazarr-themes">Bazarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#plex-themes">Plex</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#jellyfin-themes">Jellyfin</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#ombi-themes">Ombi</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#tautulli-themes">Tautulli</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#organizr-hotline-and-marine-theme">Organizr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#grafana-themes">Grafana</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#sabnzbd-themes">Sabnzbd</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#nzbget-themes">Nzbget</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#nzbhydra2-themes">NZBHydra2</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#deluge-themes">Deluge</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#qbittorrent-themes">qBittorrent</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#guacamole-themes">Guacamole</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#rutorrent-themes">ruTorrent</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#netdata-themes">Netdata</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#jackett-themes">Jackett</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#html5-speedtest-themes">html5speedtest</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#filebrowser-themes">Filebrowser</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#monitorr-themes">Monitorr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#logarr-alpha-version-themes">Logarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#php-library-presenter-themes">PLPP</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#synclounge-themes">Synclounge</a></li>
<li><a href="https://github.com/gilbN/theme.park/wiki/Themes#the-lounge-themes">The Lounge</a></li>
</ul>


## Wiki [Adding your own theme colors](https://github.com/gilbN/theme.park/wiki/Creating-your-own-themes)
***

### Honourable mentions:

[Archmonger/Blackberry-Themes](https://github.com/Archmonger/Blackberry-Themes)

[leram84/layer.Cake](https://github.com/leram84/layer.Cake/)

[rg9400/Cloud-Tautulli-Theme](https://github.com/rg9400/Cloud-Tautulli-Theme)

[Burry/organizr-v2-plex-theme](https://github.com/Burry/organizr-v2-plex-theme)

[iFelix18/Darkerr](https://github.com/iFelix18/Darkerr)

[ydkmlt84/DarkerNZBget](https://github.com/ydkmlt84/DarkerNZBget)