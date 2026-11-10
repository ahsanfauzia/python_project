import sqlite3, hashlib, secrets
from pathlib import Path
DB = Path(__file__).resolve().parent.parent / "talentlens.db"

def connect():
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; return con

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, salt TEXT NOT NULL, password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS analyses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            role_title TEXT NOT NULL, company TEXT, resume_name TEXT, score INTEGER,
            profile_json TEXT, result_json TEXT, job_description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id))""")

def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 180000).hex()

def register_user(name, email, password):
    salt = secrets.token_hex(16)
    try:
        with connect() as c:
            c.execute("INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
                      (name, email.lower(), salt, _hash(password, salt)))
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

def login_user(email, password):
    with connect() as c:
        row = c.execute("SELECT * FROM users WHERE email=?", (email.lower().strip(),)).fetchone()
    if row and secrets.compare_digest(row["password_hash"], _hash(password, row["salt"])):
        return {"id": row["id"], "name": row["name"], "email": row["email"]}
    return None
