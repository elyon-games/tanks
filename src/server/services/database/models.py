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
    
    def create(self, id, name, description):
        badge = {
            "id": id,
            "name": name,
            "description": description
        }
        self.insert(badge)
        self.save()
        return badge

class Users(BaseModel):
    def __init__(self):
        super().__init__({
            "id": {"type": int, "required": True, "unique": True},
            "username": {"type": str, "required": True},
            "identifiant": {"type": str, "required": True, "unique": True},
            "email": {"type": str, "required": True, "unique": True},
            "password": {"type": str, "required": True},
            "admin": {"type": bool, "required": True, "default": False},
            "money": {"type": int, "default": 0},
            "badges": {"type": list, "default": []},
            "created_at": {"type": str, "required": True}
        }, default_data=[{
            "id": 1,
            "username": "Admin",
            "identifiant": "admin",
            "password": generate_password_hash(config["admin"]["password"]),
            "email": config["admin"]["email"],
            "admin": True,
            "badges": [],
            "created_at": get_current_time(),
            "money": 0
        }])

    def create(self, username, identifiant, email, password, admin=False):
        user = self.insert({
            "id": self.get_new_id(),
            "username": username,
            "identifiant": identifiant,
            "email": email,
            "password": generate_password_hash(password),
            "admin": admin,
            "created_at": get_current_time()
        })
        self.save()
        return user
    
    def existed(self, id):
        return next((user for user in self.data if user["identifiant"] == id or user["email"] == id), None) is not None

    def login(self, email, password):
        user = self.get_by_email(email)
        if user and check_password_hash(user["password"], password):
            return user
        return None

    def update(self, record_id, updates):
        user = self.get_by_id(record_id)
        if user:
            user.update(updates)
            self.save()
            return user
        return None

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            self.data.remove(user)
            self.save()
            return user
        return None
    
    def get_new_id(self):
        return len(self.data) + 1
    
    def get_by_email(self, email):
        return next((user for user in self.data if user["email"] == email), None)
    
    def get_by_identifiant(self, identifiant):
        return next((user for user in self.data if user["identifiant"] == identifiant), None)
    
    def get_by_username(self, username):
        return next((user for user in self.data if user["username"] == username), None)
    
    def get_by_id(self, user_id):
        return next((user for user in self.data if user["id"] == user_id), None)
