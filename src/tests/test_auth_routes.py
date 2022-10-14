from typing import Any, Union
import pytest
from unittest import mock
from fastapi.testclient import TestClient
from database.utils.utils_db import get_db
from main import app
from sqlalchemy.orm import Session
from models.user import UserCreate
from database.models.user import User
from fastapi import status
from dbtest import TestingSessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

@pytest.fixture
def mock_db():
    try:
        db = TestingSessionLocal()
        yield mock.MagicMock(db)
    finally:
        db.close() 

@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = mock_db
    return TestClient(app)

def test_sign_in_user(client, monkeypatch):
        user_base = {
            "email": 'myemail@mine.com',
            "name": "myname",
            "last_name": "mylastname",
            "country": "mycountry",
            "age": 500,
            "password": "mysecurepass",
        }
        user_result = user_base.copy()
        user_result["id"] = "5ac05386-7b28-416e-a676-cb7742cdcc98"
        del user_result['password']

        def mocked_get_user_by_email_response(db: Session, user_email: str):
            return None
        
        def mocked_create_user_response(db: Session, user: UserCreate):
            return user_result
        
        monkeypatch.setattr("routes.auth.get_user_by_email", mocked_get_user_by_email_response)
        monkeypatch.setattr("routes.auth.create_user", mocked_create_user_response)

        response = client.post(f"/signup/?args=None&kwargs=None", json=user_base)

        assert response.status_code == status.HTTP_201_CREATED

        assert response.json() == user_result

def test_login(client, monkeypatch):
    user_login = {
        "username": 'myemail@mine.com',
        "email": 'myemail@mine.com',
        "password": "mysecurepass",
    }

    user_db = User(**{
        "id": "5ac05386-7b28-416e-a676-cb7742cdcc98",
        "email": 'myemail@mine.com',
        "password": "mysecurepass",
        "name": "myname",
        "last_name": "mylastname",
        "country": "mycountry",
        "age": 500,
    })
    fake_token = "myfaketoken"
    fake_refresh_token = "myfakerefreshtoken"

    def mocked_get_user_by_email_response(db: Session, user_email: str):
        return user_db
    monkeypatch.setattr("routes.auth.get_user_by_email", mocked_get_user_by_email_response)

    def mocked_verify_password_response(password: str, hashed_pass: str):
        return True
    monkeypatch.setattr("routes.auth.verify_password", mocked_verify_password_response)

    def mocked_create_access_token_response(subject: Union[str, Any], expires_delta: int = None):
        return fake_token
    monkeypatch.setattr("routes.auth.create_access_token", mocked_create_access_token_response)

    def mocked_create_refresh_token_response(subject: Union[str, Any], expires_delta: int = None):
        return fake_refresh_token
    monkeypatch.setattr("routes.auth.create_refresh_token", mocked_create_refresh_token_response)


    response = client.post(f"/login/?args=None&kwargs=None", data=user_login)

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == None
