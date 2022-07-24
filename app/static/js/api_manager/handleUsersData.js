//Esse script guardará o resultado da requisição, para que não seja preciso fazer várias vezes. Os users serão guardados em uma lista e conforme haver o processamento no backend (quando houver delete, post ou put), nesse script altera-se a lista para deixar ela igual aos dados da api. Assim, não precisa fazer várias requisições.

var api_users = localStorage.getItem("users").split(",")
   //localStorage cria uma variável guardada na página, até que o usuário feche ela. Ou seja, caso recarregada, essa variável ainda tem o mesmo valor.

var submit_btn = document.querySelector(".manager-api__submit")
var user_select = document.querySelector(".manager-api__user-select")
var typeRequest_select = document.querySelector(".manager-api__typeRequest-select")

//É preciso verificar se as há opções no HTML. Caso não tiver, quer dizer que o usuário fez uma requisição do tipo post, put ou delete. Nesse caso, não se deve armazenar os dados de options vazios. Por isso, armazena eles apenas se haver mais de 1. Ou seja, isso quer dizer que o usuário fez uma requisição do tipo get.
if (document.querySelectorAll(".manager-api__user-option").length > 1) {
    let api_users = document.querySelectorAll(".manager-api__user-option")

    let apiUsersList = []
    for (i = 0; i < api_users.length; i++) {
        apiUsersList.push(api_users[i].innerHTML)
    }
    localStorage.setItem("users", apiUsersList.join(','))
} else {
    //Esse else serve para criar novas opções para o select, pois no caso de uma requisição diferente de get, os options ficam vazios. Por isso, cria-se options usando o codigo abaixo
    let api_users = localStorage.getItem("users").split(",")
    let user_disabled = localStorage.getItem("user_disabled").split(',')
    for (i=0; i < api_users.length; i++) {
        new_option = new Option(api_users[i])
        
        for(j=0; j < user_disabled.length; j++) {
            if (api_users[i] == user_disabled[j]) {
            new_option.disabled = true
            }
        }

        user_select.add(new_option)
    }
}

submit_btn.addEventListener('click', doActionInApiUsers)

function doActionInApiUsers() {
    let user_selected = user_select.options[user_select.selectedIndex].text

    user_disabled = localStorage.getItem("user_disabled")
    localStorage.setItem("user_disabled", user_disabled +',' + user_selected.toString())
       //user_disabled deve ser como uma lista de usuário desabilitados. Se houver um delete ou put, esse usuário é desabilitado. Isso pode acontecer várias vezes, por isso há a concatenação da variável localStorage com o novo usuário deletado ou alterado. 
}

