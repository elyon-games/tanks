from flask import Blueprint
from common.config import getConfig
from .gateway import route_client_gateway

route_client = Blueprint("client", __name__)
@route_client.route("/info", methods=["GET"])
def info():
    config = getConfig("server")
    return {
        "version": config["version"],
        "key": config["key"]
    }

route_client.register_blueprint(route_client_gateway, url_prefix="/gateway")