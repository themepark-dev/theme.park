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
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/sonarrv3.png" alt="Screen Shot 1" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana-1.png" alt="Screen Shot 2" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plexorg.png" alt="Screen Shot 3" width="49.15%" />
    <img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plpp/plpp.png" alt="Screen Shot 4" width="49.15%" />
</p>

# Setup

All apps have 5 themes to choose from. 
`https://gilbn.github.io/theme.park/CSS/themes/<APP_NAME>/<THEME_NAME>.css`
```
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
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#tautulli-themes">Tautulli</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#organizr-hotline-and-marine-theme">Organizr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#grafana-themes">Grafana</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#sabnzbd-themes">Sabnzbd</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#nzbget-themes">Nzbget</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#nzbhydra2-themes">NZBHydra2</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#deluge-themes">Deluge</a></li>	
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#qbittorrent-themes">qBittorrent</a></li>	
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#guacamole-themes">Guacamole</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#rutorrent-themes">ruTorrent</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#netdata-themes">Netdata</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#jackett-themes">Jackett</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#html5-speedtest-themes">html5speedtest</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#filebrowser-themes">Filebrowser</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#monitorr-themes">Monitorr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#logarr-alpha-version-themes">Logarr</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#php-library-presenter-themes">PLPP</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#synclounge-themes">Synclounge</a></li>
<li><a href="https://github.com/gilbN/theme.park/blob/master/README.md#the-lounge-themes">The Lounge</a></li>
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

Custom [Ombi](https://github.com/tidusjar/Ombi) CSS.

**Install by adding `@import "https://gilbn.github.io/theme.park/CSS/themes/ombi/THEME_NAME.css";` in custom css**

```
https://gilbn.github.io/theme.park/CSS/themes/ombi/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/ombi/ombi.gif)
***
# Jackett Themes

Custom [Jackett](https://github.com/Jackett/Jackett) CSS.

```
https://gilbn.github.io/theme.park/CSS/themes/jackett/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/jackett/jackett.gif)
***
# PHP Library Presenter Themes

Custom [PLPP](https://github.com/Tensai75/plpp) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plpp/plpp.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/plpp/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```

***
# Guacamole Themes

Custom [Guacamole](https://guacamole.apache.org/) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guacamole.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/guacamole/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
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

Custom [Plex](https://plex.tv) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plex.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/plex/XXX.css
aquamarine.css
hotline.css
dark.css
space-gray.css
```

***

# Sonarr v2/v3 - Radarr - Lidarr - Bazarr Themes

Custom [Sonarr V2 and V3](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr)/[Lidarr](https://github.com/Lidarr/Lidarr)/[Bazarr](https://github.com/morpheus65535/bazarr) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/orgarr/orgarr.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/sonarr/XXX.css
https://gilbn.github.io/theme.park/CSS/themes/radarr/XXX.css
https://gilbn.github.io/theme.park/CSS/themes/lidarr/XXX.css
https://gilbn.github.io/theme.park/CSS/themes/bazarr/XXX.css
aquamarine.css
hotline.css
plex.css
dark.css
space-gray.css
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

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbget/nzbget.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/nzbget/XXX.css
aquamarine.css
hotline.css
plex.css
dark.css
space-gray.css
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

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/sabnzbd/sabnzbd.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/sabnzbd/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
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

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/grafana/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
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

Custom [Netdata](https://github.com/firehol/netdata) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/netdata.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/netdata/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
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

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/monitorr.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/monitorr/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
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

Custom [Logarr](https://github.com/Monitorr/logarr/tree/alpha) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/logarr/logarr.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/logarr/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```

***

# Filebrowser Themes

Custom [Filebrowser](https://github.com/filebrowser/filebrowser) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/filebrowser/filebrowser.gif)

Based on https://github.com/Archmonger/Blackberry-Themes/blob/master/Themes/Blackberry-Flat/bbf_filebrowser.css
**https://github.com/Archmonger/Blackberry-Themes**

```
https://gilbn.github.io/theme.park/CSS/themes/filebrowser/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```


### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/filebrowser/filebrowser2.png"></img>
</p>
</details>

***

# HTML5 Speedtest Themes

Custom [HTML5 Speedtest](https://github.com/adolfintel/speedtest) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/speedtest.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/html5speedtest/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/html5speedtest_dark.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/html5speedtest/html5speedtest_plex.png"></img>
</p>
</details>

***
# Tautulli Themes

Custom [Tautulli](https://github.com/Tautulli/Tautulli) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/tautulli/tautulli.gif)

```
https://gilbn.github.io/theme.park/CSS/themes/tautulli/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
***
# Deluge Themes

Custom [Deluge](https://github.com/deluge-torrent/deluge) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/deluge/deluge.gif)

Based on https://github.com/halianelf/deluge-dark @halianelf Thanks for making the job easier!
```
https://gilbn.github.io/theme.park/CSS/themes/deluge/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
***
# qBittorrent Themes

Custom [qBitorrent](https://github.com/qbittorrent/qBittorrent) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/qbittorrent/qbittorrent.gif)

NOTE: You need to change or remove the CSP header. 

Add this in your reverse proxy:
```nginx
        proxy_hide_header   "x-webkit-csp";
        proxy_hide_header   "content-security-policy";
```

```
https://gilbn.github.io/theme.park/CSS/themes/qbittorrent/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/qbittorrent/qbit1.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/qbittorrent/qbit2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/qbittorrent/qbit3.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/qbittorrent/qbit4.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/qbittorrent/qbit5.png"></img>
</p>
</details>

***
# ruTorrent Themes

Custom [ruTorrent](https://github.com/Novik/ruTorrent) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/rutorrent/rutorrent.gif)


**Theme needs to be `Standard` in settings!**

```
https://gilbn.github.io/theme.park/CSS/themes/rutorrent/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/rutorrent/rutorrent1.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/rutorrent/rutorrent2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/rutorrent/rutorrent3.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/rutorrent/rutorrent4.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/rutorrent/rutorrent5.png"></img>
</p>
</details>

***
# NZBhydra2 Themes

Custom [NZBHydra](https://github.com/theotherp/nzbhydra2) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbhydra2/nzbhydra2.gif)


```
https://gilbn.github.io/theme.park/CSS/themes/nzbhydra2/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbhydra2/nzbhydra1.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbhydra2/nzbhydra2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbhydra2/nzbhydra3.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbhydra2/nzbhydra4.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/nzbhydra2/nzbhydra5.png"></img>
</p>
</details>

***
# Synclounge Themes

Custom [Synclounge](https://github.com/samcm/SyncLounge) CSS.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/synclounge/synclounge.gif)


```
https://gilbn.github.io/theme.park/CSS/themes/synclounge/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/synclounge/synclounge1.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/synclounge/synclounge2.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/synclounge/synclounge3.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/synclounge/synclounge4.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/synclounge/synclounge5.png"></img>
</p>
</details>

***
# The Lounge Themes

Custom [The Lounge](https://github.com/thelounge/thelounge) CSS.

![](/Screenshots/thelounge/thelounge.gif)


```
https://gilbn.github.io/theme.park/CSS/themes/thelounge/XXX.css
aquamarine.css
hotline.css
dark.css
plex.css
space-gray.css
```
### Screenshots
<details><summary>Expand</summary>
<p>
<img src="/Screenshots/thelounge/thelounge1.png"></img>
<img src="/Screenshots/thelounge/thelounge2.png"></img>
<img src="/Screenshots/thelounge/thelounge3.png"></img>
<img src="/Screenshots/thelounge/thelounge4.png"></img>
<img src="/Screenshots/thelounge/thelounge5.png"></img>
</p>
</details>

### Honourable mentions:

[leram84/layer.Cake](https://github.com/leram84/layer.Cake/)

[rg9400/Cloud-Tautulli-Theme](https://github.com/rg9400/Cloud-Tautulli-Theme)

[Burry/organizr-v2-plex-theme](https://github.com/Burry/organizr-v2-plex-theme)

[iFelix18/Darkerr](https://github.com/iFelix18/Darkerr)

[ydkmlt84/DarkerNZBget](https://github.com/ydkmlt84/DarkerNZBget)

[Archmonger/Blackberry-Flat](https://github.com/Archmonger/Blackberry-Flat)
