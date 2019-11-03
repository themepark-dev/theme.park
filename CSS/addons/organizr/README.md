## Installation

Set the Organizr theme to either Aquamarine or Hotline.

  Import the `glass-base.css` and root variables in the Custom Theme CSS box like below.
  Replace `--main-bg-color` with a wallpaper you have uploaded to Organizr
 
```css
@import "https://gilbn.github.io/theme.park/CSS/addons/organizr/glass-base.css"; 
:root {
    --main-bg-color: url(https://domain.com/your/hosted/wallpaper.jpg) center center/cover no-repeat fixed;
    --mobile-bg-color: radial-gradient(circle, #3a3a3a, #2d2d2d, #202020, #141414, #000000) center center/cover no-repeat fixed;

    --link-color: #fff;
    --custom-buttons-color: radial-gradient(ellipse at center, #3F51B5 0%, #009688 100%) center center/cover no-repeat fixed;
    --hompage-item-hover: radial-gradient(ellipse at center, rgba(0, 150, 136, 0.33) 0%, #b53f3f73 100%) center center/cover no-repeat fixed;
    --notification-box-line: #000;

    --div-background-color-10: rgba(0, 0, 0, 0.15);
    --div-background-color-15: rgba(0, 0, 0, 0.25);
    --div-background-color-25: rgba(0, 0, 0, 0.35);
    --div-background-color-35: rgba(0, 0, 0, 0.45);
}
```


Replace the variables if you have a dark background.
  Light colors for dark backgrounds.

```css
    --div-background-color-10: rgba(255, 255, 255, 0.1);
    --div-background-color-15: rgba(255, 255, 255, 0.15);
    --div-background-color-25: rgba(255, 255, 255, 0.25);
    --div-background-color-35: rgba(255, 255, 255, 0.35);
```

Dark blur colors for bright backgrounds
```css
    --div-background-color-10: rgba(0, 0, 0, 0.15);
    --div-background-color-15: rgba(0, 0, 0, 0.25);
    --div-background-color-25: rgba(0, 0, 0, 0.35);
    --div-background-color-35: rgba(0, 0, 0, 0.45);
```
