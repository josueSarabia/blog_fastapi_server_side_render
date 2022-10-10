from datetime import datetime
from pydantic import UUID4, BaseModel

from models.user import User

class CommentBase(BaseModel):
    content: str
    blog_id: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: UUID4
    user_id: UUID4
    user: User
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True