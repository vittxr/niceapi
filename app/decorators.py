from flask import abort
from flask_login import current_user  
from functools import wraps 

def usuario(funcao):
    @wraps(funcao)
    def decorated_function(*args, **kwargs):
        if not current_user:
            return abort(403)
        return funcao(*args, **kwargs)
    return decorated_function
    