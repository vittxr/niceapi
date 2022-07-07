##transformar os usuários em um dicionario/json
##fazer uma api para armazenar os alunos

from app import create_app, db
from app.models import *
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app, db)

if __name__ == "__main__":
   app.run(debug=1, use_reloader=False)


""" def createTable():
    db.create_all()

createTable()    

def geraUsr():
from models import User
newUser = User()
newUser.id=1
newUser.nome='vitor'
newUser.email='vitor.roberto3022@gmail.com'
newUser.senha='vitor123'
db.session.add(newUser)
db.session.commit()

geraUsr() """
