from datetime import datetime

from flask import jsonify, redirect, url_for
from app import db
from app.models import User
from bs4 import BeautifulSoup #pip install beautifulsoap4
from threading import Timer
from flask_login import current_user

##funções auxiliares (usados nas rotas:
def dataToDict(name, email, password):
    data = {
        "name": f"{name}",
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

def userCanMakeRequest():
    error=""
    #essa função verifica se o usuário pode fazer requisições ainda. Além disso, ela aumenta o valor do número de requisições no banco de dados.
    if current_user.is_authenticated: 
       #user = User.query.filter_by(email=current_user.email).first()
       if current_user.requests_number == 10:
            hourTimerWillEnd = ResetRequestsNumberAfterOneDay()
            error = f"request_response -> Número máximo de requisições atingido. Para fazê-las novamente, é preciso esperar 1 dia. Você poderá fazer mais requisições amanhã, a partir das {hourTimerWillEnd.time().strftime('%H:%M')} - GMT-0 "
            return error

       current_user.requests_number = current_user.requests_number + 1
       db.session.add(current_user)
       db.session.commit()
       return True 
         #Se o retorno da função for true, o usuário pode fazer a requisição 

    error = "request_response -> é preciso estar logado para fazer esse tipo de requisição :/"
    return error

def ResetRequestsNumberAfterOneDay(): 
    usr = User.query.filter_by(email = current_user.email).first() 
    hourTimerWillEnd = datetime.now()

    t = Timer(86200.0, resetRequestsNumberInDb, (usr))
    t.start() 

    return hourTimerWillEnd

def resetRequestsNumberInDb(usr): 
    usr.requests_number = 0
    db.session.add(usr)
    db.session.commit()

def doDbAction(user, request_origin, db_session_mode):
    #-> Request origin é de o request veio, do código ou do site. Vamos usá-los para retornar diferentes tipos de resposta, caso a alteração no db seja um sucesso.
    #-> db_session_mode é a ação que o usário quer fazer no db (add ou delete)
    if db_session_mode == "add":
        db.session.add(user)
        db.session.commit()
    elif db_session_mode == "delete":
        db.session.delete(user)
        db.session.commit()
    
    if request_origin == "code": 
       return jsonify({"status": "sucess", "message": "the request was sucessful"})
         #caso request_origin seja de código, retorna-se um json para o usuário.
    elif request_origin == "site": 
       return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> success"))
          #caso request_origin seja do site, redireciona o usuário para a página principal da api, com uma resposta de sucesso.