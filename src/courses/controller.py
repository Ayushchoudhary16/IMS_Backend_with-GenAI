from sqlalchemy.orm import Session
from fastapi import HTTPException,Request
from src.courses.model import *
from src.User.model import User
from src.faculty.model import Faculty
from src.courses.dtos import *
from src.batch.model import *

def create_course(db:Session,body:CourseCreate):
    faculty = db.query(Faculty).filter(Faculty.id == body.faculty_id).first()
    if not faculty:
        raise HTTPException(400, "Invalid faculty")

    new_course= Course(
        title=body.title,
        description=body.description,
        faculty_id=body.faculty_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {
        "status":"ok",
        "name":new_course
    }


def get_all_courses(db: Session):
    return db.query(Course).all()


def get_course_by_id(request:Request,db:Session):
    course_id=int(request.query_params.get("course_id"))
    course=db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    return {
        "status":"ok",
        "name":course
    }

def get_course_by_id_p_batch(request:Request,db:Session):
    course_id=int(request.query_params.get("course_id"))
    course=db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    
    batchs=db.query(Batch).filter(Batch.course_id==course_id).all()
    if not batchs:
        raise HTTPException(404, "batchs not found")
    
    return {
        "status":"ok",
        "course_name":course,
        "batchs":batchs
    }


def update_course(request:Request,db:Session,body:CourseCreate):
    course_id=int(request.query_params.get("course_id"))
    course=db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    
    faculty = db.query(Faculty).filter(Faculty.id == body.faculty_id).first()
    if not faculty:
        raise HTTPException(400, "Invalid faculty")
    
    course.title=body.title
    course.description=body.description
    course.faculty_id=body.faculty_id
    db.commit()
    db.refresh(course)
    return {
        "status":"ok",
        "name":course
    }


def delete_course(request:Request,db: Session):
    course_id=int(request.query_params.get("course_id"))
    course=db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    
    db.delete(course)
    db.commit()
    return {
        "message": "Course deleted",
        "course":course
        }