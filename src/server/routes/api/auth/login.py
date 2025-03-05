from flask import request, jsonify, Blueprint
from server.services.database.db import users as Users
from server.services.tokens import create_jwt_token

route_auth_login = Blueprint("api-auth-login", __name__)
@route_auth_login.route("/", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Identifiant/Email et mot de passe sont requis"}), 400

    user = Users.login(email=email, password=password)
    if not user:
        return jsonify({"error": "Identifiants incorrects"}), 401

    return jsonify({
        "message": "CONNEXION_VALID",
        "user_id": user['id'],
        "username": user['username'],
        "token": create_jwt_token(user['id'])
    })