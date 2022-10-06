from datetime import datetime
from pydantic import UUID4, BaseModel

class CommentBase(BaseModel):
    content: str
    blog_id: str
    user_id: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True