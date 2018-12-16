# theme.park
A collection of themes/skins for use in conjunction with [Organizr](https://github.com/causefx/Organizr)

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
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guac-1.png.png"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/guacorg/guac-2.png.png"></img>
</p>
</details>

***

# Plex Organizr Theme

Custom [Plex](https://plex.tv) CSS to match the [Organizr](https://github.com/causefx/Organizr) theme.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/plexorg/plexorg.png)

#### The `plexorg.css` theme is a dark theme that matches Organizr.

***

# OrgArr - Sonarr v2/v3 - Radarr - Lidarr

Custom [Sonarr V2 and V3](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr)/[Lidarr](https://github.com/Lidarr/Lidarr) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

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

# GrafOrg - Grafana

Custom [Grafana](https://github.com/grafana/grafana) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration and consistent UI.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/graforg/grafana-1.png)


## Custom CSS for Organizr
#### The `graforg.css` theme is a dark theme that matches the Organizr dark theme. NOTE: The `graforg.css` theme will hide the side menu. Go to https://graforg.domain.com/login for settings. 

#### `grafplex.css` If you want a regular Plex theme for your Grafana setup, use the **`grafplex.css`** theme instead.

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

# NetOrg - Netdata

Custom [Netdata](https://github.com/firehol/netdata) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/netdata-1.png)


## Custom CSS for Organizr
#### The `netorg.css` theme is a dark theme that matches Organizr.

#### `netplex.css` If you want a regular Plex theme for your Netdata setup, use the **`netplex.css`** instead.

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/1.jpg"></img>
<img src="https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/netorg/2.jpg"></img>
</p>
</details>

### Custom HTML for Organizr Homepage

***

# Monitorg - Monitorr

Custom [Monitorr](https://github.com/Monitorr/Monitorr) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration.

![](https://raw.githubusercontent.com/gilbN/theme.park/master/Screenshots/monitorg/1-flat.jpg)

## Custom CSS for Organizr
#### This theme will mess with your Monitorr base theme. And it will hide the settings button. Go to /monitorr/settings.php for settings.

#### It is created purely for use with Organizr.
**NOTE:** When viewing /monitorr in Organizr iframe it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect.

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
<div style="overflow:hidden; height:260px">
<embed style="height:calc(100% + 50px)" width='100%' src='https://domain.com/monitorr/index.min.php' />
</div>
```
***
### Honourable mentions:

[leram84/layer.Cake](https://github.com/leram84/layer.Cake/)

[rg9400/Cloud-Tautulli-Theme](https://github.com/rg9400/Cloud-Tautulli-Theme)

[Burry/organizr-v2-plex-theme](https://github.com/Burry/organizr-v2-plex-theme)

[iFelix18/Darkerr](https://github.com/iFelix18/Darkerr)

[ydkmlt84/DarkerNZBget](https://github.com/ydkmlt84/DarkerNZBget)

[Archmonger/Blackberry-Flat](https://github.com/Archmonger/Blackberry-Flat)
