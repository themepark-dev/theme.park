/*!
* Start Bootstrap - Creative v6.0.5 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
(function ($) {
    "use strict"; // Start of use strict

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


function injectTheme(theme,container="head") {
    let themeLower = theme.toLowerCase()
    if (container === "head") {
        html_element = document.head;
    } else html_element = document.body;
    let themeOption = document.getElementById("theme-option")
    let link = themeOption ? themeOption : document.createElement("link");
    url = `${window.location.pathname}css/theme-options`
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = `${url}/${themeLower}.css`;
    link.id = `theme-option`
    html_element.appendChild(link);
  }

  // Add theme data and set theme vars
  var apps;
  var themeOptions;

  function addThemeData() {
  let themeJsonUrl = "themes.json"
  fetch(themeJsonUrl)
  .then(response =>  response.json())
  .then(json => {
    apps = json.applications
    themeOptions = json.themes
    appCount = Object.keys(json.applications).length
    document.getElementById("tag-line").innerText = `A collection of themes/skins for ${appCount} selfhosted apps!`
    document.getElementById("theme-header-text").innerText = `${appCount} themed applications!`
    document.getElementById("app-count").innerHTML = `
    theme.park contains ${appCount} themed applications, with css <a
    href="https://docs.theme-park.dev/themes/addons/">addons</a> on certain themes.`
    document.getElementById("theme-count").innerHTML = `Choose between <a class="js-scroll-trigger" href="#themes">${Object.keys(json.themes).length} official
    styles</a>, and <a href="https://docs.theme-park.dev/community-themes/">${Object.keys(json["community-themes"]).length} community styles!</a> With the possibility to easily create your own themes using the defined <a
    href="https://docs.theme-park.dev/custom/">variables</a>.`
    createApps(apps,themeOptions)
    smoothScroll()
    currentIndex = ~~(Math.random() * Object.keys(themeOptions).length)
    injectTheme(Object.keys(themeOptions)[currentIndex])
    updateMetaThemeColor()
    })
}

function createApps(apps,themeOptions) {
    let allAppsDiv = document.getElementById("all-apps")
    let allThemesDiv = document.getElementById("all-themes")
    sortedApps = Object.keys(apps).sort()
    sortedThemes = Object.keys(themeOptions).sort()
    for (let app in sortedApps) {
    let newApp = `
        <a class="col app-container text-center p-2 m-1" href="https://docs.theme-park.dev/themes/${sortedApps[app]}/">
            <p><img class="app-container-image" src="https://docs.theme-park.dev/site_assets/${sortedApps[app]}/logo.png"/></p>
            <p>${sortedApps[app][0].toUpperCase() + sortedApps[app].slice(1)}</p>
        </a>`
    allAppsDiv.innerHTML += newApp
    }
    for (let option in sortedThemes) {
        let newApp = `
        <div class="col-lg-4 col-sm-6 p-1">
            <a class="portfolio-box" href="resources/landing-page/assets/img/${sortedThemes[option].toLowerCase()}.png">
                <img class="img-fluid" src="resources/landing-page/assets/img/${sortedThemes[option].toLowerCase()}-small.jpg" alt="..." />
                <div class="portfolio-box-caption p-3 ${sortedThemes[option].toLowerCase()}-hover">
                    <div class="project-category text-light">Theme</div>
                    <div class="project-name">${sortedThemes[option][0].toUpperCase() + sortedThemes[option].slice(1)}</div>
                </div>
            </a>
        </div>`
        allThemesDiv.innerHTML += newApp
        }   
}

function fadeOutIn(speed) {
    currentIndex = (currentIndex+1)%Object.keys(themeOptions).length;
    //let theme = Object.keys(themeOptions)[~~(Math.random() * Object.keys(themeOptions).length)]
    let theme = Object.keys(themeOptions)[currentIndex]
    if (!document.body.style.opacity) {
        document.body.style.opacity = 1;
    }
    var outInterval = setInterval(function() {
        document.body.style.opacity -= 0.02;
        if (document.body.style.opacity <= 0) {
            clearInterval(outInterval);
            injectTheme(theme)
            document.getElementById("switch-theme").innerText = theme
            updateMetaThemeColor()
            var inInterval = setInterval(function() {
                document.body.style.opacity = Number(document.body.style.opacity)+0.02;
                if (document.body.style.opacity >= 1)
                    clearInterval(inInterval);
            }, speed/50 );
        }
    }, speed/50 );

}

function updateMetaThemeColor() {
    fetch(`${window.location.pathname}css/theme-options/${Object.keys(themeOptions)[currentIndex].toLowerCase()}.css`)
    .then(response =>  response.text())
    .then(text => {
        let re = text.match("--accent-color:.*;")[0]
        rgb = re.split(":")[1].split(";")[0].replace(/\s/g, "")
        document.querySelector('meta[name="theme-color"]').setAttribute('content',  `rgb(${rgb})`);
        })
}

// Smooth scrolling using anime.js
function smoothScroll() {$('a.js-scroll-trigger[href*="#"]:not([href="#"])').on('click', function () {
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
                scrollTop: target.offset().top - 120,
                duration: 1000,
                easing: 'easeInOutExpo'
            });
            return false;
        }
    }
})};

addThemeData();
document.getElementById("switch-theme").addEventListener("click", () =>  {
    fadeOutIn(350);
})

