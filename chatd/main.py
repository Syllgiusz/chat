from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app import auth, chat, database, models

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

app.include_router(auth.router)
app.include_router(chat.router)

app.mount("/template", StaticFiles(directory="template"), name="template")
templates = Jinja2Templates(directory="template")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
