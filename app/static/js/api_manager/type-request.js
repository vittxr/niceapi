//esse arquivo exibe os campos, de acordo com o tipo de requisição. Se for post, put ou delete, aparece os campos para o usuário preencher. 
var input = document.querySelector(".manager-api__input");
   //Esse é o input que o usuário coloca a rota. Ela será definida automaticamente de acordo com a requisição que o usuário escolher no select. Isso acontece no switch case abaixo.
var select = document.querySelector(".manager-api__type-request");
var request_fields__box = document.querySelector(".manager-api__request-fields");
var request_fields__input = document.querySelectorAll(".manager-api__request-fields input");
var form = document.querySelector(".manager-api__box form");
var select_users = document.querySelector(".manager-api__select-user");

select.addEventListener('change', ChangeTheDisplayOfRequestFields)
function ChangeTheDisplayOfRequestFields() {
    let option_selected = select.options[select.selectedIndex].text
    switch (option_selected) {
        case "GET":
            request_fields__box.style.display = 'none'
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].removeAttribute("required", "")
            });
            select_users.style.display = 'none'
            input.value = "get_apidata"
            break;  

        case "POST": 
            select_users.style.display = 'none'
            request_fields__box.style.display = 'flex';
            form.setAttribute("methods", "post");
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].setAttribute("required", "")
                  //deixa os campos obrigatórios a ser preenchido.
            });
            input.value = "post_apidata";
            break;

        case "PUT":
            select_users.style.display = 'block'  
            request_fields__box.style.display = 'flex';
            form.setAttribute("methods", "post");
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].setAttribute("required", "")
                  //deixa os campos obrigatórios a ser preenchido.
            });
            input.value = "put_apidata"
            break;
            
        case "DELETE": 
            select_users.style.display = 'block'  
            request_fields__box.style.display = 'none';
            form.setAttribute("methods", "post");
            request_fields__input.forEach((e, index) => {
                request_fields__input[index].removeAttribute("required", "")
                //deixa os campos obrigatórios a ser preenchido.
            });
            input.value = "delete_apidata"
            break;
    }
}

