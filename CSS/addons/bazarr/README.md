Adds a 4K logo to your Bazarr css. 
<p>
<a href="https://raw.githubusercontent.com/gilbN/theme.park/master/CSS/addons/bazarr/desktop.png" rel="noopener"><img src="https://raw.githubusercontent.com/gilbN/theme.park/master/CSS/addons/bazarr/desktop.png" alt="Screen Shot 1" width="33%" /></a>
</p>
<p>
<a href="https://raw.githubusercontent.com/gilbN/theme.park/master/CSS/addons/bazarr/mobile.png" rel="noopener"><img src="https://raw.githubusercontent.com/gilbN/theme.park/master/CSS/addons/bazarr/mobile.png" alt="Screen Shot 1" width="33%" /></a>
</p>

## Setup

#### Docker mod <img src="https://avatars.githubusercontent.com/u/12324908?s=20&v=4">
`-e TP_ADDON=bazarr-4k-logo`

#### Nginx
Examples of how to add it:

```nginx
proxy_set_header Accept-Encoding "";
sub_filter
'</head>'
'<link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/themes/bazarr/THEME.css">
<link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/addons/bazarr/bazarr-4k-logo.css">
</head>';
sub_filter_once on;
```

#### Apache

```nginx
AddOutputFilterByType SUBSTITUTE text/html
   Substitute 's|</head> '<link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/themes/bazarr/THEME.css"><link rel="stylesheet" type="text/css" href="https://theme-park.dev/CSS/addons/bazarr/bazarr-4k-logo.css">
</head>';|'
```

#### Caddy

```nginx
filter rule {
    content_type text/html.*
    search_pattern </head>
    replacement "<link rel='stylesheet' type='text/css' href='https://theme-park.dev/CSS/themes/<APP_NAME>/<THEME>.css'><link rel='stylesheet' type='text/css' href='https://theme-park.dev/CSS/addons/bazarr/bazarr-4k-logo.css'></head>"
}
```

#### Stylus

Just add another import line.

```css
@import "https://theme-park.dev/CSS/themes/bazarr/THEME.css";
@import "https://theme-park.dev/CSS/addons/bazarr/bazarr-4k-logo.css";
```