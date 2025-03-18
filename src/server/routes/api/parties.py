from flask import Blueprint, request, session, jsonify
from server.services.database.db import parties as Parties
from server.services.database.db import maps as Maps
from server.services.database.db import users as Users
from server.middleware.auth import login_required
from server.utils import formatRes

route_parties = Blueprint("api-client-parties", __name__)

@route_parties.route("/public", methods=["GET"])
def list_parties():
    parties = [{
        "id": party.get("id"),
        "map": party.get("map"),
        "private": party.get("private"),
        "owner": party.get("owner"),
    } for party in Parties.get_all() if not party.get("private") and not Parties.is_full(party) and party.get("status") == "wait"]
    return formatRes("FOUND", parties)

@route_parties.route("/create", methods=["POST"])
@login_required
def create_party():
    body: dict = request.get_json(silent=True)
    private: bool = body.get("private", False)
    map: int = body.get("map", Maps.get_random())
    user = Users.get(request.user_id)
    party = Parties.create(
        owner=user["id"],
        private=private,
        map=map,
    )
    return formatRes("CREATED", {
        "id": party.get("id"),
        "map": party.get("map"),
        "private": party.get("private"),
    })

partiesToClose = [party for party in Parties.get_all() if not party.get("status") == "close"]
for party in partiesToClose:
    party["status"] = "close"
Parties.save()