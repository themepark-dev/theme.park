
 //Custom Text Header //
 // ACSII slant font

// Needs to be inside <section id="login" class="shadow">
// YOU MUST ESCAPE ANY SINGLE BACKSLASHES LIKE SO: \\

let custom_text_header = `
<div class="custom-text-header"> <pre>                     __                             ___       __  
   ____  ____  _____/ /__________  ____ ___  ____  / (_)___  / /__
                                
     _   _    ____   ___  _   _ 
    | | / \  |  _ \ / _ \| \ | |
 _  | |/ _ \ | |_) | | | |  \| |
| |_| / ___ \|  __/| |_| | |\  |
 \___/_/   \_|_|    \___/|_| \_|
                                
                                                                 </pre> </div>
`;
document.getElementById("login").innerHTML += custom_text_header
