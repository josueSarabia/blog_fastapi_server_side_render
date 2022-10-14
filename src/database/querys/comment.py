from sqlalchemy.orm import Session
from datetime import datetime
from database.models.user import User

from models.comment import CommentCreate, Comment as CommentSchema
from database.models.comment import Comment as CommentModel


def create_comment(db: Session, comment: CommentCreate, user: User):
    """ Search Blogs in the database (only originals).

    Args:
        db (Session): database session
        title (str): title to search
        dstart (str): start date to filter
        dend(str): end date to filter
        start (int): offset needed for pagination 
        limit (int): size of the page

    Returns:
        dict: a dictionary with the blogs of the user(results) and its total(total)
    """
    created_at = datetime.utcnow().isoformat()
    db_comment = CommentModel(**comment.dict(), user_id=user.id , created_at=created_at, updated_at=created_at)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

def get_comment(db: Session, comment_id: str):
    """ get a Comment

    Args:
        db (Session): database session
        comment_id (str): id of the comment

    Returns:
        comment: the comment information
    """
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    return comment

def update_comment(db: Session, comment: CommentSchema):
    """ update a Comment

    Args:
        db (Session): database session
        comment (Comment): information of the comment

    Returns:
        comment: the updated comment information
    """
    updated_at = datetime.utcnow().isoformat()
    db.query(CommentModel).filter(CommentModel.id == comment.id).update({
        CommentModel.content: comment.content, CommentModel.updated_at: updated_at
    })
    db.commit()

    return comment

def delete_comment(db: Session, comment_id: str):
    """ delete a Comment

    Args:
        db (Session): database session
        comment_id (str): id of the comment

    """
    db.query(CommentModel).filter(CommentModel.id == comment_id).delete()

    db.commit()
    return

def get_blog_comments(db: Session, blog_id: str):
    """ get all Comments of a Blog

    Args:
        db (Session): database session
        blog_id (str): id of the blog

    Returns:
        comments: the comments of the blog
    """
    comments = db.query(CommentModel).filter(CommentModel.blog_id == blog_id).order_by(CommentModel.created_at.asc()).all()
    
    return comments




