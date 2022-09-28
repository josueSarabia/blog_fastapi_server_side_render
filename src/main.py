from fastapi import FastAPI
from routes.comments import comments_router
from database.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(comments_router)