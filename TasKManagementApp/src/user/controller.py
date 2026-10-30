from src.user.dtos import UserSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException,status
from pwdlib import PasswordHash

password_hash=PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def register(body:UserSchema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username already exists")
    is_user=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exists")

    hash_password=get_password_hash(body.password)

    new_user=UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user