from fastapi import APIRouter

comments_router = APIRouter()


@comments_router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]