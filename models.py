from sqlalchemy import Column, Integer, String,Float,DateTime
import datetime
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

class Listings(Base):
    __tablename__ = "listings"
    id = Column(Integer,primary_key=True,index=True)
    product_title =Column(String)
    price =Column(float)
    description = Column(String)
    image = Column(String)
    category = Column(String)
    createdDate = Column(DateTime,default=datetime.datetime.utcom)