##Esse arquivo faz as requisições do usuário, requisitadas no front-end
import json
import requests
from app.api.utils import generateApiData 
from app.api.v1 import api_v1
from flask import jsonify, render_template, request
from app.models import Api_user

@api_v1.route("/get", methods=["GET", "POST"])
def get_apidata():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    res = requests.get("https://niceeapi.herokuapp.com/api/v1/usuarios")
          #https://niceeapi.herokuapp.com/api/v1/usuarios (servidor)
          #http://127.0.0.1:5000/api/v1/usuarios (local)

    if request.form.get("requestMadeBySite"):
       return render_template('api_manager.html', users=res.json())
            #return se a requisição foi feita pelo site

    return json.dumps(res.json())
        #return se a requisição foi feita por código ou pelo postman.

@api_v1.route("/usuarios", methods=["GET"])
def usuarios():
    users = Api_user.query.order_by(Api_user.name).all()
    for i in range(len(users)):
        users[i] = users[i].to_dict()
    return jsonify(users)