from operator import and_
from sqlalchemy.orm import Session
from datetime import datetime
from database.models.user import User

from models.blog import BlogCreate, Blog as BlogSchema
from database.models.blogs import Blog as BlogModel
from database.models.usersblogs import UserBlog as UserBlogModel
from database.models.comment import Comment as CommentModel


def create_blog(db: Session, blog: BlogCreate, user: User):
    created_at = datetime.utcnow().isoformat()
    db_blog = BlogModel(**blog.dict(), user_id=user.id , created_at=created_at, updated_at=created_at)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)

    db_user_blog = UserBlogModel(blog_id=db_blog.id, user_id=user.id)
    db.add(db_user_blog)
    db.commit()
    db.refresh(db_user_blog)

    return db_blog

def get_user_blogs(db: Session, user_id: str):
    user_blogs = db.query(UserBlogModel).filter(UserBlogModel.user_id == user_id).all()
    
    return user_blogs

def get_blog_relation(db: Session, blog_id: str, user_id: str):
    condition = and_(UserBlogModel.blog_id == blog_id, UserBlogModel.user_id == user_id)
    return db.query(UserBlogModel).filter(condition).first()

def get_blog(db: Session, blog_id: str):
    blog_db = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    return blog_db

def update_blog(db: Session, title: str, content: str, blog_id: str):
    db.query(BlogModel).filter(BlogModel.id == blog_id).update({
        BlogModel.title: title, BlogModel.content: content, BlogModel.updated_at: updated_at
    })
    updated_at = datetime.utcnow().isoformat()
    db.commit()

    return {"title": title, "content": content, "updated_at": updated_at}

def delete_blog(db: Session, blog_id: str, user_id: str):
    condition = and_(UserBlogModel.blog_id == blog_id, UserBlogModel.user_id == user_id)
    blog = db.query(UserBlogModel).filter(condition).first()
    blog_user_id = blog.user_id # person who created the blog or person who shared a blog
    blob_blog_user_id = blog.blog.user_id # person who created the blog

    db.query(UserBlogModel).filter(condition).delete()
    db.commit()

    if blog_user_id == blob_blog_user_id:
        db.query(UserBlogModel).filter(UserBlogModel.blog_id == blog_id).delete()
        db.query(CommentModel).filter(CommentModel.blog_id == blog_id).delete()
        db.commit()

        db.query(BlogModel).filter(BlogModel.id == blog_id).delete()
        db.commit()

    return

def get_all_blogs(db: Session):
    user_blogs = db.query(UserBlogModel).all()

    return user_blogs


def share_blog(db: Session, blog_id: str, user_id: str):
    db_user_blog = UserBlogModel(blog_id=blog_id, user_id=user_id)
    db.add(db_user_blog)
    db.commit()
    db.refresh(db_user_blog)

    return db_user_blog





