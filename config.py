import os 

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
      #getenv() faz a mesma coisa que os.environ.get()
      #SQLALCHEMY é um ORM
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    SECRET_KEY = os.getenv("SECRET_KEY")

config = {
    'default': Config
}