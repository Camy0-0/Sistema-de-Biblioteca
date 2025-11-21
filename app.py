from flask import Flask, request, jsonify
from auth import auth_required, login_user, create_user, get_user_by_token
from storage import Storage
import uuid

app = Flask(__name__)
storage = Storage()

@app.route("/api/users", methods=["POST"])
def api_create_user():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "name, email and password required"}), 400
    try:
        user = create_user(name=name, email=email, password=password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    storage.save_user(user)
    user_resp = {k:v for k,v in user.items() if k != "password_hash"}
    return jsonify(user_resp), 201

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error":"email and password required"}), 400
    token, user = login_user(email, password)
    if not token:
        return jsonify({"error":"invalid credentials"}), 401
    return jsonify({"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}), 200

@app.route("/api/books", methods=["GET"])
def api_list_books():
    q = request.args.get("q")
    books = storage.list_books()
    if q:
        q_lower = q.lower()
        books = [b for b in books if q_lower in b.get("title","").lower() or q_lower in b.get("author","").lower()]
    return jsonify(books), 200

@app.route("/api/books/<book_id>", methods=["GET"])
def api_get_book(book_id):
    book = storage.get_book(book_id)
    if not book:
        return jsonify({"error":"book not found"}), 404
    return jsonify(book), 200

@app.route("/api/books/<book_id>/reserve", methods=["POST"])
@auth_required
def api_reserve_book(book_id, current_user):
    book = storage.get_book(book_id)
    if not book:
        return jsonify({"error":"book not found"}), 404
    if book.get("status") == "reserved":
        return jsonify({"error":"book already reserved"}), 400
    book["status"] = "reserved"
    book["reserved_by"] = current_user["id"]
    book["reserved_at"] = storage.now_iso()
    storage.save_book(book)
    return jsonify(book), 200

@app.route("/api/books/<book_id>/return", methods=["POST"])
@auth_required
def api_return_book(book_id, current_user):
    book = storage.get_book(book_id)
    if not book:
        return jsonify({"error":"book not found"}), 404
    if book.get("status") != "reserved" or book.get("reserved_by") != current_user["id"]:
        return jsonify({"error":"book not reserved by user"}), 400
    book["status"] = "available"
    book["reserved_by"] = None
    book["reserved_at"] = None
    storage.save_book(book)
    return jsonify(book), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
