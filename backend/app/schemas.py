from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    username: str
    password: str

class RandomNumber(BaseModel):
    timestamp: datetime
    number: float

    class Config:
        orm_mode = True
