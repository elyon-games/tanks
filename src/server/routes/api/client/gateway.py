from flask import Blueprint, request, session
import server.services.network.main as network
from server.middleware.auth import login_required

route_client_gateway = Blueprint("client_route_client_gateway", __name__)

@route_client_gateway.route("/create", methods=["POST"])
@login_required
def info():
    print(session)
    gateway = network.create_gateway(request.user_id)
    return {
        "id": gateway.gateway_ID,
        "key": gateway.gateway_KEY
    }

def test(userID, sa):
    print(userID, sa)

network.register_fonction("test", test)