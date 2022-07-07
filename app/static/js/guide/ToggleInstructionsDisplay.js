var button = document.querySelectorAll(".instructions__button")
var buttonMarked = document.querySelector(".instructions__button--active")
var getRequestSnippet = document.querySelector(".get-request")
var postRequestSnippet = document.querySelector(".post-request")
var putRequestSnipptet = document.querySelector(".put-request")
var deleteRequestSnipptet = document.querySelector(".delete-request")

button.forEach((e, index) => {
   button[index].addEventListener('click', function () {
      changeCodeSnippet(button[index].innerHTML)
      changeButtonMarked(index)
   })
}) 

function changeCodeSnippet(button_value) {
    switch (button_value) {
        case "GET":
            getRequestSnippet.style.display="block"
            postRequestSnippet.style.display="none"
            putRequestSnipptet.style.display="none"
            deleteRequestSnipptet.style.display="none"
            break;
        case "POST":
            getRequestSnippet.style.display="none"
            postRequestSnippet.style.display="block"
            putRequestSnipptet.style.display="none"
            deleteRequestSnipptet.style.display="none"
            break;
        case "PUT": 
            getRequestSnippet.style.display="none"
            postRequestSnippet.style.display="none"
            putRequestSnipptet.style.display="block"
            deleteRequestSnipptet.style.display="none"
            break;
        case "DELETE": 
            getRequestSnippet.style.display="none"
            postRequestSnippet.style.display="none"
            putRequestSnipptet.style.display="none"
            deleteRequestSnipptet.style.display="block"
    }
}

function changeButtonMarked(index) {
    //Essa função muda o botão destacado, para qual o usuário clicou. Note que é preciso setar buttonMarked como o botão que o usuário clicou.
    buttonMarked.classList.remove("instructions__button--active")
    button[index].classList.add("instructions__button--active")
    buttonMarked = button[index]
}