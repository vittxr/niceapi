from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
  #login view pede o endpoint da rota do nosso login

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
       #inicilização do db e do login

    from app.auth import auth as auth_bp
    from app.main import main as main_bp
    from app.api.v1 import api_v1 as api_v1_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app