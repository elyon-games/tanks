from flask import Blueprint, request, jsonify
from server.services.database.db import parties as Parties
from server.services.database.db import maps as Maps
from server.services.database.db import users as Users
from common.time import get_current_time
from server.middleware.auth import login_required
from server.services.network.main import create_gateway
from server.utils import formatRes, formatErrorRes

route_parties = Blueprint("api-parties", __name__)

@route_parties.route("/info/<int:party_id>", methods=["GET"])
@login_required
def get_party(party_id: int):
    party = Parties.get(party_id)
    if not party:
        return formatErrorRes("NOT_FOUND", {})
    if request.user_id not in party.get("players", []):
        return formatErrorRes("NOT_AUTHORIZED", {})
    return formatRes("FOUND", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })


@route_parties.route("/create", methods=["POST"])
@login_required
def create_party():
    body: dict = request.get_json(silent=True)
    if not body:
        return formatErrorRes("INVALID_BODY", {})
    map: int = body.get("map", Maps.get_random())
    if not map:
        return formatErrorRes("INVALID_MAP", {})
    mapVerify = Maps.get(map)
    if not mapVerify:
        return formatErrorRes("INVALID_MAP", {})
    party = Parties.create(
        owner=request.user_id,
        private=True,
        map=map,
    )
    return formatRes("CREATED", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner")
    })

@route_parties.route("/join", methods=["POST"])
@login_required
def join_party():
    body: dict = request.get_json(silent=True)
    if not body:
        return formatErrorRes("INVALID_BODY", {})
    private = body.get("private", False)
    party = None
    if private:
        party_id: int = body.get("party_id")
        if not party_id:
            return formatErrorRes("MISSING_PARTY_ID", {})
        party = Parties.get(party_id)
        if not party:
            return formatErrorRes("NOT_FOUND", {})
    else:
        party = Parties.find_random_party_public()
        if not party:
            party = Parties.create(
                owner=request.user_id,
                private=False,
                map=Maps.get_random(),
            )
            Parties.save()
    if not party:
        return formatRes("ERROR_FOR_FOUND", {})
            
    if Parties.is_player_in_party(party, request.user_id):
        return formatErrorRes("ALREADY_JOINED", {})
    if Parties.is_full(party):
        return formatErrorRes("FULL", {})
    gateway = create_gateway(request.user_id)
    gateway.add_group(f"party-{party.get('id')}")
    party["players"].append(request.user_id)

    Parties.save()
    return formatRes("JOINED", {
        "gateway_id": gateway.id,
        "gateway_key": gateway.SECRET_KEY,
        "party_id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
        "private": party.get("private"),
        "players": party.get("players"),
    })

# renvoie les 3 dernières parties publiques à afficher sur la page d'accueil
@route_parties.route("/public", methods=["GET"])
def list_parties():
    parties = Parties.get_all_parties_public()
    parties = sorted(parties, key=lambda x: x.get("created_at"))[:3]
    if not parties:
        return formatRes("NOT_FOUND", [])
    return formatRes("FOUND", parties)

partiesToClose = [
    party for party in Parties.get_all() if not party.get("status") == "finish" and party.get("ended_at") is None]
for party in partiesToClose:
    party["ended_at"] = get_current_time()
    party["status"] = "close"
Parties.save()