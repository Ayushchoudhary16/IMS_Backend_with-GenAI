from fastapi import Request,HTTPException,Depends,status
import jwt
from sqlalchemy.orm import Session

from src.utills.db import get_db
from src.utills.helper import *
from src.User.model import User

def is_authenticated(req:Request,db:Session=Depends(get_db)):
    try:
        token=req.headers.get("Authorization")
        if not token:
            raise HTTPException(401,detail={"Error":"User unauthorized 1"})
        
        token=token.split(" ")[-1]
        print(token)
        data=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        if not data:
            raise HTTPException(401,detail={"Error":"User unauthorized 2"})
        
        user_id=data.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail={"Error":"User unauthorized 3"})
        print(user_id)
        user = db.query(User).filter(User.id == user_id).first()
        print(user)
        if not user:
            raise HTTPException(status_code=401, detail={"Error":"User unauthorized 4"})

        return user
    except:
        raise HTTPException(401,detail={"Error":"user unotherized 5"})

def is_admin(user: User = Depends(is_authenticated)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin access"
        )
    return user

def is_faculty_or_admin(user: User = Depends(is_authenticated)):
    if user.role not in ["faculty", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only faculty or admin access"
        )
    return user


def is_student_or_admin(user: User = Depends(is_authenticated)):
    if user.role not in ["student", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only student or admin access"
        )
    return user

















