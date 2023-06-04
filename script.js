hljs.highlightAll();

var theme = "dark";

const code_dark_theme = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github-dark-dimmed.min.css";
const code_light_theme = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css";

const light_theme = "light_theme.css";
const dark_theme = "dark_theme.css";

function changeTheme(){
    if(theme == "dark"){
        theme = "white";

        document.getElementById("code-theme").setAttribute("href", code_light_theme);
        document.getElementById("theme").setAttribute("href", light_theme);

    } else {
        theme = "dark";

        document.getElementById("code-theme").setAttribute("href", code_dark_theme);
        document.getElementById("theme").setAttribute("href", dark_theme)
    }
}
