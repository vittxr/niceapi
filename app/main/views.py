from flask import render_template
from app.main import main

@main.route("/api_manager")
def api_manager():
    return render_template("api_manager.html")