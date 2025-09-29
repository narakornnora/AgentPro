from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=True)
    content = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    likes = Column(String(255), nullable=True)
    comments = Column(String(255), nullable=True)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    bio = Column(String(255), nullable=True)
    followers = Column(String(255), nullable=True)
    following = Column(String(255), nullable=True)

class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    message = Column(String(255), nullable=True)
    timestamp = Column(String(255), nullable=True)

class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String(255), nullable=True)
    receiver_id = Column(String(255), nullable=True)
    content = Column(String(255), nullable=True)
    timestamp = Column(String(255), nullable=True)
