from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_message(db: Session, message: schemas.MessageCreate, user_id: int):
    db_message = models.Message(content=message.content, room_id=message.room_id, user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message_with_user(db: Session, message_id: int):
    return (
        db.query(models.Message, models.User)
        .join(models.User, models.User.id == models.Message.user_id)
        .filter(models.Message.id == message_id)
        .first()
    )
