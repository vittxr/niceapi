//esse arquivo exibe os campos, de acordo com o tipo de requisição. Se for post, put ou delete, aparece os campos para o usuário preencer. 
var select = document.querySelector(".manager-api__type-request")
var request_fields = document.querySelector(".manager-api__type-request-fields")
var form = document.querySelector(".manager-api__box form")

select.addEventListener('change', ChangeTheDisplayOfRequestFields)
function ChangeTheDisplayOfRequestFields() {
    let option_selected = select.options[select.selectedIndex].text
    switch (option_selected) {
        case "GET":
            request_fields.style.display = 'none'
            break
        default: 
            //Para todos os outros caso, request_fields deve ser display: flex. Então, basta usar o default.
            request_fields.style.display = 'flex'
            form.setAttribute("methods", "post")
            break    
    }
}

