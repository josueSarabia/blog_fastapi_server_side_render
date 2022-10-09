from fastapi import APIRouter, Cookie, status, HTTPException, Depends, Request, Response
from fastapi.responses import RedirectResponse
from database.querys.user import get_user_by_email, create_user
from models.user import UserCreate, User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth_utils import create_access_token, create_refresh_token, verify_password
from database.utils.utils_db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
auth_router = APIRouter()

@auth_router.get("/signup/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def login_page(request: Request, access_token: str | None = Cookie(default=None)):
    if access_token is not None:
        return RedirectResponse('/profile/', status_code=303)
    return templates.TemplateResponse("signup.html", {"request": request})

@auth_router.post('/signup/', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user_account(response: Response, user: UserCreate,  db: Session = Depends(get_db)):

    user_db = get_user_by_email(db, user.email)
    if user_db is not None:
            raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    new_user = create_user(db, user)

    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)

    response.set_cookie( key="access_token", value=access_token, httponly=True )
    response.set_cookie( key="refresh_token", value=refresh_token, httponly=True )

    return new_user

@auth_router.get("/login/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def login_page(request: Request, access_token: str | None = Cookie(default=None)):
    if access_token is not None:
        return RedirectResponse('/profile/', status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post('/login/', status_code=status.HTTP_200_OK)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
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
    access_token = create_access_token(user_db.id)
    refresh_token = create_refresh_token(user_db.id)

    response.set_cookie( key="access_token", value=access_token, httponly=True )
    response.set_cookie( key="refresh_token", value=refresh_token, httponly=True )
    return


@auth_router.post('/logout/', status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return