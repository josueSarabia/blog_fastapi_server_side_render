from pydantic import UUID4, BaseModel

from models.user import User
from models.blog import Blog

class UserBlogBase(BaseModel):
    """ Class with base UserBlog relatioship information

    Args:
        user_id (UUID4): id of the user
        blog_id (UUID4): id of the Blog

    """
    user_id: UUID4
    blog_id: UUID4

class UserBlogCreate(UserBlogBase):
    """ Class with necesary information to create a UserBlog relatioship

    Args:
        user_id (UUID4): id of the user
        blog_id (UUID4): id of the Blog

    """
    pass

class UserBlog(UserBlogBase):
    """
    Class that represents the relationship between a User and his Blogs in the database

    Args:
        id (UUID): id of the UserBlog relationship
        blog_id (UUID): Blog related to the User
        user_id (UUID): User who create or share the Blog
        user (User): information of the user who created or shared the blog
        blog (Blog): information of the Blog
    """
    id: UUID4
    user: User
    blog: Blog

    def reprJSON(self):
        """ Format the UserBlog relationship to a dictionary

        Args:
            id (UUID): id of the UserBlog relationship
            blog_id (UUID): Blog related to the User
            user_id (UUID): User who create or share the Blog
            user (User): information of the user who created or shared the blog
            blog (Blog): information of the Blog
        
        Returns:
            dict: dictionary with the userblog info

        """
        return dict(
            user_id = self.user_id,
            blog_id = self.blog_id,
            id = self.id,
            user = self.user,
            blog = self.blog,
        )

    class Config:
        orm_mode = True