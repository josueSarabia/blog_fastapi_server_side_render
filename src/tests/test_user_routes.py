from pydantic import UUID4
import pytest
from unittest import mock
from fastapi.testclient import TestClient
from database.utils.utils_db import get_db
from middlewares.auth import  get_current_user
from main import app
from sqlalchemy.orm import Session
from fastapi import status
from dbtest import TestingSessionLocal, Base, engine
from models.user import User

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
    user_base = User(**{
        "email": 'myemail@mine.com',
        "name": "myname",
        "last_name": "mylastname",
        "country": "mycountry",
        "age": 500,
        "id": "5ac05386-7b28-416e-a676-cb7742cdcc98"
    })
    yield lambda: user_base


@pytest.fixture
def client(mock_db, mock_get_current_user):
    app.dependency_overrides[get_db] = mock_db
    app.dependency_overrides[get_current_user] = mock_get_current_user
    return TestClient(app)

testdata_get_user_info = [
    (User(**{
        "email": 'myemail@mine.com',
        "name": "myname",
        "last_name": "mylastname",
        "country": "mycountry",
        "age": 500,
        "id": "5ac05386-7b28-416e-a676-cb7742cdcc98"
    }), status.HTTP_200_OK),
    (None, status.HTTP_400_BAD_REQUEST)
]

@pytest.mark.parametrize("input, expected", testdata_get_user_info)
def test_get_user_info(input, expected, client, monkeypatch):

    fake_user_id = "fake_user_id"

    def mock_get_user_by_id(db: Session, user_id: str):
        return input
    monkeypatch.setattr("routes.users.get_user_by_id", mock_get_user_by_id)

    response = client.get(f"/users/{fake_user_id}/?args=None&kwargs=None")

    assert response.status_code == expected

    if response.status_code == status.HTTP_200_OK:
        input.id = str(input.id)
        assert response.json() == input.dict()

def test_update_user_info_does_not_exist(client, monkeypatch):

    fake_user_info = {
            "email": 'myemail@mine.com',
            "name": "myname",
            "last_name": "mylastname",
            "country": "mycountry",
            "age": 500,
            "id": "5ac05386-7b28-416e-a676-cb7742cdcc98"
        }

    def mock_get_user_by_id(db: Session, user_id: str):
        return None
    monkeypatch.setattr("routes.users.get_user_by_id", mock_get_user_by_id)

    response = client.put(f"/users/?args=None&kwargs=None", json=fake_user_info)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_user_new_email_already_exist(client, monkeypatch):
    fake_user_info = {
            "email": 'myemail@mine.com',
            "name": "myname",
            "last_name": "mylastname",
            "country": "mycountry",
            "age": 500,
            "id": "5ac05386-7b28-416e-a676-cb7742cdcc98"
        }
    fake_user = User(**fake_user_info)

    def mock_get_user_by_id(db: Session, user_id: str):
        return True
    monkeypatch.setattr("routes.users.get_user_by_id", mock_get_user_by_id)

    def mock_get_user_by_email(db: Session, email: str):
        fake_user.id = "notmyid"
        return fake_user
    monkeypatch.setattr("routes.users.get_user_by_email", mock_get_user_by_email)

    response = client.put(f"/users/?args=None&kwargs=None", json=fake_user_info)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_user_info_no_errors(client, monkeypatch):

    fake_user_info = {
            "email": 'myemail@mine.com',
            "name": "myname",
            "last_name": "mylastname",
            "country": "mycountry",
            "age": 500,
            "id": "5ac05386-7b28-416e-a676-cb7742cdcc98"
        }
    fake_user = User(**fake_user_info)

    def mock_get_user_by_id(db: Session, user_id: str):
        return True
    monkeypatch.setattr("routes.users.get_user_by_id", mock_get_user_by_id)

    def mock_get_user_by_email(db: Session, email: str):
        return fake_user
    monkeypatch.setattr("routes.users.get_user_by_email", mock_get_user_by_email)

    def mock_update_user(db: Session, user: User):
        return fake_user
    monkeypatch.setattr("routes.users.update_user", mock_update_user)

    response = client.put(f"/users/?args=None&kwargs=None", json=fake_user_info)

    assert response.status_code == status.HTTP_200_OK
    fake_user.id = str(fake_user.id)
    assert response.json() == fake_user.dict()

def test_delete_user_info(client, monkeypatch):

    fake_user_id = "fake_user_id"

    def mock_get_user_by_id(db: Session, user_id: str):
        return None
    monkeypatch.setattr("routes.users.get_user_by_id", mock_get_user_by_id)

    def mock_delete_user(db: Session, user_id: str):
        return None
    monkeypatch.setattr("routes.users.delete_user", mock_delete_user)

    response = client.delete(f"/users/{fake_user_id}/?args=None&kwargs=None")

    assert response.status_code == status.HTTP_204_NO_CONTENT


