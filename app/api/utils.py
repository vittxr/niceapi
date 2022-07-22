from flask import jsonify, redirect, render_template, url_for
from app import db
from app.models import Api_user

##funções auxiliares (usados nas rotas:
def dataToDict(name, email):
    data = {
        "name": f"{name}",
        "email": f"{email}", 
    }
    return data

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
       return render_template("api_manager.html", request_detail = "request_response -> success")
          #caso request_origin seja do site, redireciona o usuário para a página principal da api, com uma resposta de sucesso.

from faker import Faker
f = Faker()
def generateApiData():
    fake_name = f.name()
    fake_email = fake_name + "@gmail.com"
    new_user = Api_user()
    new_user.name = fake_name 
    new_user.email = fake_email.replace(" ", "")
    try:
        db.session.add(new_user)
        db.session.commit()   
    except: 
        print("xD")
    