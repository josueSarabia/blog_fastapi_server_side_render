from fastapi import FastAPI, Request, Cookie, status
from models.exception import RequiresLoginException
from routes.comments import comments_router
from routes.auth import auth_router
from routes.users import users_router
from routes.blogs import blogs_router
from database.database import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(comments_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(blogs_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", status_code=status.HTTP_200_OK)
def login_page(access_token: str | None = Cookie(default=None)):
    if access_token is None:
        return RedirectResponse('/login/', status_code=303)
    else:
        return RedirectResponse('/profile/', status_code=303)

@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    response = RedirectResponse(url='/login/')
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
