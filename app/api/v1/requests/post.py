from types import NoneType
from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from app.models import Api_user
from ...utils import dataToDict, doDbAction, generateApiData

@api_v1.route("/post", methods=["POST"])
def post_apidata():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    data = [request.form.get("name"), request.form.get('email')]

    ##Caso o usuário faça a requisição pelo site:
    if type(data[0]) != NoneType:
        data_dict = dataToDict( 
            name = data[0],
            email = data[1],
        ) 
        new_user = Api_user(name=data_dict['name'], email=data_dict['email'])
        if new_user: 
           return doDbAction(new_user, 'site', 'add')
        return render_template("api_manager.html", request_detail = "request_response: error")

    ##caso a requisição seja por postman:           
    data = [request.args.get("name"), request.args.get('email')]
    print(data)
    if data[0] != NoneType: 
       data_dict = dataToDict( 
            name = data[0],
            email = data[1],
        ) 
       new_user = Api_user(name=data_dict['name'], email=data_dict['email'])
       return doDbAction(new_user, 'postman', 'add') 
        

    ##Caso ele faça a requisição por código:
    try: 
       data = request.get_json("data")
       if data:
          new_user = Api_user(name=data['name'], email=data['email']) 
          return doDbAction(new_user, "code", "add")
    except:
       ##erros:  
       if type(data) != dict:
           # 1- caso a data enviada pelo usuário deja diferente de json
           abort(make_response(jsonify(error="The request must be send in json format."), 400))
       
       #2- caso o usuário já exista no banco de dados: 
       abort(make_response(jsonify(error="This user already exists"), 400))
       
       