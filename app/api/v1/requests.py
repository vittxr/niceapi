##Esse arquivo faz as requisições do usuário, requisitadas no front-end
from xml.sax.handler import feature_external_ges
import requests 
from app.api.v1 import api_v1
from flask import jsonify, redirect, render_template, request, url_for, json
from bs4 import BeautifulSoup #pip install beautifulsoap4

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
           return redirect(url_for("api_v1.put_apidata", url=url, name=name, cpf=cpf, email=email, password=password))
        case ('DELETE'):
           return redirect(url_for("api_v1.delete_apidata", url=url, name=name, cpf=cpf, email=email, password=password))
    

@api_v1.route("/get_apidata")
def get_apidata():
    global res 
    res = '' 

    if request.args: 
        default_url = """
                        <label for="url" class="search-apiData__ipt-url-predefined" name="default-url">
                            http://127.0.0.1:5000/api/v1/
                        </label>"
                    """
        

        url = BeautifulSoup(default_url, features="html.parser").label.string.replace(' ', '').replace('\n', '') + request.args.get('url')
        #BeatifulSoup é uma classe que retorna o conteúdo do html
        #os replaces usados são para remover espaços em branco e quebras de linha, deixando a url em um formato adequado.
        res = requests.get(url)

    return render_template('api_manager.html', res=res)


@api_v1.route("/post_apidata", methods=["GET", "POST"])
def post_apidata():
    if request.args: 
        default_url = """
                        <label for="url" class="search-apiData__ipt-url-predefined" name="default-url">
                            https://niceeapi.herokuapp.com/api/v1/
                        </label>"
                    """
        url = BeautifulSoup(default_url, features="html.parser").label.string.replace(' ', '').replace('\n', '') + request.args.get('url')

        name = request.args.get('name')
        cpf = request.args.get('cpf')
        email = request.args.get('email')
        password = request.args.get('password')

        print(cpf, email)

        data = {
             "name": f"{name}",
             "cpf": f"{cpf}", 
             "email": f"{email}", 
             "password": f"{password}"
        }
        
        res = requests.post(url, data=json.dumps(data))
          #dumps serializa um dicionário p/ json.

    return redirect(url_for("api_v1.get_apidata"))

@api_v1.route("/put_apidata")
def put_apidata():
    pass

@api_v1.route("/delete_apidata")
def delete_apidata():
    pass