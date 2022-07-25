from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, request, url_for
from app.models import Api_user
from ...utils import doDbAction, generateApiData

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


    ##-> Caso a requisição seja feito a partir do postman ou por código:      
    data = [request.args.get("newUserName"), request.args.get('newUserEmail'), request.args.get("userToBeAltered")]
    print(data)
    if data[0] != None and data[1] != None and data[2] != None: 
       try:
            userToBeAltered = Api_user.query.filter_by(email=data[2]).first()
            
            if userToBeAltered:
                userToBeAltered.name = data[0]
                userToBeAltered.email = data[1]
                return doDbAction(userToBeAltered, 'postman', 'add') 
            return jsonify({"status": "success, but...", "message": "the user you are trying to alter does'nt exist. The request worked though. Choose an existing user"})
       except: 
            #caso o usuário já exista no banco de dados: 
            abort(make_response(jsonify(error="This user email already exists"), 400))

    ##Caso algum dos campos estejam vazio:
    global emptyFields
    emptyFields = []
    for d in range(len(data)):
        if data[d] == None:
           global emptyField
           emptyField = ""
           if d == 0:
              emptyField = "newUserName"
           elif d == 1:
              emptyField = "newUserEmail"
           elif d == 2:
              emptyField = "userToBeAltered" 
        
           if emptyField != "":
              emptyFields.append(emptyField)
    abort(make_response(jsonify(error=f"The {emptyFields} arguments can't be null"), 400))

    ##-> Caso seja feito a partir do código:
    """ data = request.get_json("data")
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
           abort(make_response(jsonify(error="The request must be send in json format."), 400)) """