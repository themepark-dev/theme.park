/*!
* Start Bootstrap - Creative v6.0.5 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using anime.js
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').on('click', function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length ?
                target :
                $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                anime({
                    targets: 'html, body',
                    scrollTop: target.offset().top - 72,
                    duration: 1000,
                    easing: 'easeInOutExpo'
                });
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function () {
        $('.navbar-collapse').collapse('hide');
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
        target: '#mainNav',
        offset: 75
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-scrolled");
        } else {
            $("#mainNav").removeClass("navbar-scrolled");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);

    // Magnific popup calls
    $('#portfolio').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1]
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
        }
    });

})(jQuery); // End of use strict

const themes = ["aquamarine","hotline","dark","organizr-dark","dracula","overseerr",
"plex","space-gray","hotpink","onedark","nord"];
var random = themes[~~(Math.random() * themes.length)];
// load a random css stylesheet
function injectTheme(theme,container="head") {
    if (container === "head") {
        html_element = document.head;
    } else html_element = document.body;
    let themeOption = document.getElementById("theme-option")
    let link = themeOption ? themeOption : document.createElement("link");
    url = "/CSS/variables/"
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = `${url}/${theme.toLowerCase()}.css`;
    link.id = `theme-option`
    html_element.appendChild(link);
  }

  // Add theme data and set theme vars
  var apps;
  var themeOptions;
  function addThemeData() {
  let themeJsonUrl = "/themes.json"
  fetch(themeJsonUrl)
  .then(response =>  response.json())
  .then(json => {
    apps = json.applications
    themeOptions = json.themes
    appCount = Object.keys(json.applications).length
    document.getElementById("tag-line").innerText = `A collection of themes/skins for ${appCount} selfhosted
    apps!`
    document.getElementById("theme-header-text").innerText = `${appCount} themed applications!`
    document.getElementById("app-count").innerHTML = `
    theme.park contains ${appCount} themed applications, with css <a
    href="https://docs.theme-park.dev/themes/addons/">addons</a> on certain themes.`
    document.getElementById("theme-count").innerHTML = `Choose between <a class="js-scroll-trigger" href="#themes">${Object.keys(json.themes).length} different
    styles!</a> With the possibility to easily create your own themes using the defined <a
    href="https://docs.theme-park.dev/custom/">variables</a>.`
    createApps(apps)
    })
}

function createApps(apps) {
    let allAppsDiv = document.getElementById("all-apps")
    sorted = Object.keys(apps).sort()
    for (let app in sorted) {
    let newApp = `
        <a class="col app-container text-center p-2 m-1" href="https://docs.theme-park.dev/themes/${sorted[app]}/">
            <p><img class="app-container-image" src="https://docs.theme-park.dev/site_assets/${sorted[app]}/logo.png"/></p>
            <p>${sorted[app][0].toUpperCase() + sorted[app].slice(1)}</p>
        </a>`
    allAppsDiv.innerHTML += newApp
    }
}

function fadeOutIn(speed ) {
    let theme = Object.keys(themeOptions)[~~(Math.random() * Object.keys(themeOptions).length)]
    if (!document.body.style.opacity) {
        document.body.style.opacity = 1;
    }
    var outInterval = setInterval(function() {
        document.body.style.opacity -= 0.02;
        if (document.body.style.opacity <= 0) {
            clearInterval(outInterval);
            injectTheme(theme)
            document.getElementById("switch-theme").innerText = theme
            var inInterval = setInterval(function() {
                document.body.style.opacity = Number(document.body.style.opacity)+0.02;
                if (document.body.style.opacity >= 1)
                    clearInterval(inInterval);
            }, speed/50 );
        }
    }, speed/50 );

}

injectTheme(random);
addThemeData();
document.getElementById("switch-theme").addEventListener("click", () =>  {
    fadeOutIn(350);
})

