
 //Custom Text Header //
 // ACSII slant font

// Needs to be inside <section id="login" class="shadow">
// YOU MUST ESCAPE ANY SINGLE BACKSLASHES LIKE SO: \\

let custom_text_header = `
<div class="custom-text-header"> <pre>                     __                             ___       __  
   ____  ____  _____/ /__________  ____ ___  ____  / (_)___  / /__
  / __ \\/ __ \\/ ___/ __/ ___/ __ \\/ __ '__ \\/ __ \\/ / / __ \\/ //_/
 / / / / /_/ (__  ) /_/ /  / /_/ / / / / / / /_/ / / / / / / ,&lt;   
/_/ /_/\\____/____/\\__/_/   \\____/_/ /_/ /_/\\____/_/_/_/ /_/_/|_|  
                                                                 </pre> </div>
`;
document.getElementById("login").innerHTML += custom_text_header
