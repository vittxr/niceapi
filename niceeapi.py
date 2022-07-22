##transformar os usuários em um dicionario/json
##fazer uma api para armazenar os alunos

from app import create_app, db
from app.models import *
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app, db)

if __name__ == "__main__": 
   app.run(debug=1, use_reloader=False)

"""
from faker import Faker
f = Faker()
print("aooba")
#users = Api_user.query.filter_by(id=1).first()
print(users)
if len(users) < 100: 
    while len(users) < 100:
      fake_name = f.name()
      fake_email = fake_name + "@gmail.com"
      new_user = Api_user()
      new_user.name = fake_name 
      new_user.email = fake_email
      db.session.add(new_user)
      db.session.commit()   
"""

"""
from faker import Faker
f = Faker()
fake_name = f.name()
fake_email = fake_name + "@gmail.com"
new_user = Api_user()
new_user.name = fake_name 
new_user.email = fake_email
db.session.add(new_user)
db.session.commit()   
"""