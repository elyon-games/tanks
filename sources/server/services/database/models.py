from server.services.database.main import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from common.time import get_current_time
from common.config import getConfig

import random
from server.services.mapGenerator import generate_map
from common.ams import getAllAssetsIn

config = getConfig("server")

class Badges(BaseModel):
    def __init__(self):
        super().__init__({
            "id": {"type": str, "required": True, "unique": True},
            "name": {"type": str, "required": True},
            "description": {"type": str, "required": True}
        }, default_data=[
            {
                "id": "admin",
                "name": "Admin",
                "description": "Administrateur"
            },
            {
                "id": "moderator",
                "name": "Modérateur",
                "description": "Modérateur"
            },
            {
                "id": "developer",
                "name": "Développeur",
                "description": "Développeur"
            },
            {
                "id": "vip",
                "name": "VIP",
                "description": "Joueur VIP"
            }
        ])

class Users(BaseModel):
    def __init__(self):
        super().__init__({
            "id": {"type": int, "required": True, "unique": True},
            "username": {"type": str, "required": True, "unique": True},
            "email": {"type": str, "required": True, "unique": True},
            "password": {"type": str, "required": True},
            "admin": {"type": bool, "required": True, "default": False},
            "money": {"type": int, "default": 0},
            "points": {"type": int, "default": 0},
            "badges": {"type": list, "default": []},
            "created_at": {"type": str, "required": True},
            "stats_kill": {"type": int, "default": 0},
            "stats_death": {"type": int, "default": 0},
            "stats_win": {"type": int, "default": 0},
            "stats_lose": {"type": int, "default": 0}
        }, default_data=[{
            "id": 1,
            "username": "admin",
            "password": generate_password_hash(config["admin"]["password"]),
            "email": config["admin"]["email"],
            "admin": True,
            "badges": [],
            "points": 0,
            "created_at": get_current_time(),
            "money": 0,
            "stats_kill": 0,
            "stats_death": 0,
            "stats_win": 0,
            "stats_lose": 0
        }])

    def create(self, username: str, email: str, password: str, admin: bool = False):
        user = self.insert({
            "id": self.get_new_id(),
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "admin": admin,
            "created_at": get_current_time()
        })
        self.save()
        return user
     
    def existed(self, id):
        return next((user for user in self.data if user["id"] == id or user["email"] == id), None) is not None

    def get_by_email(self, email):
        return next((user for user in self.data if user["email"] == email), None)

    def login(self, email, password):
        user = self.get_by_email(email)
        if user and check_password_hash(user["password"], password):
            return user
        return None

    def update(self, record_id, updates):
        user = self.get(record_id)
        if user:
            user.update(updates)
            self.save()
            return user
        return None

    def delete(self, user_id):
        user = self.get(user_id)
        if user:
            self.data.remove(user)
            self.save()
            return user
        return None
    
    def get_new_id(self):
        return len(self.data) + 1


class Maps(BaseModel):
    def __init__(self):
        default = []
        for map in getAllAssetsIn("maps"):
            map = map.replace("\\", "/").split("/")[-1].split(".")[0]
            default.append({
                "id": len(default) + 1,
                "name": map,
                "description": f"Map {map}",
                "content": generate_map(),
                "background": map
            })
        super().__init__(schema={
            "id": {"type": int, "required": True, "unique": True},
            "name": {"type": str, "required": True},
            "description": {"type": str, "required": True},
            "content": {"type": list, "required": True},
            "background": {"type": str, "default": "sable"},
        }, default_data=default)

    def get_random(self):
        return random.choice(self.data)["id"]

class Parties(BaseModel):
    def __init__(self):
        super().__init__({
            "id": {"type": int, "required": True, "unique": True},
            "owner": {"type": int, "required": True},
            "players_datas": {"type": dict, "default": {}},
            "players": {"type": list, "default": []},
            "max_players": {"type": int, "default": 2},
            "map": {"type": int, "required": True},
            "private": {"type": bool, "default": False},
            "started_at": {"type": str, "default": None},
            "ended_at": {"type": str, "default": None},
            "status": {"type": str, "default": "wait"},
            "created_at": {"type": str, "required": True},
        })

    def create(self, owner: int, private: bool = False, map: int = 0):
        party = self.insert({
            "id": self.get_new_id(),
            "owner": owner,
            "players": [
                owner
            ],
            "private": private,
            "map": map,
            "created_at": get_current_time()
        })
        self.save()
        return party

    def get_by_owner(self, owner):
        return [party for party in self.data if party["owner"] == owner]

    def get_by_player(self, player):
        return [party for party in self.data if player in party["players"]]

    def get_new_id(self):
        return len(self.data) + 1
    
    def get_all_partys_public(self):
        return [{
            "id": party.get("id"),
            "map": party.get("map"),
            "private": party.get("private"),
            "owner": party.get("owner"),
        } for party in self.get_by("private", False) if not self.is_full(party) and party.get("status") == "wait"]

    def find_random_party_public(self):
        parties = self.get_all_partys_public()
        if not parties:
            return None
        return random.choices(parties)
    
    def is_full(self, party):
        return len(party["players"]) >= party["max_players"]
    
    def is_owner(self, party, user):
        return party["owner"] == user["id"]
    
    def finish(self, party):
        party["status"] = "finished"
        party["ended_at"] = get_current_time()
        self.save()
        return party
    
    def is_finished(self, party):
        return party["status"] == "finished"
    
    def is_waiting(self, party):
        return party["status"] == "wait"
    
    def start(self, party):
        party["status"] = "playing"
        party["started_at"] = get_current_time()
        self.save()
        return party
    
    def is_playing(self, party):
        return party["status"] == "playing"
    
    def time_lenght_playing(self, party):
        if party["status"] == "playing":
            return get_current_time() - party["started_at"]
        return 0
    
    def time_party(self, party):
        if party["status"] == "finished":
            return party["ended_at"] - party["started_at"]
        return 0    