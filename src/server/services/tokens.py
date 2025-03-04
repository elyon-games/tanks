import jwt
from datetime import datetime, timedelta, timezone
from server.services.database.db import users as User
from common.config import getConfig

configData = getConfig("server")

def create_jwt_token(user_id):
    if not configData:
        raise Exception("TOKEN_SERVICE_NO_INIT")
    if not user_id:
        raise Exception("USER_ID_INVALID")
    userData = User.get_by_id(user_id)
    if not userData:
        raise Exception("USER_NOFOUND")
    payload = {
        "user_id": userData.get("id"),
        "admin": userData.get("admin", False),
        "iss": "elyon",
        "exp": datetime.now(timezone.utc) + timedelta(seconds=configData["jwt"]["expiresIn"]),
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, configData["secret"], algorithm="HS256")
    return token

def verify_jwt_token(token):
    try:
        if not configData:
            raise Exception("TOKEN_SERVICE_NO_INIT")
        if not token:
            raise Exception("TOKEN_INVALID")        
        payload = jwt.decode(token, configData["secret"], algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("TOKEN_EXPIRED")
    except jwt.InvalidTokenError:
        raise Exception("TOKEN_INVALID")