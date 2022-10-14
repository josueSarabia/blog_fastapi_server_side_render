from sqlalchemy import Column, Integer, String, inspect
from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    """
    Class that represents a User in the database

    Args:
        id (UUID): id of the User
        email (str): email of the User
        password (str): hashed password of the User
        name (str): name of the User
        last_name (str): last_name of the User
        country (str): country of the User
        age (int): age of the User
    """

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def as_dict(self):
        """
        Format a User to a dictionary

        Returns:
            dict: dictionary that contains the User informarion
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
