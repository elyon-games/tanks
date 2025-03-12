from server.services.database.main import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from common.time import get_current_time
from common.config import getConfig

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
            "stats_lose": {"type": int, "default": 0},
            "item_buy": {"type": list, "default": []},
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
            "stats_lose": 0,
            "item_buy": []
        }])

    def create(self, username, identifiant, email, password, admin=False):
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