from flask import Blueprint, request
from server.services.database.db import parties as Parties
from server.services.database.db import maps as Maps
from server.utils import formatRes
from server.middleware.auth import login_required

route_parties_public = Blueprint("api-parties-public", __name__)

# Créer une partie publique
@route_parties_public.route("/create", methods=["POST"])
@login_required
def create_party():
    body: dict = request.get_json(silent=True)
    map: int = body.get("map", Maps.get_random())
    if not map:
        return formatRes("INVALID_MAP", {})
    party = Parties.create(
        owner=request.user_id,
        private=False,
        map=map,
    )
    return formatRes("CREATED", {
        "id": party.get("id"),
        "map": party.get("map")
    })

# renvoie les 3 dernières parties publiques à afficher sur la page d'accueil
@route_parties_public.route("/", methods=["GET"])
def list_parties():
    parties = Parties.get_all_partys_public()
    parties = sorted(parties, key=lambda x: x.get("created_at"))[:3]
    if not parties:
        return formatRes("NOT_FOUND", {})
    return formatRes("FOUND", parties)

# Récupère une partie publique aléatoire
@route_parties_public.route("/random", methods=["GET"])
def random_party():
    party = Parties.find_random_party_public()
    if not party:
        return formatRes("NOT_FOUND", {})
    return formatRes("FOUND", {
        "id": party.get("id"),
        "map": party.get("map"),
        "owner": party.get("owner"),
    })