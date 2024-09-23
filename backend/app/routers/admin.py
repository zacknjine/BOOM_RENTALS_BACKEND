from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.auth import get_current_user
from typing import List
from app.schemas.message import MessageResponse, MessageReply
from app.schemas.property import PropertyCreate, Property  
from app.crud import get_messages_for_admin, reply_to_message
from app import crud

router = APIRouter()

def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.post("/properties/", response_model=Property)
def add_property(
    property: PropertyCreate,  
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    return crud.create_property(db, property.name, property.location, property.number_of_houses, property.description)

@router.get("/properties/", response_model=list[Property])
def get_all_properties(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    return crud.get_properties(db)

@router.get("/messages/", response_model=list[MessageResponse])
def get_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    return get_messages_for_admin(db)

@router.put("/messages/{message_id}/reply", response_model=MessageResponse)
def admin_reply(
    message_id: int,
    reply: MessageReply,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    db_message = reply_to_message(db, message_id, reply)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@router.post("/register-user", response_model=UserSchema)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    
    hashed_password = User.hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[UserSchema])
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    users = db.query(User).all()
    return users

@router.delete("/delete-user/{user_id}", response_model=UserSchema)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user

@router.put("/update-user/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    
    for key, value in user_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
