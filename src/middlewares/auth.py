from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.querys.user import get_user_by_id
from database.utils.utils_db import get_db
from utils.auth_utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from models.user import User

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login/",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        token_data = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(token_data, 'token_datatoken_datatoken_data')
        if datetime.fromtimestamp(token_data.get("exp")) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = get_user_by_id(db, token_data.get("sub"))
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user