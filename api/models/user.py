from datetime import datetime
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy import Column, Integer, String, DateTime
from api.db.database import Base
from pydantic import BaseModel
import bcrypt

class RegisterUser:
    def __init__(self, username, password, location, ip_addr):
        self.username = username
        self.password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt(10))
        self.location = location
        self.ip_addr  = ip_addr
        self.created_at = datetime.now()
    
    def __repr__(self):
        return str({
            "username": self.username,
            "password": self.password,
            "location": self.location,
            "ip_addr" : self.ip_addr
        })

class UserIn(BaseModel):    
    username: str
    password: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String)
    ip_addr = Column(INET)
    created_at = Column(DateTime)

# THIS FILE LOOKS LIKE A CLUSTERFUCK FEELS.