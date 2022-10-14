import pytest
from unittest import mock
from fastapi.testclient import TestClient
from database.utils.utils_db import get_db
from middlewares.auth import  get_current_user
from main import app
from sqlalchemy.orm import Session
from fastapi import status
from dbtest import TestingSessionLocal, Base, engine
from datetime import datetime
from models.comment import Comment

Base.metadata.create_all(bind=engine)

@pytest.fixture
def mock_db():
    try:
        db = TestingSessionLocal()
        yield mock.MagicMock(db)
    finally:
        db.close()

@pytest.fixture
def mock_get_current_user():
    user_base = {
        "email": 'myemail@mine.com',
        "name": "myname",
        "last_name": "mylastname",
        "country": "mycountry",
        "age": 500,
        "id": "5ac05386-7b28-416e-a676-cb7742cdcc98"
    }
    yield lambda: user_base


@pytest.fixture
def client(mock_db, mock_get_current_user):
    app.dependency_overrides[get_db] = mock_db
    app.dependency_overrides[get_current_user] = mock_get_current_user
    return TestClient(app)

def test_get_all_comments(client, monkeypatch):
    fake_blog_id = "fake_blog_id"

    def mock_get_blog(db: Session, blog_id: str):
        return True
    monkeypatch.setattr("routes.comments.get_blog", mock_get_blog)

    def mock_get_blog_comments(db: Session, blog_id: str):
        return []
    monkeypatch.setattr("routes.comments.get_blog_comments", mock_get_blog_comments)
    
    response = client.get(f"/blogs/{fake_blog_id}/comments/?args=None&kwargs=None")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == []

testdata_post = [
    ("regular comment", status.HTTP_201_CREATED), 
    ("", status.HTTP_400_BAD_REQUEST), 
    ("long comment long comment long commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong\
    commentlong commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong commentlong \
    comment", status.HTTP_400_BAD_REQUEST)
]
@pytest.mark.parametrize("test_input,expected", testdata_post)
def test_create_comment_for_blog(test_input, expected, client, monkeypatch):
    fake_comment_base = {
        "content": test_input,
        "blog_id": "fake_blog_id",
        "user_id": "fake_uder_id"
    }

    fake_comment = fake_comment_base.copy()
    fake_comment["id"] = "5ac05386-7b28-416e-a676-cb7742cdcc98"
    fake_comment["created_at"] = datetime.utcnow().isoformat()
    fake_comment["updated_at"] = datetime.utcnow().isoformat()

    def mock_get_blog(db: Session, blog_id: str):
        return True
    monkeypatch.setattr("routes.comments.get_blog", mock_get_blog)

    def mock_create_comment(db: Session, blog_id: str):
        return fake_comment
    monkeypatch.setattr("routes.comments.create_comment", mock_create_comment)

    response = client.post(f"/comments/?args=None&kwargs=None", json=fake_comment_base)

    assert response.status_code == expected

    if expected == status.HTTP_201_CREATED:
        fake_comment["id"] = str(fake_comment["id"])
        assert response.json() == fake_comment

testdata_put = [
    ("regular comment", status.HTTP_200_OK), 
    ("", status.HTTP_400_BAD_REQUEST), 
    ("long comment long comment long commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong\
    commentlong commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong commentlong commentlong \
    commentlong commentlong commentlong commentlong commentlong \
    comment", status.HTTP_400_BAD_REQUEST)
]
@pytest.mark.parametrize("test_input,expected", testdata_put)
def test_update_comment_for_blog(test_input, expected,client, monkeypatch):
    fake_comment = {
        "id": "5ac05386-7b28-416e-a676-cb7742cdcc98",
        "content": test_input,
        "blog_id": "fake_blog_id",
        "user_id": "fake_uder_id",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    def mock_get_comment(db: Session, comment_id: str):
        return Comment(**fake_comment)
    monkeypatch.setattr("routes.comments.get_comment", mock_get_comment)

    def mock_get_blog(db: Session, blog_id: str):
        return True
    monkeypatch.setattr("routes.comments.get_blog", mock_get_blog)

    def mock_update_comment(db: Session, comment: Comment):
        return fake_comment
    monkeypatch.setattr("routes.comments.update_comment", mock_update_comment)

    response = client.put(f"/comments/?args=None&kwargs=None", json=fake_comment)
    assert response.status_code == expected

    if expected == status.HTTP_201_CREATED:
        assert response.json() == fake_comment

def test_delete_comment_for_blog(client, monkeypatch):

    fake_comment_id = "fake_comment_id"

    def mock_get_comment(db: Session, comment_id: str):
        return None
    monkeypatch.setattr("routes.comments.get_comment", mock_get_comment)

    def mock_delete_comment(db: Session, comment_id: str):
        return None
    monkeypatch.setattr("routes.comments.delete_comment", mock_delete_comment)

    response = client.delete(f"/comments/{fake_comment_id}/?args=None&kwargs=None")

    assert response.status_code == status.HTTP_204_NO_CONTENT
