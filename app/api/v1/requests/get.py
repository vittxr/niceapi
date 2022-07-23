##Esse arquivo faz as requisições do usuário, requisitadas no front-end
import json
import requests 
from app.api.v1 import api_v1
from flask import jsonify, render_template, request
from app.models import Api_user

@api_v1.route("/get")
def get_apidata():
    res = requests.get("http://127.0.0.1:5000/api/v1/usuarios")
          #https://niceeapi.herokuapp.com/api/v1 (servidor)
          #http://127.0.0.1:5000/api/v1/usuarios (local)
   
    print(request)
    if (): 
        return res

    return render_template('api_manager.html', users=res.json())

@api_v1.route("/usuarios", methods=["GET"])
def usuarios():
    users = Api_user.query.all()
    for i in range(len(users)):
        users[i] = users[i].to_dict()
    return jsonify(users)