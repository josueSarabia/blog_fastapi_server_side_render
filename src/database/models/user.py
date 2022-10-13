from sqlalchemy import Column, Integer, String, inspect
from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def as_dict(self):
       return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
