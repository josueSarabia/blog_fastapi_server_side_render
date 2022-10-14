from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, DateTime, inspect
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

class Blog(Base):
    __tablename__ = "blogs"

    """
    Class that represents a Blog in the database

    Args:
        id (UUID): id of the Blog
        title (str): title of the Blog
        content (str): content of the Blog
        user_id (UUID): user who created the Blog
        created_at (datetime): when was the Blog created
        updated_at (datetime): when was the Blog updated
        user (User): information of the user who created the blog
    """

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", lazy="joined")

    def as_dict(self):
        """
        Format a Blog to a dictionary

        Returns:
            dict: dictionary that contains the Blog informarion
        """
        return {c.key: getattr(self, c.key, None) for c in inspect(self).mapper.column_attrs}