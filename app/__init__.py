from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
       #Isso permite que qualquer domínio da internet acesse nossas rotas. Isso permite que um usuário faça um aplicação e fazer requisições por front-end.
       #Além disso, pode-se passar mais argumentos. Por exemplo: resources(r'api/*': origins: "*"). Isso liberaria acesso apenas às rotas nossas de api e poderia ser feito por qualquer lugar (origins: "*")
    app.config.from_object(config[config_name])

    db.init_app(app)
       #inicilização do db

    from app.main import main as main_bp
    from app.api.v1 import api_v1 as api_v1_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app