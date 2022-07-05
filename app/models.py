from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

class User(db.Model, UserMixin):
    __tablename__ = "tb_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    requests_number = db.Column(db.Integer, nullable=False, default=1) 
        #db.session.remove() remove o que tem dentro da session. Isso é útil. Se der erro em subir um usuário, por faltar algum dado, ele ainda fica na session, por isso é preciso removê-lo e colocá-lo novamente (pelo menos no caso do postgresql)

    """  @property
    def password(self):
        raise Exception("Este não é um atributo que possa ser lido")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
   
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    """
    def to_dict(self):
        return {
            "id":self.id, 
            "name":self.name,
            "cpf":self.cpf,
            "email":self.email,
        }        
    