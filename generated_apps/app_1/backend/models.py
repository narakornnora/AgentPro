from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Coffee(Base):
    __tablename__ = "coffees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    price = Column(Float, nullable=True)
    category = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    coffee_ids = Column(String(255), nullable=True)
    total_price = Column(Float, nullable=True)
    status = Column(String(255), nullable=True)

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    coordinates = Column(String(255), nullable=True)

