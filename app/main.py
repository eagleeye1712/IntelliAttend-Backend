from fastapi import FastAPI, Depends, HTTPException
import base64, cv2, numpy as np

from app.database import init_db, get_db
from app.models import *
from app.auth import login_user
from app.dependencies import get_current_user
from app.qr import generate_qr, validate_qr
from app.face_ai import face_ai
from app.attendance import mark_attendance

app = FastAPI(title="IntelliAttend Backend")
init_db()

@app.post("/login")
def login(data: LoginRequest):
    return login_user(data.username, data.password)

@app.post("/register-student")
def register_student(data: StudentRegister, user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM courses WHERE name=?", (data.course,))
    course = cur.fetchone()
    if not course:
        raise HTTPException(400, "Invalid course")

    cur.execute(
        "INSERT OR IGNORE INTO students(username, name, course_id) VALUES (?, ?, ?)",
        (data.username, data.name, course[0])
    )
    conn.commit()
    conn.close()
    return {"status": "registered"}

@app.post("/register-face-live")
def register_face_live(data: FaceRegisterLive, user=Depends(get_current_user)):
    added = 0
    for frame in data.frames:
        img = base64.b64decode(frame.split(",")[1])
        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if face_ai.add_embedding(user["sub"], rgb):
            added += 1

    if added < 3:
        raise HTTPException(400, "Not enough live face samples")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET face_registered=1 WHERE username=?",
        (user["sub"],)
    )
    conn.commit()
    conn.close()

    return {"status": "face_registered"}

@app.get("/qr")
def get_qr(user=Depends(get_current_user)):
    if user["role"] != "teacher":
        raise HTTPException(403, "Only teacher allowed")
    return {"token": generate_qr()}

@app.post("/scan")
def scan(data: ScanRequest, user=Depends(get_current_user)):
    if not validate_qr(data.qr_token):
        raise HTTPException(403, "QR expired")

    img = base64.b64decode(data.image.split(",")[1])
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    username = face_ai.recognize(rgb)
    if not username:
        return {"status": "unknown"}

    return {
        "status": mark_attendance(username),
        "username": username
    }
