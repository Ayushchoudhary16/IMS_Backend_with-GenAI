from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.User.controller import *
from src.User.dtos import *
from src.User.model import User
from src.utills.db import get_db
from src.utills.is_authentication import *


userrouter = APIRouter()


@userrouter.post("/user_register")
def create_user_api(body:UserCreate,db:Session=Depends(get_db)):
    return create_user(body,db)

@userrouter.post("/loginUser")
def user_login(body:loginUserSchema,db:Session=Depends(get_db)):
    return loginUser(body,db)

@userrouter.get("/getUser")
def get_user(db: Session=Depends(get_db),user:User=Depends(is_admin)):
    return get_admin_by_login(db,user)

@userrouter.get("/get_all_users")
def get_all_users_api(db: Session = Depends(get_db)):
    return get_all_users(db)

@userrouter.delete("/deleteUser")
def delete_user(db:Session=Depends(get_db),user:User=Depends(is_admin)):
    return delete_admin_account(db,user)

@userrouter.put("/updateUser")
def update_user(body:UpdateUserSchema,db:Session=Depends(get_db),user:User=Depends(is_student_or_admin)):
    return update_admin_data(body,db,user)