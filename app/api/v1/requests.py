##Esse arquivo faz as requisições do usuário, requisitadas no front-end
import requests 
from app.api.v1 import api_v1
from flask import jsonify, redirect, render_template, request, url_for, json
from bs4 import BeautifulSoup #pip install beautifulsoap4
from app.models import User
from app import db

@api_v1.route("/main", methods=["GET", "POST"])
def main(): 
    ##Essa rota/função serve para obter o tipo de requisição que o usuário fez, escolhida no front-end. A partir daqui, redireciona para as rotas individuais de cada requisição (GET, POST, PUT ou DELETE)
    url = request.args.get('url')
    name = request.args.get('name')
    cpf = request.args.get('cpf')
    password = request.args.get("password")
    email = request.args.get('email')
       #url é o que o usuário colocou no input. Ou seja, é o path para onde ele quer ir na api (a única opção é "usuarios" lol, mas poderia ter outras)
    selected_option = request.args.get('type-request')
       #para se obter a opção selecionada no select, basta usar o código acima.
    match selected_option:
        case ('GET'):
           return redirect(url_for("api_v1.get_apidata", url=url))
        case ('POST'):
           return redirect(url_for("api_v1.post_apidata", url=url, name=name, cpf=cpf, email=email, password=password))
        case ('PUT'):
           userToBeAltered = request.args.get('selected-user')
           print(userToBeAltered)
           return redirect(url_for("api_v1.put_apidata", url=url, name=name, cpf=cpf, email=email, password=password, userToBeAltered=userToBeAltered))
        case ('DELETE'):
           return redirect(url_for("api_v1.delete_apidata", url=url, name=name, cpf=cpf, email=email, password=password))
    

@api_v1.route("/get_apidata")
def get_apidata():
    global res 
    res = ""
    if request.args.get('url'):
        url = request.args.get('url')
        full_url = getUrl(url)
        res = requests.get(full_url)

    try:
        res_json = res.json()
    except: 
        res_json = "an error occurred :/"

    if request.args.get('request_detail'): 
        res_json = json.dumps(request.args.get('request_detail'))
           #detalhe da requisição POST, PUT e delete. Exibe uma mensagem falando se ela foi um sucesso ou não

    return render_template('api_manager.html', res_json=res_json)


@api_v1.route("/post_apidata", methods=["GET", "POST"])
def post_apidata():
    data = dataToDict( 
        name = request.args.get('name'),
        cpf = request.args.get('cpf'),
        email = request.args.get('email'),
        password = request.args.get('password'),
        ) 

    url = request.args.get('url')
    full_url = getUrl(url)

    if data and url:
        res = requests.post(full_url, data=json.dumps(data))
          #dumps serializa um dicionário p/ json.
        return redirect(url_for("api_v1.get_apidata", request_detail="request_response -> success"))

    return redirect(url_for("api_v1.get_apidata", request_detail="request_response -> error"))

@api_v1.route("/put_apidata")
def put_apidata():
    userToBeAltered = request.args.get('userToBeAltered')
    print(f"userTobeAltered => {userToBeAltered}")

    user = User.query.filter_by(email=userToBeAltered).first()
    print(user)
    
    if user:
        user.name = request.args.get("name")
        user.cpf = request.args.get("cpf")
        user.email = request.args.get("email")
        user.password = request.args.get("password")

        print(user)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("api_v1.get_apidata", resquest_detail = "request_response -> success"))

    return redirect(url_for("api_v1.get_apidata", resquest_detail = "request_response -> error"))
    

@api_v1.route("/delete_apidata")
def delete_apidata():
    pass

##funções auxiliares (usados nas rotas:
def dataToDict(name, cpf, email, password):
    data = {
        "name": f"{name}",
        "cpf": f"{cpf}", 
        "email": f"{email}", 
        "password": f"{password}"
    }
    return data

def getUrl(url):
    default_url = """
                        <label for="url" class="search-apiData__ipt-url-predefined" name="default-url">
                            https://niceeapi.herokuapp.com/api/v1/
                        </label>"
                  """
    full_url = BeautifulSoup(default_url, features="html.parser").label.string.replace(' ', '').replace('\n', '') + url
        #BeatifulSoup é uma classe que retorna o conteúdo do html
        #os replaces usados são para remover espaços em branco e quebras de linha, deixando a url em um formato adequado.
    return full_url