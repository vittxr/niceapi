/*Esse arquivo tem a função de mudar a cor da navbar quando o usuário "scrollar" para baixo */

var nav = document.querySelector(".navbar");
window.addEventListener("scroll", function(event) {
    if(window.scrollY > 500) {
        nav.style.background = "#0D0D0D";
    } else {
        nav.style.background = "transparent";
    }
})