from storage import Storage
from uuid import uuid4
import bcrypt

storage = Storage()
# in-memory token store: token -> user_id
TOKENS = {}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password: str, pw_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), pw_hash.encode("utf-8"))

def create_user(name, email, password):
    existing = storage.get_user_by_email(email)
    if existing:
        raise ValueError("email already in use")
    user = {
        "id": str(uuid4()),
        "name": name,
        "email": email,
        "password_hash": hash_password(password)
    }
    return user

def login_user(email, password):
    user = storage.get_user_by_email(email)
    if not user:
        return None, None
    if not check_password(password, user["password_hash"]):
        return None, None
    token = str(uuid4())
    TOKENS[token] = user["id"]
    return token, user

# Decorator for routes
from functools import wraps
from flask import request, jsonify

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error":"authorization required"}), 401
        token = auth.split(" ",1)[1]
        user_id = TOKENS.get(token)
        if not user_id:
            return jsonify({"error":"invalid token"}), 401
        user = storage.get_user(user_id)
        if not user:
            return jsonify({"error":"user not found"}), 401
        # inject current_user
        return f(*args, current_user=user, **kwargs)
    return wrapper
