
 //Custom Text Header //
 // ACSII slant font

// Needs to be inside <section id="login" class="shadow">
// YOU MUST ESCAPE ANY SINGLE BACKSLASHES LIKE SO: \\

let custom_text_header = `
<div class="custom-text-header"> <pre>                     __                             ___       __  

       _       _ _                   _  __                   _____       _       _   _                 
      | |     | | |                 | |/ /                  / ____|     | |     | | (_)                
      | | ___ | | | ___ _   _ ______| ' / _ __   _____  __ | (___   ___ | |_   _| |_ _  ___  _ __  ___ 
  _   | |/ _ \| | |/ _ \ | | |______|  < | '_ \ / _ \ \/ /  \___ \ / _ \| | | | | __| |/ _ \| '_ \/ __|
 | |__| | (_) | | |  __/ |_| |      | . \| | | | (_) >  <   ____) | (_) | | |_| | |_| | (_) | | | \__ \
  \____/ \___/|_|_|\___|\__, |      |_|\_\_| |_|\___/_/\_\ |_____/ \___/|_|\__,_|\__|_|\___/|_| |_|___/
                         __/ |                                                                         
                        |___/                                                                          

                                                                 </pre> </div>
`;
document.getElementById("login").innerHTML += custom_text_header
