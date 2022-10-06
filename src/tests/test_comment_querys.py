import pytest
from database.querys.comment import create_comment, delete_comment, get_comment, update_comment
# from unittest import mock
from fastapi import HTTPException, status
from dbtest import TestingSessionLocal, Base, engine
from models.comment import CommentCreate


Base.metadata.create_all(bind=engine)

@pytest.fixture
def dbtest():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def test_create_comment_in_db(dbtest):
    comment_create = CommentCreate(**{
        "content": "regular comment",
        "blog_id": "fake_blog_id",
        "user_id": "fake_uder_id"
    })

    comment_result = create_comment(dbtest, comment_create)

    comment_db = get_comment(dbtest, comment_result.id)

    delete_comment(dbtest, comment_db.id)

    assert comment_db is not None and comment_db.user_id == comment_create.user_id


def test_update_user_in_db(dbtest):
    comment_create = CommentCreate(**{
        "content": "regular comment",
        "blog_id": "fake_blog_id",
        "user_id": "fake_uder_id"
    })

    comment_result = create_comment(dbtest, comment_create)

    update_comment(dbtest, comment_result)
    
    comment_db = get_comment(dbtest, comment_result.id)
    delete_comment(dbtest, comment_db.id)
    assert comment_db is not None and comment_db.user_id == comment_create.user_id

        
    
    
