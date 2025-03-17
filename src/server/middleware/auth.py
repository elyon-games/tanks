from functools import wraps
from flask import request, jsonify, session
from server.services.tokens import verify_jwt_token
from typing import Callable, Any
import time

cache = {}

def login_required(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authentification requise"}), 401
        
        token = auth_header.split(" ")[1]
        current_time = time.time()
        
        if token in cache:
            user_data, timestamp = cache[token]
            if current_time - timestamp < 300:
                request.user_id = user_data.get("user_id")
                request.user_data = user_data
                session["user_id"] = user_data.get("user_id")
                return f(*args, **kwargs)
            else:
                del cache[token]
        
        try:
            user_data = verify_jwt_token(token)
            user_id = user_data.get("user_id")
            request.user_id = user_id
            request.user_data = user_data
            session["user_id"] = user_id
            cache[token] = (user_data, current_time)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        
        return f(*args, **kwargs)
    return decorated_function