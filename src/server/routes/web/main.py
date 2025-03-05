from flask import Flask, jsonify, Blueprint, render_template
from server.services.database.db import get_classement, get_user_id, get_user_stats


route_web = Blueprint("web", __name__)

@route_web.route("/")
def index():
    return render_template(("index.html"))

@route_web.route("/stat")
def stat():
    try: 
        return 
    except:
        return