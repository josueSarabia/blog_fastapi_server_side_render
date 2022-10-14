from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from database.querys.blog import delete_blog, get_user_blogs
from database.querys.comment import delete_all_user_comments
from middlewares.auth import get_current_user
from models.user import User
from database.database import SessionLocal
from sqlalchemy.orm import Session
from database.querys.user import delete_user, get_user_by_id, get_user_by_email, update_user
from database.utils.utils_db import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
users_router = APIRouter()


@users_router.get('/profile/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_user_profile(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_db = get_user_by_id(db, user.id)
    if user_db is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User does not exists"
        )

    user.id = str(user.id)
    return templates.TemplateResponse("profile.html", {"request": request, "data": user})

@users_router.get('/users/info/', status_code=status.HTTP_200_OK, response_model=User)
async def get_user_info_json(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_db = get_user_by_id(db, user.id)
    if user_db is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User does not exists"
        )

    user.id = str(user.id)
    return user

@users_router.put('/users/', status_code=status.HTTP_200_OK, response_model=User)
async def update_user_info(updated_user: User, user: User = Depends(get_current_user),  db: Session = Depends(get_db)):

    user_db = get_user_by_id(db, updated_user.id)
    if user_db is None:
            raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User does not exists"
        )

    user_db = get_user_by_email(db, updated_user.email)
    if user_db is not None and updated_user.id != user_db.id:
            raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    return update_user(db, updated_user)

@users_router.delete('/users/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(response: Response, user_id: str, user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    user_db = get_user_by_id(db, user_id)
    if user_db is None:
        return
    
    results = get_user_blogs(db, user.id, limit=100000)
    blogs_db = results["results"]

    for blog in blogs_db:
        delete_blog(db, blog_id=str(blog.blog_id), user_id=str(user.id))

    delete_all_user_comments(db, str(user.id))
    
    delete_user(db, user_id)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return

