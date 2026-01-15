import os

SECRET_KEY = os.getenv("INTELLIATTEND_SECRET", "intelliattend-secure-key")
ALGORITHM = "HS256"

QR_VALIDITY_SECONDS = 3
FACE_MATCH_THRESHOLD = 0.6

DB_PATH = "data/attendance.db"
ENCODINGS_PATH = "data/encodings.pkl"
