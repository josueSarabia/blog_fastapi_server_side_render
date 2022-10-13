from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, DateTime, inspect
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", lazy="joined")

    def as_dict(self):
       return {c.key: getattr(self, c.key, None) for c in inspect(self).mapper.column_attrs}