# Radarr 4K logo

Add a 4K logo to your Radarr css. 

### Desktop
![](desktop.png)
![](v3-desktop.png)

### Mobile
![](mobile.png)
![](v3-mobile.png)


## Setup

#### Nginx
Examples of how to add it:

```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/themes/radarr/THEME.css">
<link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/addons/radarr/radarr-4k-logo.css">
</head>';
sub_filter_once on;
```

#### Apache

```nginx
AddOutputFilterByType SUBSTITUTE text/html
   Substitute 's|</head> '<link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/themes/radarr/THEME.css"><link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/addons/radarr/radarr-4k-logo.css">
</head>';|'
```

#### Caddy

```nginx
filter rule {
    content_type text/html.*
    search_pattern </head>
    replacement "<link rel='stylesheet' type='text/css' href='https://theme-park.dev/CSS/themes/<APP_NAME>/<THEME>.css'><link rel='stylesheet' type='text/css' href='https://theme-park.dev/CSS/addons/radarr/radarr-4k-logo.css'></head>"
}
```

#### Stylus

Just add another import line.

```css
@import "https://theme-park.dev/CSS/themes/radarr/THEME.css";
@import "https://theme-park.dev/CSS/addons/radarr/radarr-4k-logo.css";
```