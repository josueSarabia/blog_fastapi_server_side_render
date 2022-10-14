import email
from uuid import uuid4
from pydantic import BaseModel, UUID4

class UserBase(BaseModel):
    """ Class with base user information

    Args:
        email (str): email of the User
        name (str): name of the User
        last_name (str): last_name of the User
        country (str): country of the User
        age (int): age of the User

    """
    email: str
    name: str
    last_name: str
    country: str
    age: int

class UserCreate(UserBase):
    """ Class with necesary information to create a Blog

    Args:
        email (str): email of the User
        name (str): name of the User
        last_name (str): last_name of the User
        country (str): country of the User
        age (int): age of the User
        password (str): plain password of the User
    """
    password: str

class User(UserBase):
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
    id: UUID4

    def reprJSON(self):
        """ Format the User to a dictionary

        Args:
            id (UUID): id of the User
            email (str): email of the User
            password (str): hashed password of the User
            name (str): name of the User
            last_name (str): last_name of the User
            country (str): country of the User
            age (int): age of the User
        
        Returns:
            dict: dictionary with the user info

        """
        return dict(
            email = self.email,
            name = self.name,
            last_name = self.last_name,
            country = self.country,
            age = self.age,
            id = self.id,
        )
    
    class Config:
        orm_mode = True

class UserLogin():
    """ Class with necesary information to login

    Args:
        email (str): email of the User
        password (str): plain password of the User
    """
    email: str
    password: str
