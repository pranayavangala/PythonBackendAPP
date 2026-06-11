from sqlalchemy import Column, Integer, String, DECIMAL
from app.database import Base


class User(Base):
    __tablename__ = "users1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))


class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(DECIMAL(10, 2))
    image = Column(String(255))