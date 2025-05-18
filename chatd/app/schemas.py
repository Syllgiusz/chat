from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RoomCreate(BaseModel):
    name: str

class MessageCreate(BaseModel):
    content: str
    room_id: int

class MessageOut(BaseModel):
    content: str
    timestamp: datetime
    user_id: int
    room_id: int
