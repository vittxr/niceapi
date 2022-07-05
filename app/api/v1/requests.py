##Esse arquivo faz as requisições do usuário, requisitadas no front-end
from flask_login import login_required, current_user
import requests 
from app.api.v1 import api_v1
from flask import redirect, render_template, request, url_for, json
from bs4 import BeautifulSoup #pip install beautifulsoap4
from app.models import User
from app import db
import time

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
           cond = userCanMakeRequest()
           if cond:
               return redirect(url_for("api_v1.post_apidata", url=url, name=name, cpf=cpf, email=email, password=password))

        case ('PUT'):
           userToBeAltered = request.args.get('selected-user')
           return redirect(url_for("api_v1.put_apidata", url=url, name=name, cpf=cpf, email=email, password=password, userToBeAltered=userToBeAltered))
           #return render_template('api_manager.html', error=f'Você fez o número máximo de requisições por agora. Falta {tempo_restante} para que você possa fazê-las novamente')


        case ('DELETE'):
           cond = userCanMakeRequest()
           if cond:
               userToBeDeleted = request.args.get('selected-user')
               return redirect(url_for("api_v1.delete_apidata", url=url, name=name, cpf=cpf, email=email, password=password, userToBeDeleted=userToBeDeleted))


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
@login_required
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
@login_required
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

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> success"))

    return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> error"))
    

@api_v1.route("/delete_apidata")
@login_required
def delete_apidata():
    userToBeDeleted = request.args.get('userToBeDeleted')

    user = User.query.filter_by(email=userToBeDeleted).first()

    if user:
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> success"))

    if not current_user.is_authenticated: 
       return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> É preciso estar logado para fazer DELETE"))
       

    return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> error"))

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

#timerToResetRequests = time.sleep(86400)
def userCanMakeRequest():
    #essa função verifica se o usuário pode fazer requisições ainda. Além disso, ela aumenta o valor do número de requisições no banco de dados.
    if current_user.is_authenticated: 
       #user = User.query.filter_by(email=current_user.email).first()
       if current_user.requests_number == 10:
            return redirect(url_for("api_v1.get_apidata", request_detail = f"request_response -> Número máximo de requisições atingido. Para fazê-las novamente, é preciso esperar 1 dia. Tempo restante para resetar as requisições:"))

       current_user.requests_number = current_user.requests_number + 1
       db.session.add(current_user)
       db.session.commit()
       return True 
         #Se o retorno da função for true, o usuário pode fazer a requisição 

    return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> é preciso estar logado para fazer esse tipo de requisição :/"))