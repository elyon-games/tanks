from flask import Flask, jsonify, Blueprint, render_template

route_web = Blueprint("web", __name__)

@route_web.route("/")
def index():
    return render_template(("index.html"))