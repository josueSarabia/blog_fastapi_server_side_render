from datetime import datetime
from pydantic import UUID4, BaseModel

from models.user import User

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    id: UUID4

class Blog(BlogBase):
    id: UUID4
    user_id: UUID4
    user: User
    created_at: datetime
    updated_at: datetime

    def reprJSON(self):
        return dict(
            title = self.title,
            content = self.content,
            id = self.id,
            user_id = self.user_id,
            user = self.user,
            created_at = self.created_at,
            updated_at = self.updated_at,
        )

    class Config:
        orm_mode = True