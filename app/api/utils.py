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
    
    if request_origin == "code" or request_origin=="postman": 
       return jsonify({"status": "sucess", "message": "the request was sucessful"})
         #caso request_origin seja de código, retorna-se um json para o usuário.
    elif request_origin == "site": 
       return redirect(url_for("main.api_manager", request_detail="request_response -> success"))
          #caso request_origin seja do site, redireciona o usuário para a página principal da api, com uma resposta de sucesso.

from faker import Faker
f = Faker()
def generateApiData():
    new_user = Api_user()

    fake_name = f.name()
    fake_email = (fake_name + "@gmail.com").replace(" ", "")
    new_user.name = fake_name 
    new_user.email = fake_email
    try:
        db.session.add(new_user)
        db.session.commit() 

        ##É preciso gerar um email único, mas o Faker não assegura isso, por isso faço a concatenação do fake_email + id gerado pelo db. Porém, para fazer isso, usaria-se um trigger, qua basicamente concateria o email + o id (em formato str). O problema é que o heroku não oferece suporte para isso, então resolvi fazer da forma abaixo. Basicamente, eu coloco o usuário gerado pelo Faker no db, permitindo eu acessar seu id. Ou seja, há dois commits aq (oq n parece ser mt bom, mas ok. Não consigo pensar em outra forma de resolver). O algoritmo abaixo pega o email e o id do db, concatena os dois e, por fim, faz o commit desse usuário alterado. Assim, todos usuários da api terão emails únicos, já que o id é único. 
        newUserEmail_unique = Api_user.query.filter_by(email=fake_email).first()
        altered_email = newUserEmail_unique.email + str(newUserEmail_unique.id)

        altered_email_v2 = altered_email.split("@")

        altered_email_v3 = altered_email_v2[0] + altered_email_v2[1].split(".com")[1] + "@" + altered_email_v2[1].split(".com")[0]
          #altered_email_v3 é a versão final do email, ajeitando ele da forma adequada, na forma de um email.

        newUserEmail_unique.email = altered_email_v3

        db.session.add(newUserEmail_unique)
        db.session.commit() 
    except: 
        print("user generation failed")
    