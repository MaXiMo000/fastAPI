from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    # password: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase): #response
    id: int
    owner_id: int
    created_at: datetime
    owner: User

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        orm_mode = True

# token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None

# vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore