var button = document.querySelectorAll(".instructions__button");

var getRequestSnippet = document.querySelector(".get-request");
var postRequestSnippet = document.querySelector(".post-request");


button.forEach((e, index) => {
   button[index].addEventListener('click', function () {
      changeCodeSnippet(button[index].innerHTML)
   })
}) 

function changeCodeSnippet(button_value) {
    switch (button_value) {
        case "GET":
            getRequestSnippet.style.display="block";
            postRequestSnippet.style.display="none"
            break;
        case "POST":
            getRequestSnippet.style.display="none";
            postRequestSnippet.style.display="block";
            break;
    }
}