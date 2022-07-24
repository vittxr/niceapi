from types import NoneType
from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from app.models import Api_user
from ...utils import dataToDict, doDbAction, generateApiData

@api_v1.route("/put", methods=["POST", "PUT"])
def put_apidata():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    global userToBeAltered
    userToBeAltered = ""
    data = request.form.get('selected-user')
    if data: 
       ##-> Isso caso a requisição seja feita a partir do site: 
       userToBeAltered = Api_user.query.filter_by(email=data).first()
       
       userToBeAltered.name = request.form.get("name")
       userToBeAltered.email = request.form.get("email")
       
       if userToBeAltered:
          return doDbAction(userToBeAltered, "site", "add") 
                            #user; request_origin; db_session_mode
       return redirect(url_for("main.api_manager", request_detail="request_response: error"))


    ##-> Caso a requisição seja feito a partir do postman:      
    data = [request.args.get("newUserName"), request.args.get('newUserEmail'), request.args.get("userToBeAltered")]
    print(data)
    if data[0] != NoneType: 
       userToBeAltered = Api_user.query.filter_by(email=data[2]).first()
      
       print(data)

       if userToBeAltered:
          userToBeAltered.name = data[0]
          userToBeAltered.email = data[1]
          return doDbAction(userToBeAltered, 'postman', 'add') 
       return jsonify({"status": "success, but...", "message": "the user you are trying to alter does'nt exist. The request worked though. Choose an existing user"})

    ##-> Caso seja feito a partir do código:
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