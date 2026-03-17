from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.utills.db import get_db
from src.students.dtos import *
from src.students.controller import *
from src.utills.is_authentication import *

studentrouter = APIRouter()

@studentrouter.post("/create_student")
def create_student_api(body: StudentCreateSchema, db: Session = Depends(get_db), user=Depends(is_student_or_admin)):
    return create_student(db, body)

@studentrouter.get("/get_all_students")
def get_students(db: Session = Depends(get_db)):
    return get_all_students(db)

@studentrouter.get("/get_student_by_id")
def get_student(request: Request, db: Session = Depends(get_db)):
    return get_student_by_id(request, db)

@studentrouter.put("/update_student")
def update_student_api(request: Request, body: StudentUpdateSchema, db: Session = Depends(get_db), user=Depends(is_student_or_admin)):
    return update_student(request,db,body)

@studentrouter.delete("/delete_student")
def delete_student_api(request: Request, db: Session = Depends(get_db), user=Depends(is_student_or_admin)):
    return delete_student(request, db)

@studentrouter.delete("/delete-by-user")
def delete_student_by_user_id_api(request: Request,db: Session = Depends(get_db),user=Depends(is_student_or_admin)):
    return delete_student_by_user_id(request, db)