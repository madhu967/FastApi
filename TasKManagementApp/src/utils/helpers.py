from fastapi import HTTPException,status,Request,Depends
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db
from src.utils.settings import settings
from sqlalchemy.orm import Session
from src.user.models import UserModel
from datetime import datetime,timedelta

import jwt

def is_authenticated(request:Request,db:Session = Depends(get_db)):
    try:
            token=request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token missing")
            
            token=token.split(" ")[1]
        
            data=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
            user_id=data.get("_id")
            exp_time=int(data.get("exp"))
        
            current_time=datetime.now().timestamp()
            print(exp_time-current_time)
            if current_time>exp_time:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token expired")
        
            is_user=db.query(UserModel).filter(UserModel.id==user_id).first()
            if not is_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        
            
            return is_user
    except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")