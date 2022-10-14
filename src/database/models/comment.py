from datetime import datetime
import uuid
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

class Comment(Base):
    __tablename__ = "comments"

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

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    blog_id = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", lazy="joined")

    @validates('content')
    def validate_content(self, key, content) -> str:
        if content.replace(" ", "") == "" :
            raise ValueError('content cant be empty')

        if len(content) > 200:
            raise ValueError('content is too long. max 200 chars.')
        return content