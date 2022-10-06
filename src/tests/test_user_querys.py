import pytest
# from unittest import mock
from database.querys.user import create_user, delete_user, get_user_by_id, update_user
from fastapi import HTTPException
from dbtest import TestingSessionLocal, Base, engine
from models.user import UserCreate


Base.metadata.create_all(bind=engine)

@pytest.fixture
def dbtest():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def test_create_user_in_db(dbtest):
    user_create = UserCreate(**{
            "email": 'myemail@mine.com',
            "name": "myname",
            "last_name": "mylastname",
            "country": "mycountry",
            "age": 500,
            "password": "mysecurepass",
        })

    user_result = create_user(dbtest, user_create)

    user_db = get_user_by_id(dbtest, user_result.id)

    delete_user(dbtest, user_db.id)

    assert user_db is not None and user_db.email == user_create.email

testdata_put = [
    ("empty", "email"), 
    ("empty", "name"), 
    ("empty", "last_name"),
    ("empty", "country"),
    ("empty", "age"),
    ("", "good result")
]
@pytest.mark.parametrize("input,input_value", testdata_put)
def test_update_user_in_db(input, input_value, dbtest):
    try:
        user_create = UserCreate(**{
            "email": 'myemail2@mine.com' + input_value,
            "name": "myname",
            "last_name": "mylastname",
            "country": "mycountry",
            "age": 500,
            "password": "mysecurepass",
        })
        user_result = create_user(dbtest, user_create)

        if input == "empty":
            user_result.__setattr__(input_value, None)
        update_user(dbtest, user_result)
        
        user_db = get_user_by_id(dbtest, user_result.id)
        assert user_db is not None and user_db.email == user_create.email
    except HTTPException:
        print('missing values')
    finally:
        user_db = get_user_by_id(dbtest, user_result.id)
        delete_user(dbtest, user_db.id)
    
    

    