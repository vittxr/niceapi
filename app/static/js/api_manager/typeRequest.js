//esse arquivo exibe os campos, de acordo com o tipo de requisição. Se for post, put ou delete, aparece os campos para o usuário preencher. 

var select = document.querySelector(".manager-api__route-select")
var request_fields__box = document.querySelector(".manager-api__request-fields")
var request_fields__input = document.querySelectorAll(".manager-api__request-fields input")
var form = document.querySelector(".manager-api__box form")
var select_users = document.querySelector(".manager-api__user-select")
var managerApiForm = document.querySelector(".manager-api__form")

select.addEventListener('change', ChangeTheDisplayOfRequestFields)
function ChangeTheDisplayOfRequestFields() {
    let option_selected = select.options[select.selectedIndex].text
    let TypeRequestSelected = option_selected.split("/api/v1/")
    switch (TypeRequestSelected[1]) {
        case "get":
            select_users.style.display = 'none'
            request_fields__box.style.display = 'none'
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].removeAttribute("required", "")
            });
            managerApiForm.action = "/api/v1/" + TypeRequestSelected[1]
            break;  

        case "post": 
            select_users.style.display = 'none'
            request_fields__box.style.display = 'flex';
            form.setAttribute("methods", "post");
            request_fields__input[0].placeholder = "name..."
            request_fields__input[1].placeholder = "email..."
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].setAttribute("required", "")
                  //deixa os campos obrigatórios a ser preenchido.
            });
            managerApiForm.action = "/api/v1/" +  TypeRequestSelected[1]
            break;

        case "put":
            select_users.style.display = 'block'  
            request_fields__box.style.display = 'flex';
            request_fields__input[0].placeholder = "new user name..."
            request_fields__input[1].placeholder = "new user email..."

            request_fields__input.forEach((e, index) => {
                request_fields__input[index].setAttribute("required", "")
                  //deixa os campos obrigatórios a ser preenchido.
            });
            managerApiForm.action = "/api/v1/" +  TypeRequestSelected[1]
            break;
            
        case "delete": 
            select_users.style.display = 'block'  
            request_fields__box.style.display = 'none';
            form.setAttribute("methods", "post");
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].removeAttribute("required", "")
                //deixa os campos obrigatórios a ser preenchido.
            });
            managerApiForm.action = "/api/v1/" +  TypeRequestSelected[1]
            break;
    }
}

