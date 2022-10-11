
from fastapi import APIRouter, Depends, HTTPException, Request, status, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.comment import Comment, CommentCreate
from database.querys.comment import create_comment, get_blog, update_comment, get_comment, delete_comment, get_blog_comments
from database.utils.utils_db import get_db
from middlewares.auth import  get_current_user
from models.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
comments_router = APIRouter()

# se debe eliminar? ---> este seria el blog detail
@comments_router.get("/comment-test/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def comment_test(request: Request):
    return templates.TemplateResponse("comment.html", {"request": request})

# se debe eliminar
@comments_router.get("/blogs/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def blogs_test(request: Request):
    return templates.TemplateResponse("blogs.html", {"request": request})


@comments_router.get("/blogs/{blog_id}/comments/", status_code=status.HTTP_200_OK)
def get_all_comments(blog_id: str,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    db_blog = get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog does not exists")
    
    comments = get_blog_comments(db, blog_id)

    return comments

@comments_router.post("/comments/", status_code=status.HTTP_201_CREATED, response_model=Comment)
def create_comment_for_blog(comment: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if comment.content.replace(" ", "") == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create an empty comment")
    
    if len(comment.content) > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cant be more than 200 chars")

    db_blog = get_blog(db=db, blog_id=comment.blog_id)
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog does not exists")

    new_comment = create_comment(db, comment, user)
    return new_comment


@comments_router.put("/comments/", status_code=status.HTTP_200_OK, response_model=Comment)
def update_comment_for_blog(comment: Comment, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if comment.content.replace(" ", "") == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create an empty comment")
    
    if len(comment.content) > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cant be more than 200 chars")

    db_comment = get_comment(db=db, comment_id=comment.id)
    if db_comment.user_id != comment.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User cant edit this comment")

    db_blog = get_blog(db=db, blog_id=comment.blog_id)
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog does not exists")
    

    return update_comment(db, comment)


@comments_router.delete("/comments/{comment_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment_for_blog(comment_id: str,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    db_comment = get_comment(db=db, comment_id=comment_id)
    if db_comment is None:
        pass

    delete_comment(db, comment_id)

    return
