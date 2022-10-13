import email
from uuid import uuid4
from pydantic import BaseModel, UUID4

class UserBase(BaseModel):
    email: str
    name: str
    last_name: str
    country: str
    age: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID4

    def reprJSON(self):
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
    email: str
    password: str
