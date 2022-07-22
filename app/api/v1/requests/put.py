from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from app.models import Api_user
from ...utils import doDbAction, generateApiData

@api_v1.route("/put_apidata", methods=["GET", "PUT"])
def put_apidata():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    global userToBeAltered
    userToBeAltered = ""
    data = request.args.get('userToBeAltered')
    if data: 
       ##-> Isso caso a requisição seja feita a partir do site: 
       userToBeAltered = Api_user.query.filter_by(email=data).first()
       
       userToBeAltered.name = request.args.get("name")
       userToBeAltered.email = request.args.get("email")
       userToBeAltered.password = request.args.get("password")
       
       if userToBeAltered:
          return doDbAction(userToBeAltered, "site", "add") 
                            #user; request_origin; db_session_mode
       return render_template("api_manager.html", request_detail = "request_response -> error")

    ##-> Caso seja feito a partir do código ou postman:
    data = request.get_json("data")
    
    try: 
        if data:
            userToBeAltered = Api_user.query.filter_by(email=data['userToBeAltered']['email']).first() 
            print(userToBeAltered)
        
            if userToBeAltered:
                userToBeAltered.name = data['newUser']["name"]
                userToBeAltered.email = data['newUser']["email"]
        
                return doDbAction(userToBeAltered, "code", "add")
            return jsonify({"status": "success, but...", "message": "the user you are trying to alter does'nt exist. The request worked though. Choose an existing user"})
    except: 
       ##erros:  
       if type(data) != dict:
           # 1- caso a data enviada pelo usuário deja diferente de json
           abort(make_response(jsonify(error="The request must be send in json format."), 400))