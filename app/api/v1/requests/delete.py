from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from app.models import Api_user
from ...utils import doDbAction, generateApiData

@api_v1.route("/delete", methods=["GET", "DELETE"])
def delete_apidata():
   while len(Api_user.query.all()) < 100:
      generateApiData()

   global userToBeDeleted
   userToBeDeleted = ""
   data = request.args.get('userToBeDeleted')
   if data:
      ##-> caso a requisição seja feita a partir do site:
      userToBeDeleted = Api_user.query.filter_by(email=data).first()
      if userToBeDeleted: 
         return doDbAction(userToBeDeleted, "site", "delete") 
      return redirect(url_for("main.api_manager", request_detail="request_response -> error"))

   ##-> Caso seja feito a partir do código ou postman: 
   try: 
      data = request.get_json("data")
      if data:
         userToBeDeleted = Api_user.query.filter_by(email=data['userToBeDeleted']['email']).first() 
         if userToBeDeleted: 
             return doDbAction(userToBeDeleted, "code", "delete")
         return jsonify({"status": "success, but...", "message": "the user you are trying to delete does'nt exist. The request worked though. Choose an existing user"}) 
   except: 
      ##erros:  
      if type(data) != dict:
         # 1- caso a data enviada pelo usuário deja diferente de json
         abort(make_response(jsonify(error="The request must be send in json format."), 400))  