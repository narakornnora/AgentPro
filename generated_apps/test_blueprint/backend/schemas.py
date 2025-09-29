from pydantic import BaseModel
from typing import Optional

class PostsIn(BaseModel):
    user_id: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    likes: Optional[str] = None
    comments: Optional[str] = None

class PostsOut(PostsIn):
    id: int

class UsersIn(BaseModel):
    username: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    followers: Optional[str] = None
    following: Optional[str] = None

class UsersOut(UsersIn):
    id: int

class NotificationsIn(BaseModel):
    user_id: Optional[str] = None
    type: Optional[str] = None
    message: Optional[str] = None
    timestamp: Optional[str] = None

class NotificationsOut(NotificationsIn):
    id: int

class MessagesIn(BaseModel):
    sender_id: Optional[str] = None
    receiver_id: Optional[str] = None
    content: Optional[str] = None
    timestamp: Optional[str] = None

class MessagesOut(MessagesIn):
    id: int
