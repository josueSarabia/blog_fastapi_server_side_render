from datetime import datetime
import uuid
from sqlalchemy.orm import validates
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    blog_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    @validates('content')
    def validate_content(self, key, content) -> str:
        if content.replace(" ", "") == "" :
            raise ValueError('content cant be empty')

        if len(content) > 200:
            raise ValueError('content is too long. max 200 chars.')
        return content