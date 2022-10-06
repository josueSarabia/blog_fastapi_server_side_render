from fastapi import FastAPI
from routes.comments import comments_router
from routes.auth import auth_router
from routes.users import users_router
from database.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(comments_router)
app.include_router(auth_router)
app.include_router(users_router)