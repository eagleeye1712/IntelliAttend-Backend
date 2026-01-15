import time
import hashlib
from app.config import SECRET_KEY, QR_VALIDITY_SECONDS

def generate_qr():
    step = int(time.time() / QR_VALIDITY_SECONDS)
    return hashlib.sha256(
        f"{SECRET_KEY}-{step}".encode()
    ).hexdigest()[:12]

def validate_qr(token):
    step = int(time.time() / QR_VALIDITY_SECONDS)
    valid = [
        hashlib.sha256(f"{SECRET_KEY}-{step}".encode()).hexdigest()[:12],
        hashlib.sha256(f"{SECRET_KEY}-{step-1}".encode()).hexdigest()[:12]
    ]
    return token in valid
