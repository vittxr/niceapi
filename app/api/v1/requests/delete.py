from app.api.v1 import api_v1
from flask import abort, jsonify, make_response, redirect, request, url_for
from app.models import Api_user
from ...utils import doDbAction, generateApiData

@api_v1.route("/delete", methods=["POST", "DELETE"])
def delete_apidata():
   while len(Api_user.query.all()) < 100:
      generateApiData()

   ##-> caso a requisição seja feita a partir do site:
   global userToBeDeleted
   userToBeDeleted = ""
   data = request.form.get('selected-user')
   print(data)
   if data:
      userToBeDeleted = Api_user.query.filter_by(email=data).first()
      if userToBeDeleted: 
         return doDbAction(userToBeDeleted, "site", "delete") 
      return redirect(url_for("main.api_manager", request_detail="request_response: error"))

   ##-> Caso a requisição seja feito a partir do postman ou por código:      
   email = request.args.get('userToBeDeleted')
   if email:
      userToBeDeleted = Api_user.query.filter_by(email=email).first() 
      if userToBeDeleted: 
         return doDbAction(userToBeDeleted, "code", "delete")
      return jsonify({"status": "success, but...", "message": "the user you are trying to delete does'nt exist. The request worked though. Choose an existing user"}) 
   abort(make_response(jsonify(error=f"The [userToBeDeleted] arguments can't be null"), 400))