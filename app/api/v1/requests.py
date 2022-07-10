##Esse arquivo faz as requisições do usuário, requisitadas no front-end
import email
from flask_login import login_required, current_user
import requests 
from app.api.v1 import api_v1
from flask import jsonify, redirect, render_template, request, url_for, json
from app.models import User
from app import db
from ..utils import getUrl, dataToDict, userCanMakeRequest, doDbAction

@api_v1.route("/main", methods=["GET", "POST"])
@login_required
def main(): 
    ##Essa rota/função serve para obter o tipo de requisição que o usuário fez, escolhida no front-end. A partir daqui, redireciona para as rotas individuais de cada requisição (GET, POST, PUT ou DELETE)
    url = request.args.get('url')
    name = request.args.get('name')
    password = request.args.get("password")
    email = request.args.get('email')
       #url é o que o usuário colocou no input. Ou seja, é o path para onde ele quer ir na api (a única opção é "usuarios" lol, mas poderia ter outras)
    selected_option = request.args.get('type-request')
       #para se obter a opção selecionada no select, basta usar o código acima.
    match selected_option:
        case ('GET'):
           return redirect(url_for("api_v1.get_apidata", url=url))

        case ('POST'):
           usrCanMakeRequest = userCanMakeRequest()
           if usrCanMakeRequest == True:
               return redirect(url_for("api_v1.post_apidata", url=url, name=name, email=email, password=password))
           return redirect(url_for("api_v1.get_apidata", request_detail = f'{usrCanMakeRequest}'))

        case ('PUT'):
           usrCanMakeRequest = userCanMakeRequest()
           if usrCanMakeRequest == True:
               userToBeAltered = request.args.get('selected-user')
               return redirect(url_for("api_v1.put_apidata", url=url, name=name, email=email, password=password, userToBeAltered=userToBeAltered))
           return redirect(url_for("api_v1.get_apidata", request_detail = f'{usrCanMakeRequest}'))


        case ('DELETE'):
           usrCanMakeRequest = userCanMakeRequest()
           if usrCanMakeRequest == True:
               userToBeDeleted = request.args.get('selected-user')
               return redirect(url_for("api_v1.delete_apidata", url=url, name=name, email=email, password=password, userToBeDeleted=userToBeDeleted))
           return redirect(url_for("api_v1.get_apidata", request_detail = f'{usrCanMakeRequest}'))
           
@api_v1.route("/get_apidata")
def get_apidata():
    global res 
    res = ""
    if request.args.get('url'):
        url = request.args.get('url')
        full_url = getUrl(url)
        res = requests.get(full_url)

    try:
        res_json = res.json()
    except: 
        res_json = "an error occurred :/"

    if request.args.get('request_detail'): 
        res_json = request.args.get('request_detail')
           #detalhe da requisição POST, PUT e delete. Exibe uma mensagem falando se ela foi um sucesso ou não

    return render_template('api_manager.html', res_json=res_json)


@api_v1.route("/post_apidata", methods=["GET", "POST"])
def post_apidata():
    data = dataToDict( 
        name = request.args.get('name'),
        email = request.args.get('email'),
        password = request.args.get('password'),
        ) 
    #url = request.args.get('url')
    #full_url = getUrl(url)

    if data:
        new_user = User(name=data['name'], email=data['email'], password=['password'])
        doDbAction(new_user, 'site', 'add')
          #dumps serializa um dicionário p/ json.
        return redirect(url_for("api_v1.get_apidata", request_detail="request_response -> success"))

    return redirect(url_for("api_v1.get_apidata", request_detail="request_response -> error"))

@api_v1.route("/put_apidata", methods=["GET", "PUT"])
def put_apidata():
    global userToBeAltered
    userToBeAltered = ""
    data = request.args.get('userToBeAltered')
    if data: 
       ##-> Isso caso a requisição seja feita a partir do site: 
       userToBeAltered = User.query.filter_by(email=data).first()
       
       userToBeAltered.name = request.args.get("name")
       userToBeAltered.email = request.args.get("email")
       userToBeAltered.password = request.args.get("password")
       
       if userToBeAltered:
          return doDbAction(userToBeAltered, "site", "add") 
                            #user; request_origin; db_session_mode
       return redirect(url_for("api_v1.get_apidata", request_detail = "request_response -> error"))

    ##-> Caso seja feito a partir do código ou postman:
    data = request.get_json("data")
    user = User.query.filter_by(email=data["myAcessData"]['email']).first() 
    if user and user.password == data["myAcessData"]["password"]: 
        #essa condição serve para verificar se o usuário está no banco de dados e se a senha que ele enviou na data está correta.
        """
        Caso o usuário faça requisição por fontes externas, ele precisará informar seus dados, por isso verificamos aqui se ele já está logado. No site, a rota "main" que controla tudo e colocamos que, para acessa-lá, é preciso estar logado.
        """
        userToBeAltered = User.query.filter_by(email=data['userToBeAltered']['email']).first() 
       
        if userToBeAltered:
            userToBeAltered.name = data['newUser']["name"]
            userToBeAltered.email = data['newUser']["email"]
            userToBeAltered.password = data['newUser']["password"]
        
            return doDbAction(userToBeAltered, "code", "add")
        return jsonify({"status": "error", "message": "the user you are trying to alter does'nt exist."})
    return jsonify({"status": "error", "message": "your data acess is wrong or does'nt exist in database"}) 
    
@api_v1.route("/delete_apidata", methods=["GET", "DELETE"])
def delete_apidata():
    global userToBeDeleted
    userToBeDeleted = ""
    data = request.args.get('userToBeDeleted')
    if data:
       ##-> caso a requisição seja feita a partir do site:
       userToBeDeleted = User.query.filter_by(email=data).first()
       return doDbAction(userToBeDeleted, "site", "delete") 

    ##-> Caso seja feito a partir do código ou postman:
    data = request.get_json("data")
    user = User.query.filter_by(email=data["myAcessData"]["email"]).first()

    if user and user.password == data["myAcessData"]["password"]: 
        #essa condição serve para verificar se o usuário está no banco de dados e se a senha que ele enviou na data está correta.
        userToBeDeleted = User.query.filter_by(email=data['userToBeDeleted']['email']).first() 
        return doDbAction(userToBeDeleted, "code", "delete") 
