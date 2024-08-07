from sqlalchemy import Column, Integer, String,ARRAY,JSON
from schemas.userSchema import Userr
# from models.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    interests = Column(JSON(String))
