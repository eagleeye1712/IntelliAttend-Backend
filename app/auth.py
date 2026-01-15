from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException

from app.config import SECRET_KEY, ALGORITHM
from app.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(username, role):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def login_user(username, password):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT password, role, full_name FROM users WHERE username=?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if not row or not verify_password(password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "token": create_token(username, row[1]),
        "role": row[1],
        "name": row[2]
    }
