from src.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException,status
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime,timedelta
import jwt


password_hash=PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

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



def login_user(body:LoginSchema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")

    if not verify_password(body.password,is_user.hash_password):    
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid password")

    exp_time=datetime.now()+timedelta(minutes=settings.EXP_TIME)
    print(exp_time)
    token=jwt.encode({"_id":is_user.id,"exp":exp_time},settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return {"token":token,"user":{"id":is_user.id,"name":is_user.name,"username":is_user.username,"email":is_user.email}}