from fastapi import APIRouter, Depends, Request ,status
from src.utils.db import get_db
from src.user import controller
from src.user.dtos import LoginSchema, UserSchema,UserResponseSchema
from sqlalchemy.orm import Session

user_routes=APIRouter(
    prefix="/user")

@user_routes.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register_user(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)

@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login_user(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

@user_routes.get("/is_authenticated",status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
def is_authenticated(request:Request,db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db)