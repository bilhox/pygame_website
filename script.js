hljs.highlightAll();

var theme = "dark";

const dark_theme = "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github-dark-dimmed.min.css";
const light_theme = "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css";

function changeTheme(){
    if(theme == "dark"){
        theme = "white";

        document.getElementById("theme").setAttribute("href", light_theme);

        document.body.style.backgroundColor = "#aaeebb";
        document.body.style.color = "black";
        var elements = document.getElementsByTagName("a");

        for(var i = 0 ; i < elements.length ; i++){
            elements[i].style.color = "black";
        }

        document.getElementById("module-title").style.borderColor = "rgb(81, 99, 81)";
        document.getElementById("module-members-title").style.borderColor = "rgb(145, 120, 55)";

        elements = document.getElementsByTagName("code");

        for(var i = 0 ; i < elements.length ; i++){
            if(elements[i].className == "member-code"){
                elements[i].style.backgroundColor = "#77a783";
            } else {
                elements[i].style.backgroundColor = "#eeffcc";
            }
        }

        elements = document.getElementsByClassName("f-documentation");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#88be96";
            elements[i].style.boxShadow = "0px 0px 30px #88be96";
        }

        elements = document.getElementsByClassName("f-title-container");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#77a783";
        }

        elements = document.getElementsByClassName("module-documentation");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#88be96";
            elements[i].style.boxShadow = "0px 0px 30px #88be96";
        }

        elements = document.getElementsByTagName("kbd");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#c4f3cf";
            elements[i].style.borderColor = "#b4b4b4";
            elements[i].style.color = "black";
        }

    } else {
        theme = "dark";

        document.getElementById("theme").setAttribute("href", dark_theme);

        document.body.style.backgroundColor = "#1E1E1E";
        document.body.style.color = "white";

        var elements = document.getElementsByTagName("a");

        for(var i = 0 ; i < elements.length ; i++){
            elements[i].style.color = "white";
        }

        document.getElementById("module-title").style.borderColor = "rgb(188, 231, 190)";
        document.getElementById("module-members-title").style.borderColor = "rgb(231, 219, 188)";
        elements = document.getElementsByTagName("code");

        for(var i = 0 ; i < elements.length ; i++){
            if(elements[i].className != "member-code"){
                elements[i].style.backgroundColor = "#121212";
            }
            else{
                elements[i].style.backgroundColor = "#252526";
            }
        }

        elements = document.getElementsByClassName("f-documentation");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#2b2b2c";
            elements[i].style.boxShadow = "0px 0px 30px #2b2b2c";
            
        }

        elements = document.getElementsByClassName("f-title-container");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#252526";
        }

        elements = document.getElementsByClassName("module-documentation");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#2b2b2c";
            elements[i].style.boxShadow = "0px 0px 30px #2b2b2c";
        }

        elements = document.getElementsByTagName("kbd");

        for(var i = 0; i < elements.length ; i++){
            elements[i].style.backgroundColor = "#323131";
            elements[i].style.borderColor = "#b4b4b4";
            elements[i].style.color = "white";
        }
    }
}