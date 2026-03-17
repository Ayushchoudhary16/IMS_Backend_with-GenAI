from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session

from src.utills.db import get_db
from src.courses.dtos import *
from src.User.model import *
from src.courses.controller import *
from src.utills.is_authentication import *

courserouter = APIRouter()


@courserouter.post("/create_course",)
def create_course_api(body: CourseCreate,db:Session=Depends(get_db),user:User=Depends(is_admin)):
    return create_course(db, body)


@courserouter.get("/get_all_courses")
def get_courses(db: Session = Depends(get_db)):
    return get_all_courses(db)


@courserouter.get("/get_course_by_id")
def get_course(request:Request, db: Session = Depends(get_db)):
    return get_course_by_id(request,db)

@courserouter.get("/get_course_by_id_p_batch")
def get_course_P_batch(request:Request, db: Session = Depends(get_db)):
    return get_course_by_id_p_batch(request,db)

@courserouter.put("/update_course")
def update_course_api(request:Request,body:CourseCreate,db: Session=Depends(get_db),user=Depends(is_admin)):
    return update_course(request,db, body)


@courserouter.delete("/delete_course")
def delete_course_api(request:Request,db: Session = Depends(get_db),user=Depends(is_admin)):
    return delete_course(request,db)
