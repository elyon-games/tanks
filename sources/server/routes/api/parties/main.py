from flask import Blueprint, request, jsonify
from server.services.database.db import parties as Parties
from common.time import get_current_time
from server.routes.api.parties.private import route_parties_private
from server.routes.api.parties.public import route_parties_public
from server.middleware.auth import login_required
from server.utils import formatRes

route_parties = Blueprint("api-parties", __name__)
route_parties.register_blueprint(route_parties_public, url_prefix="/public")
route_parties.register_blueprint(route_parties_private, url_prefix="/private")

@route_parties.route("/info/<int:party_id>", methods=["GET"])
@login_required
def get_party(party_id: int):
    party = Parties.get(party_id)
    if not party:
        return formatRes("NOT_FOUND", {})
    if request.user_id not in party.get("players", []):
        return formatRes("NOT_AUTHORIZED", {})
    return formatRes("FOUND", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })


partiesToClose = [party for party in Parties.get_all() if not party.get("status") == "wait" and party.get("ended_at") is None]
for party in partiesToClose:
    party["ended_at"] = get_current_time()
    party["status"] = "close"
Parties.save()