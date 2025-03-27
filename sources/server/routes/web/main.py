from flask import Flask, jsonify, Blueprint, render_template, request, redirect, url_for
from server.services.database.db import get_classement, get_user_id, get_user_stats


route_web = Blueprint("web", __name__)

@route_web.route("/")
def index():
    return render_template("index.html")


@route_web.route("/elya")
def elya():
    return render_template("elya.html")

@route_web.route("/stat")
def index_stat():
    return render_template("index_stat.html")

@route_web.route("/stat/stats")
def stats():
    try:
        name=str(request.args.get("name"))
        id = get_user_id(name) 
    except: id = None 
    
    # Vérifie que le champ n'est pas vide
    if not id:  
        return render_template("index_stat.html", error="Veuillez entrer un nom d'utilisateur valide")
    
    all_stats = get_user_stats(id)

    return render_template("stats.html", all_stats=all_stats, name=name)