
import json
from fastapi import APIRouter, Depends, HTTPException, Request, status, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.blog import Blog, BlogCreate, BlogUpdate
from database.querys.blog import create_blog, delete_blog, get_all_blogs, get_blog, get_blog_relation, get_user_blogs, share_blog, update_blog
from database.utils.utils_db import get_db
from middlewares.auth import  get_current_user
from models.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.userblog import UserBlog

templates = Jinja2Templates(directory="templates")
blogs_router = APIRouter()


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON() 
        elif type(obj).__name__ == 'UUID':
            return str(obj)
        elif type(obj).__name__ == 'datetime':
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def format_db_blogs(blogs_db):
    blogs = []

    for blog in blogs_db:

        blog.blog_id = str(blog.blog_id)
        blog.user_id = str(blog.user_id)
        blog.id = str(blog.id)
        user_model = User(**blog.user.as_dict()).__dict__
        blog_model = Blog(**blog.blog.as_dict(), user=blog.blog.user.as_dict()).__dict__
        user_blog_model = UserBlog(blog_id=blog.blog_id, user_id=blog.user_id, id=blog.id, user=user_model, blog=blog_model)
        user_blog_json = json.dumps(user_blog_model.reprJSON(), cls=ComplexEncoder)
        blogs.append(json.loads(user_blog_json))
    return blogs

@blogs_router.get("/create-blog/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def get_create_blog_form(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("blogForm.html", {"request": request, "data": {"title": "", "content": "", "type": "create"}})

@blogs_router.post("/blogs/", status_code=status.HTTP_201_CREATED, response_model=Blog)
def create_blog_for_a_user(blog: BlogCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if blog.title.replace(" ", "") == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create a blog without title")

    if blog.content.replace(" ", "") == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create an empty blog")

    new_blog = create_blog(db, blog, user)
    return new_blog

@blogs_router.get("/user/blogs/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def get_user_all_blogs(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    blogs_db = get_user_blogs(db, user.id)
    blogs = format_db_blogs(blogs_db)

    return templates.TemplateResponse("userBlogs.html", {"request": request, "data": {"blogs": blogs }})

@blogs_router.get("/update-blog/{blog_id}/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def get_update_blog_form(blog_id: str, request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    blog_db = get_blog(db, blog_id)

    return templates.TemplateResponse("blogForm.html", {
        "request": request, 
        "data": {
            "title": blog_db.title, 
            "content": blog_db.content,
            "type": "update"
            }
        }
    )

@blogs_router.put("/blogs/", status_code=status.HTTP_200_OK, response_model=Blog)
def update_user_blog(blog: BlogUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if blog.title.replace(" ", "") == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create a blog without title")

    if blog.content.replace(" ", "") == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create an empty blog")

    db_blog = get_blog(db=db, blog_id=blog.id)
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog does not exists")
    
    updated_info = update_blog(db, blog.title, blog.content, blog.id)

    db_blog.title = updated_info["title"]
    db_blog.content = updated_info["content"]
    db_blog.updated_at = updated_info["updated_at"]

    return db_blog

@blogs_router.delete("/blogs/{blog_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_blog(blog_id: str,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    db_blog = get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        pass
    
    delete_blog(db, blog_id, user.id)

    return

@blogs_router.get("/blogs/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def get_all_blogs_of_the_app(request: Request,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    blogs_db = get_all_blogs(db)
    blogs = format_db_blogs(blogs_db)
    return templates.TemplateResponse("blogs.html", {"request": request, "data": {"blogs": blogs }})

@blogs_router.post("/blogs/share/", status_code=status.HTTP_201_CREATED, response_model=Blog)
async def user_share_a_blog(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    body = await request.json()
    blog_id = body["id"]

    db_blog_relation = get_blog_relation(db=db, blog_id=blog_id, user_id=user.id)
    if db_blog_relation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant share a blog more than once")

    db_blog = get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog does not exists")
    
    share_blog(db, blog_id, user.id)
    return db_blog

@blogs_router.get("/blogs/detail/{blog_id}/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def get_detail_of_a_blog(request: Request, blog_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    blog_db = get_blog(db, blog_id)

    return templates.TemplateResponse("blogDetail.html", {"request": request, "data": { "blog": blog_db }})





