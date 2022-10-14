from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from utils.auth_utils import get_hashed_password
from models.user import UserCreate, User as UserSchema
from database.models.user import User as UserModel


def create_user(db: Session, user: UserCreate):
    """ Create a user in the database

    Args:
        db (Session): database session
        user (UserCreate): information of the user

    Returns:
        user: the created user in the database
    """
    user.password = get_hashed_password(user.password)
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_id(db: Session, user_id: str):
    """ Get a user by his id

    Args:
        db (Session): database session
        user_id (str): id of the user

    Returns:
        user: the user with the specified id
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user

def get_user_by_email(db: Session, user_email: str):
    """ Get a user by his email

    Args:
        db (Session): database session
        user_email (str): email of the user

    Returns:
        user: the user with the specified email
    """
    if user_email is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Missing email"
        )

    user = db.query(UserModel).filter(UserModel.email == user_email).first()
    return user

def update_user(db: Session, user: UserSchema):
    """ Update the user information

    Args:
        db (Session): database session
        user (UserSchema): updated user info

    Returns:
        user: the user with the updated info
    """
    missing_fields = "Missing values: "
    error = False
    if user.name is None:
        missing_fields += 'name '
        error = True
    
    if  user.last_name is None:
        missing_fields += 'last_name '
        error = True
    
    if user.country is None:
        missing_fields += 'country '
        error = True
    
    if user.age is None:
        missing_fields += 'age '
        error = True
    
    if user.email is None:
        missing_fields += 'email '
        error = True
    
    if error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=missing_fields
        )


    db.query(UserModel).filter(UserModel.id == user.id).update({
        UserModel.name: user.name,
        UserModel.last_name: user.last_name,
        UserModel.country: user.country,
        UserModel.age: user.age,
        UserModel.email: user.email
    })
    db.commit()

    return user

def delete_user(db: Session, user_id: str):
    """ Delete the user from the database

    Args:
        db (Session): database session
        user_id (str): id of the user

    """
    db.query(UserModel).filter(UserModel.id == user_id).delete()
    db.commit()

    return



