from flask import request, jsonify, Blueprint
from server.services.database.db import users as Users
from server.services.tokens import create_jwt_token

route_auth_register = Blueprint("api-auth-register", __name__)
@route_auth_register.route("/", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    identifiant = data.get("identifiant")
    email = data.get("email")
    password = data.get("password")
    
    if not username:
        return jsonify({"error": "Le nom d'utilisateur est requis"}), 400
    if not identifiant:
        return jsonify({"error": "L'identifiant est requis"}), 400
    if not email:
        return jsonify({"error": "L'email est requis"}), 400
    if not password:
        return jsonify({"error": "Le mot de passe est requis"}), 400

    if Users.existed(identifiant) or Users.existed(email):
        return jsonify({"error": "Ses informations sont déjà utiliée"}), 400

    user = Users.create(username=username, identifiant=identifiant, email=email, password=password)
    return jsonify({
        "message": "Utilisateur créé avec succès",
        "user_id": user.get("id"),
        "token": create_jwt_token(user.get("id")),
        "username": user.get("username")
    }), 201