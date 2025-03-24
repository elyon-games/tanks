from flask import Blueprint
from server.routes.api.auth.login import route_auth_login
from server.routes.api.auth.register import route_auth_register
from server.routes.api.auth.verify import route_auth_verify

route_api_auth = Blueprint("api-auth", __name__)

route_api_auth.register_blueprint(route_auth_login, url_prefix="/login")
route_api_auth.register_blueprint(route_auth_register, url_prefix="/register")
route_api_auth.register_blueprint(route_auth_verify, url_prefix="/verify")