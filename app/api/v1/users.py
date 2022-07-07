import sqlalchemy
from app.api.v1 import api_v1
from flask import jsonify, redirect, render_template, request, abort, url_for 
from app.models import User 
from app import db
from sqlalchemy.exc import IntegrityError

@api_v1.route("/usuarios", methods=["GET"])
def usuarios():
    users = User.query.all()
    for i in range(len(users)):
        users[i] = users[i].to_dict()
    return jsonify(users)

@api_v1.route("/create_user", methods=["GET", "POST"])
def create_user():
    user_infoPosted = request.get_json("res")
    try:
        user = User(name=user_infoPosted['name'], email=user_infoPosted['email'], password=user_infoPosted['password'])
        db.session.add(user)
        db.session.commit()
    except: 
       return render_template("api_manager.html", error="Email is already registered")

    return redirect(url_for('api_v1.get_apidata'))
