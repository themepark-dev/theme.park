<h1 align="center">
    <img src="https://i.imgur.com/brLughi.png">
</h1>
<p align="center">
  A collection of themes/skins for use in conjunction with <a href="https://github.com/causefx/Organizr/" target="_blank">Organizr</a>
<p align="center">
<a href="https://www.buymeacoffee.com/oY5Nk8GHK" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>	
    <br />
    <br />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3.png" alt="Screen Shot 1" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana-1.png" alt="Screen Shot 2" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plexorg.png" alt="Screen Shot 3" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plpp/plpp.png" alt="Screen Shot 4" width="49.15%" />
</p>

## Setup

### Subfilter

As  most of these apps doesn't have support for custom CSS you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx.

Add this to your reverse proxy:

```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/CUSTOM_CSS.css">
</head>';
sub_filter_once on;
```
Where `CUSTOM_CSS` is the name of the theme. e.g. `nzbget-plex.css`

Here is a complete example:

<details><summary>Expand</summary>

```nginx
# REDIRECT HTTP TRAFFIC TO https://[domain.com]
server {
    listen 80;
    server_name plpp.domain.com;
    return 301 https://$server_name$request_uri;
}
server {  
    listen 443 ssl http2;
    server_name plpp.domain.com;

#SSL settings
    include /config/nginx/ssl.conf

location / {
    proxy_pass http://192.168.1.2:8701;
    include /config/nginx/proxy.conf;
	proxy_set_header Accept-Encoding "";
	sub_filter
	'</head>'
	'<link rel="stylesheet" type="text/css" href="https://gilbn.github.io/theme.park/CSS/themes/plpporg.css">
	</head>';
	sub_filter_once on;
  }
}
```
</details>

## [Feature requests](http://feathub.com/gilbN/theme.park)
[![Feature Requests](http://feathub.com/gilbN/theme.park?format=svg)](http://feathub.com/gilbN/theme.park)

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

# PHP Library Presenter Dark/Plex Theme

Custom [PLPP](https://github.com/Tensai75/plpp) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plpp/plpp.png)

#### `plpporg.css` is a dark theme that matches Organizr.

#### `plpp-plex.css` is a Plex theme for PLPP


***
# Guacamole Dark/Plex Theme

Custom [Guacamole](https://guacamole.apache.org/) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guacorg.png)

#### `guacorg.css` is a dark theme that matches Organizr.

#### `guacplex.css` is a Plex theme for Guacamole

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guac-1.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guac-2.png"></img>
</p>
</details>

***

# Plex Organizr Theme

Custom [Plex](https://plex.tv) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plexorg.png)

#### The `plexorg.css` theme is a dark theme that matches Organizr.

***

# OrgArr - Sonarr v2/v3 - Radarr - Lidarr - Bazarr Dark/Plex Theme

Custom [Sonarr V2 and V3](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr)/[Lidarr](https://github.com/Lidarr/Lidarr)/[Bazarr](https://github.com/morpheus65535/bazarr) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3.png)

 

Thank you iFelix18 for doing all the hard work! :)

#### The `orgarr.css` theme is a dark theme that matches the Organizr dark theme.

#### `orgarr-plex.css` If you want a regular Plex theme for your *arr setup, use the **`orgarr-plex.css`** instead.

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

# NZBGet Dark/Plex Theme

Custom CSS for [Nzbget](https://github.com/nzbget/nzbget)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget-split.png)

#### The `nzborg.css` theme is a dark theme that matches the Organizr dark theme.

#### The `nzbget-plex.css` theme is a plex theme for NZBGet.

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

# SABnzbd Dark/Plex Theme

Custom CSS for [SABnzbd](https://github.com/sabnzbd/sabnzbd)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd.png)

#### Use the `sabnzbd_dark.css` for a dark theme that matches the Organizr dark theme.
**Note: SABnzbd theme must be set to `Glitter`**

#### Use the `sabnzbd_plex.css` for a dark theme that matches the Organizr dark theme.
**Note: SABnzbd theme must be set to `Glitter`**

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd_dark_2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd_dark_3.png"></img>
</p>
</details>

***

# GrafOrg - Grafana Dark/Plex

Custom [Grafana](https://github.com/grafana/grafana) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration and consistent UI.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana-1.png)

#### The `graforg.css` theme is a dark theme that matches the Organizr dark theme.
#### `grafplex.css`: If you want a regular Plex theme for your Grafana setup, use the **`grafplex.css`** theme instead.
#### For panel integration on the Organizr homepage you can use `graforg-dashboard.css` if you use the Plex theme in Organizr.
### Check out https://technicalramblings.com/blog/spice-up-your-homepage-part-ii/

![](https://technicalramblings.com/wp-content/uploads/2019/01/orgdash.jpg)

### **TIP:**
Click the `kiosk` button and use that link if you don't want to show the top bar and side bar inside Organizr! There are two modes, one where the side menu and variables ect disappear and one where just the panels are visible.

https://grafana.technicalramblings.com/d/nLJXnLJiz/unraid-ups-dashboard?refresh=10s&orgId=1&kiosk=tv
https://grafana.technicalramblings.com/d/nLJXnLJiz/unraid-ups-dashboard?refresh=10s&orgId=1&kiosk

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

# NetOrg - Netdata Dark/Plex Theme

Custom [Netdata](https://github.com/firehol/netdata) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/netdata-1.png)

#### The `netorg.css` theme is an "internal" theme that is meant to be used in an Organizr iframe as the background is set to transparent. [The theme can be used to integrate Netadata on the Organizr Homepage](https://technicalramblings.com/blog/spice-up-your-homepage/)

#### `netplex.css` If you want a regular Plex theme for your Netdata setup, use the **`netplex.css`** instead.

#### The `netorg-dark.css` theme is a dark theme that matches Organizr. 

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/1.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/2.jpg"></img>
</p>
</details>

### Custom HTML for Organizr Homepage

***

# Monitorg - Monitorr Dark/Plex Theme

Custom [Monitorr](https://github.com/Monitorr/Monitorr) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/1-flat.jpg)

#### The `monitorg.css` theme will mess with your Monitorr base theme. And it will hide the settings button. Go to /monitorr/settings.php for settings.  It is created purely for use with "minimum" version of the index.php `https://domain.com/monitorr/index.min.php` for Organizr homepage integration.
**NOTE:**
When viewing monitorr in Organizr iframe using `monitorg.css` it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect. If you don't want this you can create two reverse proxies. One for monitorr organizr homepage integration and one for the monitorr dark/plex theme. And use subfilter on both instead of adding `@import "https://gilbn.github.io/theme.park/CSS/themes/monitorg.css";` in the monitorr custom css.

#### For the dark theme use `monitorg-dark.css`
#### For the Plex theme use `monitorg-plex.css`

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
@import "https://gilbn.github.io/theme.park/CSS/themes/monitorg.css";
```
And add this in custom HTML in Organizr:
```css
<div id="announcementRow" class="row"><h4 class="pull-left"><span>Monitorr</span></h4><hr class="hidden-xs"></div>
<div style="overflow:hidden; height:260px; width:calc(100% + 39px); -webkit-overflow-scrolling: touch; overflow-y: scroll;">
<iframe class="iframe" frameborder="0" src="https://monitorr.domain.com/index.min.php"></iframe>
</div>
```

***

# Logarr (alpha only) (WIP)

Custom [Logarr](https://github.com/Monitorr/logarr/tree/alpha) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr).

![](https://raw.githubusercontent.com/goldenpipes/theme.park/master/Screenshots/logarr-plex.png)

Install via subfilter, logarr custom css, or by over writing the default 'logarr.css' in your `webserver/logarr/css` directory.

#### the css is named `logarr-plex.css`

***

# Filebrowser - Dark Theme

Custom [Filebrowser](https://github.com/filebrowser/filebrowser) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr).

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/filebrowser/filebrowser.png)

Based on https://github.com/Archmonger/Blackberry-Themes/blob/master/Themes/Blackberry-Flat/bbf_filebrowser.css
**https://github.com/Archmonger/Blackberry-Themes**

#### The css is named `filebrowser_dark.css`


### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/filebrowser/filebrowser2.png"></img>
</p>
</details>

***

# HTML5 Speedtest Dark/Plex Theme

Custom [HTML5 Speedtest](https://github.com/adolfintel/speedtest) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr).

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/html5speedtest.png)

#### The css files are named `html5speedtest_dark.css` and `html5speedtest_plex.css` 

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
