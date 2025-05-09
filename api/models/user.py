from datetime import datetime
import bcrypt
from sqlalchemy.dialects.postgresql import INET, INTEGER, TEXT, TIMESTAMP
from sqlalchemy import Column
from pydantic import BaseModel
from api.db.database import Base


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

# pydantic model, best way to audit the requrest params
class UserIn(BaseModel):    
    username: str
    password: str

class DBUser(Base):
    __tablename__ = "users"
    # that name above has to be correct. thats how we map the DB table to this object
    # the column types below also have to be correct
    id         = Column(INTEGER, default=None, primary_key=True)
    username   = Column(TEXT, unique=True, nullable=False)
    password   = Column(TEXT, nullable=False)
    location   = Column(TEXT, default="Internet")
    ip_addr    = Column(INET)
    created_at = Column(TIMESTAMP, nullable=True, server_default="now()")