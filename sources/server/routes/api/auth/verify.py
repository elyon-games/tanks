from flask import request, jsonify, Blueprint
from server.middleware.auth import login_required

route_auth_verify = Blueprint("api-auth-very", __name__)

@route_auth_verify.route("/", methods=["GET"])
@login_required
def verify():
    return jsonify({"message": "TOKEN_VALID", "user_id": request.user_id}), 200