# theme.park
A collection of themes/skins for use in conjunction with [Organizr](https://github.com/causefx/Organizr)

### Honourable mentions: 

[leram84/layer.Cake/](https://github.com/leram84/layer.Cake/)

[rg9400/Cloud-Tautulli-Theme](https://github.com/rg9400/Cloud-Tautulli-Theme)

[Burry/organizr-v2-plex-theme](https://github.com/Burry/organizr-v2-plex-theme)

[iFelix18/Darkerr](https://github.com/iFelix18/Darkerr)

[ydkmlt84/DarkerNZBget](https://github.com/ydkmlt84/DarkerNZBget)


# OrgArr

Custom [Sonarr](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr)/[Lidarr](https://github.com/Sonarr/Sonarr) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr) homepage integration.
![](/Screenshots/orgarr/5.jpg)

#### The `orgarr.css` theme will mess with your Xarr base theme. 

#### `graforg.css` is created purely for use with Organizr.
**NOTE:** When viewing Xarr in Organizr iframe it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect.

#### `orgarr-blur.css`
If you want a regular Plex theme for your *arr setup, use the **`orgarr-blur.css`** instead.

## Setup
<details><summary>Expand</summary>

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="/Screenshots/orgarr/1.jpg"></img>
<img src="/Screenshots/orgarr/2.jpg"></img>
<img src="/Screenshots/orgarr/3.jpg"></img>
<img src="/Screenshots/orgarr/4.jpg"></img>
</p>
</details>

### Subfilter
As the arr's doesn't have support for custom CSS you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx.

Add this to your location context/block:
```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/orgarr.css">
</head>';
sub_filter_once on;
```
### Here is a complete example:
```nginx
#GRAFANA CONTAINER

# REDIRECT HTTP TRAFFIC TO https://[domain.com]
server {
  listen 80;
  server_name orgarr.domain.com;
  return 301 https://$server_name$request_uri;
  }

server {
  listen 443 ssl http2;
  server_name graforg.domain.com;

include /config/nginx/ssl.conf;

location / {
  proxy_pass http://192.168.1.34:3000;
  proxy_set_header Accept-Encoding "";
  sub_filter
  '</head>'
  '<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/orgarr.css">
  </head>';
  sub_filter_once on;
  proxy_hide_header X-Frame-Options;
  proxy_set_header X-Forwarded-Host $host;
  proxy_set_header X-Forwarded-Server $host;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_http_version 1.1;
  proxy_pass_request_headers on;
  proxy_set_header Connection "keep-alive";
  proxy_store off;
  }
}
```

# GrafOrg

Custom [Grafana](https://github.com/grafana/grafana) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration.
![](/Screenshots/graforg/3.jpg)
## Custom CSS for Organizr
#### The `graforg.css` theme will mess with your Grafana base theme. And it will hide the side menu. Go to https://graforg.domain.com/datasources for settings.

#### `graforg.css` is created purely for use with Organizr.
**NOTE:** When viewing Grafana in Organizr iframe it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect.

#### `grafblur.css`
If you want a regular Plex theme for your Grafana setup, use the **`grafblur.css`** instead.

## Setup
<details><summary>Expand</summary>

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="/Screenshots/graforg/1.jpg"></img>
<img src="/Screenshots/graforg/2.jpg"></img>
</p>
</details>

### Subfilter
As Grafana doesn't have support for custom CSS you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx.

Create **another** reverse proxy for monitorr and add this:
```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/graforg.css">
</head>';
sub_filter_once on;
```
### Here is a complete example:
```nginx
#GRAFANA CONTAINER

# REDIRECT HTTP TRAFFIC TO https://[domain.com]
server {
  listen 80;
  server_name graforg.domain.com;
  return 301 https://$server_name$request_uri;
  }

server {
  listen 443 ssl http2;
  server_name graforg.domain.com;

include /config/nginx/ssl.conf;

location / {
  proxy_pass http://192.168.1.34:3000;
  proxy_set_header Accept-Encoding "";
  sub_filter
  '</head>'
  '<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/graforg.css">
  </head>';
  sub_filter_once on;
  proxy_hide_header X-Frame-Options;
  proxy_set_header X-Forwarded-Host $host;
  proxy_set_header X-Forwarded-Server $host;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_http_version 1.1;
  proxy_pass_request_headers on;
  proxy_set_header Connection "keep-alive";
  proxy_store off;
  }
}
```
### Custom HTML for Organizr Homepage
Thank you [Fma965](https://gist.github.com/Fma965) for the [code](https://gist.github.com/Fma965/d30ac1fa5695304a7d6dcdc748220027)

Change the ***Panel name*** to what you want and the ***src*** to the panel URL.

```css
<h5><span>Panel name</span></h5>
  <div class="overflowhider"><embed id="grafanadwidget1" src='https://graforg.domain.com/panel-embed-link'/>**
```
The URL can be found by clicking **share** on the panel you want to add.
![](/Screenshots/graforg/4.jpg)

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

# NetOrg

Custom [Netdata](https://github.com/firehol/netdata) CSS for consistent UI in [Organizr](https://github.com/causefx/Organizr)

![](/Screenshots/netorg/2.jpg)

## Custom CSS for Organizr
#### The `netorg.css` theme will mess with your Netdata base theme.

#### `netorg.css` is created purely for use with Organizr.
**NOTE:** When viewing Netdata in Organizr iframe it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect.

#### `netblur.css`
If you want a regular Plex theme for your Netdata setup, use the **`netblur.css`** instead.

## Setup
<details><summary>Expand</summary>

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="/Screenshots/netorg/1.jpg"></img>
</p>
</details>

### Subfilter
As Netdata doesn't have support for custom CSS you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx.

Create **another** reverse proxy for monitorr and add this:
```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/netorg.css">
</head>';
sub_filter_once on;
```
### Here is a complete example:
```nginx
	# NETDATA CONTAINER
	location ~ /netdata/(?<ndpath>.*) {
		#auth_request /auth-user;
		auth_request /auth-4;   #=User
		proxy_set_header X-Forwarded-Host $host;
		proxy_set_header X-Forwarded-Server $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_pass http://192.168.1.34:19999/$ndpath$is_args$args;
		proxy_http_version 1.1;
		proxy_pass_request_headers on;
		proxy_set_header Connection “keep-alive”;
		proxy_store off;
		gzip on;
    gzip_proxied any;
    gzip_types *;
		proxy_set_header Accept-Encoding "";
		sub_filter
		'</head>'
		'<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/netorg.css">
		</head>';
		sub_filter_once on;
	}
```
### Custom HTML for Organizr Homepage

```css
```
</details>

***

# Monitorg

Custom [Monitorr](https://github.com/Monitorr/Monitorr) CSS for [Organizr](https://github.com/causefx/Organizr) homepage integration.

![](/Screenshots/monitorg/1.jpg)

## Custom CSS for Organizr
#### This theme will mess with your Monitorr base theme. And it will hide the settings button. Go to /monitorr/settings.php for settings.

#### It is created purely for use with Organizr.
**NOTE:** When viewing /monitorr in Organizr iframe it will follow the Organizr theme. When viewing it outside of Organizr iframe the background will be white ect.

## Setup
<details><summary>Expand</summary>

### Screenshots
<details><summary>Expand</summary>
<p>
<img src="/Screenshots/monitorg/2.jpg"></img>
<img src="/Screenshots/monitorg/3.jpg"></img>
<img src="/Screenshots/monitorg/4.jpg"></img>
</p>
</details>

Add this in the custom css box:
```css
@import "https://rawgit.com/gilbN/theme.park/CSS/themes/monitorg.css";
```
And add this in custom HTML in Organizr:
```css
<div style="overflow:hidden; height:260px">
<embed style="height:calc(100% + 50px)" width='100%' src='https://domain.com/monitorr/index.min.php' />
</div>
```
### Subfilter
As this theme will change the base theme, you can get around that by using [subfilter](http://nginx.org/en/docs/http/ngx_http_sub_module.html) in Nginx.
Create another reverse proxy for monitorr and add this:
```nginx
		proxy_set_header Accept-Encoding "";
		sub_filter
		'</head>'
		'<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/monitorg.css">
		</head>';
		sub_filter_once on;
```
Here is a complete example:
```nginx
#MONITORR CONTAINER

# REDIRECT HTTP TRAFFIC TO https://[domain.com]
server {
 	listen 80;
 	server_name monitorg.domain.com;
 	return 301 https://$server_name$request_uri;
}

server {  
    listen 443 ssl http2;
    server_name monitorg.domain.com;

	#SSL settings
	include /config/nginx/ssl.conf

location / {
    proxy_pass http://192.168.1.2:8701;
    include /config/nginx/proxy.conf;
		proxy_set_header Accept-Encoding "";
		sub_filter
		'</head>'
		'<link rel="stylesheet" type="text/css" href="https://rawgit.com/gilbN/theme.park/CSS/themes/monitorg.css">
		</head>';
		sub_filter_once on;
  }
}
```
</details>
