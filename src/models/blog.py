from datetime import datetime
from pydantic import UUID4, BaseModel

from models.user import User

class BlogBase(BaseModel):
    """ Class with base blog information

    Args:
        title (str): title of the Blog
        content (str): content of the Blog

    """
    title: str
    content: str

class BlogCreate(BlogBase):
    """ Class with necesary information to create a Blog

    Args:
        title (str): title of the Blog
        content (str): content of the Blog

    """
    pass

class BlogUpdate(BlogBase):
    """ Class with necesary information to update a Blog

    Args:
        id (UUID): id of the Blog
        title (str): title of the Blog
        content (str): content of the Blog

    """
    id: UUID4

class Blog(BlogBase):
    """ Class that represents a Blog

    Args:
        id (UUID): id of the Blog
        title (str): title of the Blog
        content (str): content of the Blog
        user_id (UUID): user who created the Blog
        created_at (datetime): when was the Blog created
        updated_at (datetime): when was the Blog updated
        user (User): information of the user who created the blog

    """
    id: UUID4
    user_id: UUID4
    user: User
    created_at: datetime
    updated_at: datetime

    def reprJSON(self):
        """ Format the Blog to a dictionary

        Args:
            id (UUID): id of the Blog
            title (str): title of the Blog
            content (str): content of the Blog
            user_id (UUID): user who created the Blog
            created_at (datetime): when was the Blog created
            updated_at (datetime): when was the Blog updated
            user (User): information of the user who created the blog
        
        Returns:
            dict: dictionary with the blog info

        """
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