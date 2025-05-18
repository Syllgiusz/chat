from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import database
from .models import User
from passlib.hash import bcrypt

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    db: Session = next(get_db())
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return JSONResponse({"status": "error", "message": "Użytkownik już istnieje"})
    hashed_password = bcrypt.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return JSONResponse({"status": "ok", "message": "Zarejestrowano pomyślnie"})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not username or not password:
        return JSONResponse({"status": "error", "message": "Login i hasło są wymagane"})
    db: Session = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        return JSONResponse({"status": "error", "message": "Nieprawidłowe dane logowania"})
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    return JSONResponse({"status": "ok", "message": "Zalogowano pomyślnie"})

@router.get("/me")
async def me(request: Request):
    username = request.session.get("username")
    if username:
        return JSONResponse({"username": username})
    return JSONResponse(status_code=404, content={"message": "Nie zalogowano"})

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return JSONResponse({"status": "ok", "message": "Wylogowano"})
