from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from src.utills.db import get_db
from src.faculty.dtos import *
from src.faculty.controller import *
from src.utills.is_authentication import *

facultyrouter = APIRouter()

@facultyrouter.post("/create_faculty")
def create_faculty_api(body: FacultyCreateSchema,db: Session = Depends(get_db),user=Depends(is_admin)):
    return create_faculty(db, body)

@facultyrouter.post("/upsert_faculty")
def upsert_faculty_api(request:Request,body: FacultyCreateSchema,db: Session = Depends(get_db)):
    return faculty_upsert(request,db, body)


@facultyrouter.get("/get_all_faculty")
def get_all_faculty(db: Session = Depends(get_db)):
    return get_faculties(db)

@facultyrouter.put("/update_faculty_data")
def update_faculty_api(request:Request,body: FacultyUpdateSchema,db: Session = Depends(get_db),user=Depends(is_faculty_or_admin)):
    return update_faculty(request,db,body)


@facultyrouter.delete("/delete_faculty")
def delete_faculty_api(request:Request,db: Session = Depends(get_db),user=Depends(is_admin)):
    return delete_faculty(request, db)

@facultyrouter.delete("/delete_user_faculty")
def delete_userfaculty_api(request:Request,db: Session = Depends(get_db),user = Depends(is_admin)):
    return delete_faculty_by_user_id(request,db)