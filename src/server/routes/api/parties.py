from flask import Blueprint, request, session, jsonify
from server.services.database.db import parties as Parties
from server.services.database.db import maps as Maps
from server.services.database.db import users as Users
from server.middleware.auth import login_required
from server.utils import formatRes

route_parties = Blueprint("api-client-parties", __name__)

@route_parties.route("/public", methods=["GET"])
def list_parties():
    parties = Parties.find_random_party_public()
    return formatRes("FOUND", parties)

@route_parties.route("/public/random", methods=["GET"])
def random_party():
    party = Parties.find_random_party_public()
    if not party:
        return formatRes("NOT_FOUND", {})
    return formatRes("FOUND", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })

@route_parties.route("/public/<int:party_id>", methods=["GET"])
def get_party(party_id: int):
    party = Parties.get(party_id)
    if not party:
        return formatRes("NOT_FOUND", {})
    return formatRes("FOUND", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })

@route_parties.route("/private/create", methods=["POST"])
@login_required
def create_party():
    body: dict = request.get_json(silent=True)
    map: int = body.get("map", Maps.get_random())
    user = Users.get(request.user_id)
    party = Parties.create(
        owner=user["id"],
        private=True,
        map=map,
    )
    return formatRes("CREATED", {
        "id": party.get("id"),
        "map": party.get("map")
    })

@route_parties.route("/private/join", methods=["POST"])
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

partiesToClose = [party for party in Parties.get_all() if not party.get("status") == "close"]
for party in partiesToClose:
    party["status"] = "close"
Parties.save()