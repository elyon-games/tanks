from flask import Blueprint
from server.routes.api.auth import route_auth
from server.routes.api.users import route_users
from server.routes.api.badges import route_badges
from server.routes.api.client.main import route_client

route_api = Blueprint("api", __name__)

route_api.register_blueprint(route_auth, url_prefix="/auth")
route_api.register_blueprint(route_users, url_prefix="/users")
route_api.register_blueprint(route_badges, url_prefix="/badges")
route_api.register_blueprint(route_client, url_prefix="/client")