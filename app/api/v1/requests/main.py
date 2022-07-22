from app.api.v1 import api_v1
from flask import redirect, request, url_for

@api_v1.route("/main", methods=["GET", "POST"])
def main():     
    ##Essa rota/função serve para obter o tipo de requisição que o usuário fez, escolhida no front-end. A partir daqui, redireciona para as rotas individuais de cada requisição (GET, POST, PUT ou DELETE)
    url = request.args.get('url')
    name = request.args.get('name')
    email = request.args.get('email')
       #url é o que o usuário colocou no input. Ou seja, é o path para onde ele quer ir na api (a única opção é "usuarios" lol, mas poderia ter outras)
    selected_option = request.args.get('type-request')
       #para se obter a opção selecionada no select, basta usar o código acima.
    match selected_option:
        case ('GET'):
           return redirect(url_for("api_v1.get_apidata", url=url))

        case ('POST'):
            return redirect(url_for("api_v1.post_apidata", url=url, name=name, email=email))

        case ('PUT'):
            userToBeAltered = request.args.get('selected-user')
            return redirect(url_for("api_v1.put_apidata", url=url, name=name, email=email, userToBeAltered=userToBeAltered))


        case ('DELETE'):
            userToBeDeleted = request.args.get('selected-user')
            return redirect(url_for("api_v1.delete_apidata", url=url, name=name, email=email, userToBeDeleted=userToBeDeleted))