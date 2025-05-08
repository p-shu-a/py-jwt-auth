from datetime import datetime
import bcrypt
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy import Column
from pydantic import BaseModel
from typing import Union, Optional

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

class DBUser(SQLModel, table=True):
    __tablename__ = "users"

    # Note on syntax:
    # var id: can either be int or None = default is None
    id: Union[int, None] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    location: Union[str,  None] = "Internet"
    ip_addr: Union[str, None] = Field(
            sa_column=Column(INET, nullable=False)
    )
    #created_at: Union[str, None] = Field(default=None) ### acutally db should manage created_at