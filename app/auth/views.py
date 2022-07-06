from flask_login import login_required, current_user
from app.auth import auth
from flask import render_template, url_for, redirect, request
from flask_login import login_user, logout_user
from ..models import User
from app import db

@auth.route("/")
def auth_page():
    auth_mode = request.args.get('auth_mode')
      #pega-se o args enviado pelo url_for do html. Caso o usuário clicar no link de fazer login (sign in), muda-se o auth_mode. Essa variável será utilizada para uma condicional no jinja, que exibe o formulário de login ou de cadastro (sign-in e sign-up), de acordo com o valor de auth_mode.
    if not auth_mode: 
       auth_mode = "sign_up"

    print(auth_mode)
    return render_template("auth.html", auth_mode = auth_mode)

@auth.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.form: 
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return render_template("auth.html", auth_mode="sign_in")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.form:
        user = User.query.filter_by(email=request.form['email']).first()

        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for("main.api_manager"))

    return render_template("auth.html", auth_mode="sign_in")

@auth.route('/logout')
def logout ():
    logout_user()
    return redirect(url_for("auth.login"))