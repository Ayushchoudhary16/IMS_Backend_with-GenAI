from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt

from src.User.model import User
from src.User.dtos import UserCreate,loginUserSchema,UpdateUserSchema
from src.utills.db import get_db
from src.utills.helper import *

def create_user(body:UserCreate,db:Session):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    h_pass=get_password_hash(body.password)
    new_user = User(
        name=body.name,
        email=body.email,
        password=h_pass,
        role=body.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "data":new_user,"status":"User register sucessfully."
    }

def loginUser(body:loginUserSchema,db:Session):
    user=db.query(User).filter(User.email == body.email).first()
    if not user:
        raise HTTPException(404,detail={"message":"user is not exits"})
    
    password=verify_password(body.password,user.password)
    if not password:
        raise HTTPException(404,detail={"message":"password is incorrect"})
    
    expire=datetime.now(timezone.utc)+timedelta(minutes=20)
    token=jwt.encode({"user_id": user.id,"name":user.name,"exp":expire},SECRET_KEY,algorithm=ALGORITHM)

    return {"status":"okk","token":token}



def get_admin_by_login(db:Session,userr:User):
    user=userr
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin access"
        )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_all_users(db: Session):
    users = db.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return {
        "status": "ok",
        "total_users": len(users),
        "users": users
    }

def delete_admin_account(db:Session,userr:User):
    user=userr
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="only admin can acces")
    db.delete(user)
    db.commit()
    return{
        "status":"delete Admin account",
        "return":user
    }

def update_admin_data(body:UpdateUserSchema,db:Session,userr:User):
    user=userr
    # if user.role != "admin":
    #     raise HTTPException(status_code=403, detail="only admin can acces")
    user.name=body.name,
    user.email=body.email

    db.commit()
    db.refresh(user)
    return{
        "status":"ok",
        "name":user
    }





