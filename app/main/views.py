from flask import render_template
from app.main import main
from app.api.utils import generateApiData
from ..models import Api_user
import sys

@main.route("/")
def api_manager():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    usersInfo=len(Api_user.query.all())
    return render_template("api_manager.html", usersInfo=usersInfo)