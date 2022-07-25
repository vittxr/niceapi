from flask import redirect, render_template, request
from app.main import main
from app.api.utils import generateApiData
from ..models import Api_user

request_detail = None 
@main.route("/")
def api_manager():
    while len(Api_user.query.all()) < 100:
        generateApiData()

    request_detail = request.args.get("request_detail")
    return render_template("api_manager.html", request_detail=request_detail)