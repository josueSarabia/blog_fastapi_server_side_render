from fastapi import APIRouter, status, HTTPException, Depends
from database.querys.user import get_user_by_email, create_user
from models.user import UserCreate, User
from database.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth_utils import create_access_token, create_refresh_token, verify_password
from database.utils.utils_db import get_db


auth_router = APIRouter()


@auth_router.post('/signup/', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user_account(user: UserCreate,  db: Session = Depends(get_db)):

    user_db = get_user_by_email(db, user.email)
    if user_db is not None:
            raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    return create_user(db, user)

@auth_router.post('/login/', status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    user_db = get_user_by_email(db, form_data.username)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user_db.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user_db.id),
        "refresh_token": create_refresh_token(user_db.id),
    }