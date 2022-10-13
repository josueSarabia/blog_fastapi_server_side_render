from pydantic import UUID4, BaseModel

from models.user import User
from models.blog import Blog

class UserBlogBase(BaseModel):
    user_id: UUID4
    blog_id: UUID4

class UserBlogCreate(UserBlogBase):
    pass

class UserBlog(UserBlogBase):
    id: UUID4
    user: User
    blog: Blog

    def reprJSON(self):
        return dict(
            user_id = self.user_id,
            blog_id = self.blog_id,
            id = self.id,
            user = self.user,
            blog = self.blog,
        )

    class Config:
        orm_mode = True