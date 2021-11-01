function get_base_sha(app,theme) {
    url = `https://api.github.com/repos/gilbn/theme.park/contents/CSS/themes/${app}/${app}-base.css`
    const date = new Date().toUTCString();
  fetch(url, {
    headers: { "If-Modified-Since": date }
    })
    .then(res => res.json())
    .then(data => (injectTheme(app,theme,sha=data.sha || "ratelimited")))
    .catch(err => { throw err });
}

 function injectTheme(app,theme,sha,container="head") {
    if (container === "head") {
        html_element = document.head;
    } else html_element = document.body;
    let link = document.createElement("link");
    url = "https://theme-park.dev/CSS/themes/"
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = `${url}/${app}/${theme}.css?v=${sha}`;
  
    html_element.appendChild(link);
  }

   function injectAddon(app,addon,container="head") {
    if (container === "head") {
        html_element = document.head;
    } else html_element = document.body;
    let link = document.createElement("link");
    url = "https://theme-park.dev/CSS/addons/"
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = `${url}/${app}/${addon}.css`;
  
    html_element.appendChild(link);
  }
 
  
//   {
//     if (res.status) {
//         res.json()
//         .then(data => console.log(data))
//     }  else {
//         res.json()
//         .then(data =>  console.log(data))
//         console.info("%c theme.park %c ".concat("ERROR", " "), "color: white; background: #009688; font-weight: 700; font-size: 24px; font-family: Monospace;", "color: red; background: white; font-weight: 700; font-size: 24px; font-family: Monospace;");
//         console.info(`%c Error %c Failed to fetch the url, double check the name passed in your subfilter.. `, "color: white; background: red; font-weight: 700;", "color: red; background: white; font-weight: 700;");
//     }
// })


