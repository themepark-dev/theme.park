<h1 align="center">
    <img src="https://i.imgur.com/OkX6Zup.png">
</h1>
<p align="center">
  A collection of themes/skins for use in conjunction with <a href="https://github.com/causefx/Organizr/" target="_blank">Organizr</a> or standalone.
<p align="center">
<a href="https://www.buymeacoffee.com/oY5Nk8GHK" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" >   </a><a href="https://discord.gg/HM5uUKU" rel="noopener"><img class="alignnone" title="theme.park!" src="https://img.shields.io/discord/591352397830553601.svg?style=for-the-badge&logo=discord" alt="" height="37" /></a>
 </a><a href="https://technicalramblings.com/" rel="noopener"><img class="alignnone" title="technicalramblings!" src="https://img.shields.io/badge/blog-technicalramblings.com-informational.svg?style=for-the-badge" alt="" height="37" /></a>	
    <br />
    <br />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3.png" alt="Screen Shot 1" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana-1.png" alt="Screen Shot 2" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plexorg.png" alt="Screen Shot 3" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plpp/plpp.png" alt="Screen Shot 4" width="49.15%" />
</p>

# Setup

All apps have 4 themes to choose from. 
`https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/<THEME_NAME>.css`
```
aquamarine.css
hotline.css
dark.css
plex.css
```
Example: `https://gilbn.github.io/theme.park/CSS/themes/sonarr/dark.css`

As  most of these apps doesn't have support for custom CSS you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx or a browser addon called Stylus.

## Subfilter method
### nginx
Add this to your reverse proxy:

```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/THEME.css">
</head>';
sub_filter_once on;
```
Where `THEME.css` is the name of the theme. e.g. `aquamarine.css`

Here is a complete example:

<details><summary>Expand</summary>

```nginx
# REDIRECT HTTP TRAFFIC TO https://[domain.com]
server {
    listen 80;
    server_name ombi.domain.com;
    return 301 https://$server_name$request_uri;
}
server {  
    listen 443 ssl http2;
    server_name ombi.domain.com;

#SSL settings
    include /config/nginx/ssl.conf

location / {
    proxy_pass http://192.168.1.2:8701;
    include /config/nginx/proxy.conf;
	proxy_set_header Accept-Encoding "";
	sub_filter
	'</head>'
	'<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/ombi/plex.css">
	</head>';
	sub_filter_once on;
  }
}
```
</details>

### Stylus method
Stylus is a browser extention that can inject custom css to the webpage of your choosing. 

Add this in the style page:

```css
@import "https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/THEME.css";
```
Example:  `@import "https://gilbn.github.io/theme.park/CSS/themes/sonarr/dark.css";`

Link to Chrome extention: https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne?hl=en
Link to Firefox extention: https://addons.mozilla.org/en-US/firefox/addon/styl-us/

## [Feature requests](https://feathub.com/gilbN/theme.park)
[![Feature Requests](https://feathub.com/gilbN/theme.park?format=svg)](http://feathub.com/gilbN/theme.park)

## Current themes in the repo: 
<ul>
<li><a href="https://github.com/gilbN/theme.park#sonarr-v2v3---radarr---lidarr---bazarr-themes">Sonarr</a></li>
<li><a href="https://github.com/gilbN/theme.park#sonarr-v2v3---radarr---lidarr---bazarr-themes">Radarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#sonarr-v2v3---radarr---lidarr---bazarr-themes">Lidarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#sonarr-v2v3---radarr---lidarr---bazarr-themes">Bazarr</a></li>
<li><a href="https://github.com/gilbN/theme.park#plex-themes">Plex</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#ombi-themes">Ombi</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#organizr-hotline-and-marine-theme">Organizr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#grafana-themes">Grafana</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#sabnzbd-themes">Sabnzbd</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#nzbget-themes">Nzbget</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#guacamole-themes">Guacamole</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#netdata-themes">Netdata</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#jackett-themes">Jackett</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#html5-speedtest-themes">html5speedtest</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#filebrowser-themes">Filebrowser</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#monitorr-themes">Monitorr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#logarr-alpha-version-themes">Logarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#php-library-presenter-themes">PLPP</a></li>
</ul>

***
# Organizr Hotline and Marine theme
Custom [Organizr](https://github.com/causefx/Organizr/) themes.
<p align="center">
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-hotline-theme2.png" alt="Screen Shot 1" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-marine-theme2.png" alt="Screen Shot 2" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-hotline-theme-login.png" alt="Screen Shot 3" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-marine-theme-login.png" alt="Screen Shot 4" width="49.15%" />	
</p>

These themes are still a WIP so bugs may occur. Please make an issue if you find one.
Aquamarine are the colors from https://heimdall.site that I fell in love with.
All themes are highly customizable in regards of which radial gradient color combination you want. 

#### Installation: Themes can be found in the "Theme Marketplace" in Organizr.

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-hotline-theme.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-hotline-theme-login.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-marine-theme.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/organizr-themes/organizr-marine-theme-login.png"></img>
</p>
</details>

***
# Ombi Themes

**Install by adding `@import "https://gilbn.github.io/theme.park/CSS/themes/ombi/THEME_NAME.css";` in custom css**

```
https://gilbn.github.io/theme.park/CSS/themes/ombi/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

***
# Jackett Themes

```
https://gilbn.github.io/theme.park/CSS/themes/jackett/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

***
# PHP Library Presenter Themes

Custom [PLPP](https://github.com/Tensai75/plpp) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plpp/plpp.png)

```
https://gilbn.github.io/theme.park/CSS/themes/plpp/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

***
# Guacamole Themes

Custom [Guacamole](https://guacamole.apache.org/) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guacorg.png)

```
https://gilbn.github.io/theme.park/CSS/themes/guacamole/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guac-1.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guac-2.png"></img>
</p>
</details>

***

# Plex Themes

Custom [Plex](https://plex.tv) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plexorg.png)

```
https://gilbn.github.io/theme.park/CSS/themes/plex/XXX.css
aquamarine.css
hotline.css
dark.css
```

***

# Sonarr v2/v3 - Radarr - Lidarr - Bazarr Themes

Custom [Sonarr V2 and V3](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr)/[Lidarr](https://github.com/Lidarr/Lidarr)/[Bazarr](https://github.com/morpheus65535/bazarr) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3.png)

```
https://gilbn.github.io/theme.park/CSS/themes/sonarr/XXX.css
https://gilbn.github.io/theme.park/CSS/themes/radarr/XXX.css
https://gilbn.github.io/theme.park/CSS/themes/lidarr/XXX.css
https://gilbn.github.io/theme.park/CSS/themes/bazarr/XXX.css
aquamarine.css
hotline.css
plex.css
dark.css
```

Thank you iFelix18 for doing all the hard work on v2! :)

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3-2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3-3.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/1.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/2.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/3.jpg"></img>

</p>
</details>

***

# NZBGet Themes

Custom CSS for [Nzbget](https://github.com/nzbget/nzbget)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget-split.png)

```
https://gilbn.github.io/theme.park/CSS/themes/nzbget/XXX.css
aquamarine.css
hotline.css
plex.css
dark.css
```

Thank you [ydkmlt84](https://github.com/ydkmlt84) for making the job easier :)

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget1.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget2.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget-split-2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget3.png"></img>
</p>
</details>

***

# SABnzbd Themes

Custom CSS for [SABnzbd](https://github.com/sabnzbd/sabnzbd)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd.png)

```
https://gilbn.github.io/theme.park/CSS/themes/sabnzbd/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

**Note: SABnzbd theme must be set to `Glitter`**

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd_dark_2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd_dark_3.png"></img>
</p>
</details>

***

# Grafana Themes

Custom [Grafana](https://github.com/grafana/grafana) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration and consistent UI.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana-1.png)

```
https://gilbn.github.io/theme.park/CSS/themes/grafana/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
organizr-dashboard.css
```

#### For panel integration on the Organizr homepage you can use `organizr-dashboard.css` if you use the Plex theme in Organizr. The theme is an "internal" theme that is meant to be used in an Organizr iframe as the background is set to transparent.
NOTE: When viewing Grafana in Organizr iframe using `organizr-dashboard.css` it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect. If you don't want this you can create two reverse proxies. One for grafana organizr homepage integration and one for the regular grafana theme. 

### Check out https://technicalramblings.com/blog/spice-up-your-homepage-part-ii/

![](https://technicalramblings.com/wp-content/uploads/2019/01/orgdash.jpg)

### **TIP:**
Click the `kiosk` button and use that link if you don't want to show the top bar and side bar inside Organizr! There are two modes, one where the side menu and variables ect disappear and one where just the panels are visible.

![](https://i.imgur.com/pVSKUzi.png)

Check out my Varken dashboard here: https://grafana.com/dashboards/9558

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/1.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/2.jpg"></img>
</p>
</details>

### Custom HTML for Organizr Homepage


![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/3.jpg)

<details><summary>Expand</summary>

Thank you [Fma965](https://gist.github.com/Fma965) for the base [code](https://gist.github.com/Fma965/d30ac1fa5695304a7d6dcdc748220027)

Change the ***Panel name*** to what you want and the ***src*** to the panel URL.

```css
<h5><span>Panel name</span></h5>
  <div class="overflowhider"><embed id="grafanadwidget1" src='https://graforg.domain.com/panel-embed-link'/>**
```
The URL can be found by clicking **share** on the panel you want to add.

<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/4.png"></img>

If you dont want the ***Panel name*** text, just remove the `<h5><span>` line entirely.

```css
<style>
.flex {
  	display: flex;
  	flex-wrap: wrap;
 	align-items: center;
  	justify-content: center;
	background: transparent;
	margin-top:10px;
	box-shadow: none !important;
}
.flex-child {
	flex: 1 1 1 1;
	padding: 1px 1px 1px 1px;
}
#flex-grafanadwidget1 {
	min-width: 25%;
}
#flex-grafanadwidget2 {
	min-width: 25%;
}
#flex-grafanadwidget3 {
	min-width: 25%;
}
#flex-grafanadwidget4 {
	min-width: 25%;
}
@media only screen and (max-width: 1374px) {
    #flex-grafanadwidget1, #flex-grafanadwidget2, #flex-grafanadwidget3, #flex-grafanadwidget4 {
        min-width: 50%;
    }
}
@media only screen and (max-width: 640px) {
    #flex-grafanadwidget1, #flex-grafanadwidget2, #flex-grafanadwidget3, #flex-grafanadwidget4 {
        min-width: 100%;
    }
@media only screen and (max-width: 400px) {
    .flex-child>h5 {
	margin-left: 15px;
    }
#announcementRow {
	background-color:transparent !important;
}
.flex-child>h5 {
	text-transform: uppercase;
	font-weight: 600 !important;
	font-size: 15px;important;
	color: #eee;
}
.overflowhider {
	height: 100%;
	overflow: hidden;
}
#grafanadwidget1 {
	position: relative;
	height: calc(250px);
	width: calc(100%);
}
#grafanadwidget2 {
    position: relative;
	height:calc(250px);
	width:calc(100%);
}
#grafanadwidget3 {
	position: relative;
	height: calc(250px);
	width: calc(100%);
}
#grafanadwidget4 {
    position: relative;
	height:calc(250px);
	width:calc(100%);
}
</style>

<div id="announcementRow" class="row">
	<div class="content-box flex">
<div class="flex-child" id="flex-grafanadwidget1">
  <h5><span>Panel name</span></h5>
  <div class="overflowhider"><embed id="grafanadwidget1" src='https://graforg.domain.com/panel-embed-link'/></div>
  </div>
<div class="flex-child box-shadow" id="flex-grafanadwidget2">
  <h5><span>Panel name</span></h5>
  <div class="overflowhider"><embed id="grafanadwidget2" src='https://graforg.domain.com/panel-embed-link' /></div>
  </div>
<div class="flex-child" id="flex-grafanadwidget3">
  <h5><span>Panel name</span></h5>
  <div class="overflowhider"><embed id="grafanadwidget3" src='https://graforg.domain.com/panel-embed-link'/></div>
  </div>
<div class="flex-child box-shadow" id="flex-grafanadwidget4">
  <h5><span>Panel name</span></h5>
  <div class="overflowhider"><embed id="grafanadwidget4" src='https://graforg.domain.com/panel-embed-link' /></div>
  </div>
	</div>
</div>
```
</details>

***

# Netdata Themes

Custom [Netdata](https://github.com/firehol/netdata) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/netdata-1.png)

```
https://gilbn.github.io/theme.park/CSS/themes/netdata/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
organizr-dashboard.css
```

#### The `organizr-dashboard.css` theme is an "internal" theme that is meant to be used in an Organizr iframe as the background is set to transparent. [The theme can be used to integrate Netadata on the Organizr Homepage](https://technicalramblings.com/blog/spice-up-your-homepage/) 

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/1.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/2.jpg"></img>
</p>
</details>

### Custom HTML for Organizr Homepage

***

# Monitorr Themes

Custom [Monitorr](https://github.com/Monitorr/Monitorr) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/1-flat.jpg)

```
https://gilbn.github.io/theme.park/CSS/themes/monitorr/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
organizr-dashboard.css
```

#### The `organizr-dashboard.css` theme will mess with your Monitorr base theme. And it will hide the settings button. Go to /monitorr/settings.php for settings.  It is created purely for use with "minimum" version of the index.php `https://domain.com/monitorr/index.min.php` for Organizr homepage integration.
**NOTE:**
When viewing monitorr in Organizr iframe using `organizr-dashboard.css` it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect. If you don't want this you can create two reverse proxies. One for monitorr organizr homepage integration and one for the monitorr dark/plex theme. And use subfilter on both instead of adding `@import "https://gilbn.github.io/theme.park/CSS/themes/organizr-dashboard.css";` in the monitorr custom css.


### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/2.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/3.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/4.jpg"></img>
</p>
</details>

Add this in the Monitorr custom css box:
```css
@import "https://gilbn.github.io/theme.park/CSS/themes/monitorr/THEME_NAME.css";
```
And add this in custom HTML in Organizr:
```css
<div id="announcementRow" class="row"><h4 class="pull-left"><span>Monitorr</span></h4><hr class="hidden-xs"></div>
<div style="overflow:hidden; height:260px; width:calc(100% + 39px); -webkit-overflow-scrolling: touch; overflow-y: scroll;">
<iframe class="iframe" frameborder="0" src="https://monitorr.domain.com/index.min.php"></iframe>
</div>
```

***

# Logarr alpha version Themes 

Custom [Logarr](https://github.com/Monitorr/logarr/tree/alpha) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr).

![](https://raw.githubusercontent.com/goldenpipes/theme.park/master/Screenshots/logarr-plex.png)

```
https://gilbn.github.io/theme.park/CSS/themes/logarr/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

***

# Filebrowser Themes

Custom [Filebrowser](https://github.com/filebrowser/filebrowser) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr).

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/filebrowser/filebrowser.png)

Based on https://github.com/Archmonger/Blackberry-Themes/blob/master/Themes/Blackberry-Flat/bbf_filebrowser.css
**https://github.com/Archmonger/Blackberry-Themes**

```
https://gilbn.github.io/theme.park/CSS/themes/filebrowser/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```


### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/filebrowser/filebrowser2.png"></img>
</p>
</details>

***

# HTML5 Speedtest Themes

Custom [HTML5 Speedtest](https://github.com/adolfintel/speedtest) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr).

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/html5speedtest.png)

```
https://gilbn.github.io/theme.park/CSS/themes/html5speedtest/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
```

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/html5speedtest_dark.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/html5speedtest_plex.png"></img>
</p>
</details>

***
### Honourable mentions:

[leram84/layer.Cake](https://github.com/leram84/layer.Cake/)

[rg9400/Cloud-Tautulli-Theme](https://github.com/rg9400/Cloud-Tautulli-Theme)

[Burry/organizr-v2-plex-theme](https://github.com/Burry/organizr-v2-plex-theme)

[iFelix18/Darkerr](https://github.com/iFelix18/Darkerr)

[ydkmlt84/DarkerNZBget](https://github.com/ydkmlt84/DarkerNZBget)

[Archmonger/Blackberry-Flat](https://github.com/Archmonger/Blackberry-Flat)
