import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, inspect
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

class UserBlog(Base):
    __tablename__ = "usersblogs"

    """
    Class that represents the relationship between a User and his Blogs in the database

    Args:
        id (UUID): id of the UserBlog relationship
        blog_id (UUID): Blog related to the User
        user_id (UUID): User who create or share the Blog
        user = information of the user who created or shared the blog
        blog = information of the Blog
    """

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", lazy="joined")
    blog = relationship("Blog", lazy="joined")

    def as_dict(self):
       return {c.key: getattr(self, c.key, None) for c in inspect(self).mapper.column_attrs}