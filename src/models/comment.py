from datetime import datetime
from pydantic import UUID4, BaseModel

from models.user import User

class CommentBase(BaseModel):
    """ Class with base Comment information

    Args:
        blog_id (str): id of the blog
        content (str): session of the database

    """
    content: str
    blog_id: str

class CommentCreate(CommentBase):
    """ Class with necesary information to create a Comment

    Args:
        blog_id (str): id of the blog
        content (str): session of the database

    """
    pass

class Comment(CommentBase):
    """
    Class that represents a Comment in the database

    Args:
        id (UUID): id of the Comment
        content (str): content of the Comment
        blog_id (UUID): the blog where the Comment exist
        user_id (UUID): user who created the Comment
        created_at (datetime): when was the Comment created
        updated_at (datetime): when was the Comment updated
        user (User): information of the user who created the Comment
    """
    id: UUID4
    user_id: UUID4
    user: User
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True