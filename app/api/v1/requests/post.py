from types import NoneType
from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, request, url_for
from app.models import Api_user
from ...utils import dataToDict, doDbAction, generateApiData

@api_v1.route("/post", methods=["POST"])
def post_apidata():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    data = [request.form.get("name"), request.form.get('email')]

    ##Caso o usuário faça a requisição pelo site:
    if type(data[0]) != NoneType:
        try:
            data_dict = dataToDict( 
                name = data[0],
                email = data[1],
            ) 
            new_user = Api_user(name=data_dict['name'], email=data_dict['email'])
            if new_user: 
               return doDbAction(new_user, 'site', 'add')
            return redirect(url_for("main.api_manager", request_detail="request_response: error"))
        except: 
            return redirect(url_for("main.api_manager", request_detail="request_response: this user already exists."))



    ##caso a requisição seja por postman ou código:            
    data = [request.args.get("name"), request.args.get('email')]
    if data[0] != None and data[1] != None: 
       try: 
            data_dict = dataToDict( 
                    name = data[0],
                    email = data[1],
                ) 
            new_user = Api_user(name=data_dict['name'], email=data_dict['email'])
            return doDbAction(new_user, 'postman', 'add') 
       except: 
            #caso o usuário já exista no banco de dados: 
            abort(make_response(jsonify(error="This user already exists"), 400))

    ##Caso algum dos campos estejam vazio:
    global emptyFields
    emptyFields = []
    for d in range(len(data)):
        if data[d] == None:
            global emptyField
            emptyField = ""
            if d == 0:
                emptyField = "name"
            elif d == 1:
                emptyField = "email"
        
            if emptyField != "":
                emptyFields.append(emptyField)
    abort(make_response(jsonify(error=f"The {emptyFields} arguments can't be null"), 400))

       
       