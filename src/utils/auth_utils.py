from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 86400  # 24 horas
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str):
    """ hashed a plain text(password)

    Args:
        password (str): plain text password
    
    Returns:
        dict: a hashed password

    """
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str):
    """ vaerify a plain text(password) against a hashed string(password)

    Args:
        password (str): plain text password
        hashed_pass (str): hashed password
    
    Returns:
        bool: True if it matchs, False if not.

    """
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], expires_delta: int = None):
    """ create an jwt access token for a user

    Args:
        subject (str): content of the token
        expires_delta (str): expiration time
    
    Returns:
        jwt: encoded jwt

    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None):
    """ create an jwt refresh token for a user

    Args:
        subject (str): content of the token
        expires_delta (str): expiration time
    
    Returns:
        jwt: encoded jwt

    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt