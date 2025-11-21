import json, os
from datetime import datetime
from uuid import uuid4

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")

class Storage:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE,"w") as f:
                json.dump([], f)
        if not os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE,"w") as f:
                json.dump([], f)

    def _read(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Users
    def list_users(self):
        return self._read(USERS_FILE)

    def save_user(self, user):
        users = self.list_users()
        users.append(user)
        self._write(USERS_FILE, users)

    def get_user_by_email(self, email):
        for u in self.list_users():
            if u.get("email") == email:
                return u
        return None

    def get_user(self, user_id):
        for u in self.list_users():
            if u.get("id") == user_id:
                return u
        return None

    # Books
    def list_books(self):
        return self._read(BOOKS_FILE)

    def get_book(self, book_id):
        for b in self.list_books():
            if b.get("id") == book_id:
                return b
        return None

    def save_book(self, book):
        books = self.list_books()
        for i, b in enumerate(books):
            if b["id"] == book["id"]:
                books[i] = book
                self._write(BOOKS_FILE, books)
                return
        books.append(book)
        self._write(BOOKS_FILE, books)

    # helper
    def now_iso(self):
        return datetime.utcnow().isoformat() + "Z"

    def create_sample_books(self):
        books = [
            {"id": str(uuid4()), "title":"Dom Casmurro", "author":"Machado de Assis", "status":"available", "reserved_by": None, "reserved_at": None},
            {"id": str(uuid4()), "title":"O Alquimista", "author":"Paulo Coelho", "status":"available", "reserved_by": None, "reserved_at": None}
        ]
        self._write(BOOKS_FILE, books)
