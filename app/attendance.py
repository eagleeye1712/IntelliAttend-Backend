from datetime import datetime
from app.database import get_db

def mark_attendance(username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, course_id FROM students WHERE username=?",
        (username,)
    )
    row = cur.fetchone()
    if not row:
        return "not_registered"

    student_id, course_id = row
    today = datetime.now().strftime("%Y-%m-%d")

    cur.execute(
        "SELECT * FROM attendance WHERE student_id=? AND date=?",
        (student_id, today)
    )
    if cur.fetchone():
        conn.close()
        return "already_marked"

    cur.execute(
        "INSERT INTO attendance(student_id, course_id, date, time) VALUES (?, ?, ?, ?)",
        (student_id, course_id, today,
         datetime.now().strftime("%H:%M:%S"))
    )

    conn.commit()
    conn.close()
    return "marked"
