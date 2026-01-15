from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    username: str
    password: str

class StudentRegister(BaseModel):
    username: str
    name: str
    course: str

class FaceRegisterLive(BaseModel):
    frames: List[str]

class ScanRequest(BaseModel):
    image: str
    qr_token: str
