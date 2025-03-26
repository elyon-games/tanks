from flask import Blueprint, request, jsonify
from server.services.database.db import parties as Parties
from server.services.database.db import maps as Maps
from server.services.database.db import users as Users
from server.middleware.auth import login_required
from server.utils import formatRes

route_parties_private = Blueprint("api-parties-private", __name__)

# Créer une partie privée
@route_parties_private.route("/create", methods=["POST"])
@login_required
def create_party():
    body: dict = request.get_json(silent=True)
    map: int = body.get("map", Maps.get_random())
    if not map:
        return formatRes("INVALID_MAP", {})
    mapVerify = Maps.get(map)
    if not mapVerify:
        return formatRes("INVALID_MAP", {})
    party = Parties.create(
        owner=request.user_id,
        private=True,
        map=map,
    )
    return formatRes("CREATED", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })

@route_parties_private.route("/join", methods=["POST"])
@login_required
def join_party():
    body: dict = request.get_json(silent=True)
    party_id: int = body.get("party_id")
    party = Parties.get(party_id)
    if not party:
        return formatRes("NOT_FOUND", {})
    user = Users.get(request.user_id)
    if user["id"] in party["players"]:
        return formatRes("ALREADY_IN_PARTY", {})
    if Parties.is_full(party):
        return formatRes("PARTY_FULL", {})
    party["players"].append(user["id"])
    Parties.save()
    return formatRes("JOINED", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })