import os
import pickle
import face_recognition

from app.config import ENCODINGS_PATH, FACE_MATCH_THRESHOLD

class FaceAI:
    def __init__(self):
        self.encodings = {}
        self.load()

    def load(self):
        if os.path.exists(ENCODINGS_PATH):
            with open(ENCODINGS_PATH, "rb") as f:
                self.encodings = pickle.load(f)

    def save(self):
        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump(self.encodings, f)

    def add_embedding(self, username, rgb_image):
        encodings = face_recognition.face_encodings(rgb_image)
        if len(encodings) != 1:
            return False

        self.encodings.setdefault(username, []).append(encodings[0])
        self.save()
        return True

    def recognize(self, rgb_image):
        encodings = face_recognition.face_encodings(rgb_image)
        if not encodings:
            return None

        face_vec = encodings[0]
        for user, vectors in self.encodings.items():
            for v in vectors:
                dist = ((face_vec - v) ** 2).sum() ** 0.5
                if dist < FACE_MATCH_THRESHOLD:
                    return user
        return None

face_ai = FaceAI()
