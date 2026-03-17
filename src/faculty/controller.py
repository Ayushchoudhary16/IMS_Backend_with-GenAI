from sqlalchemy.orm import Session
from fastapi import HTTPException,Request
from src.faculty.model import Faculty
from src.User.model import User
from src.faculty.dtos import *

def create_faculty(db:Session,body:FacultyCreateSchema):
    user = db.query(User).filter(User.id == body.user_id,User.role == "faculty").first()
    if not user:
        raise HTTPException(400, "Invalid faculty user")

    faculty=Faculty(
        user_id=body.user_id,
        department=body.department,
        designation=body.designation
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return {
        "status":"ok",
        "name":faculty
    }

def faculty_upsert(request: Request, db: Session, body: FacultyCreateSchema):
    faculty_id = request.query_params.get("faculty_id")

    faculty = None
    if faculty_id:
        faculty = db.query(Faculty).filter(Faculty.id == int(faculty_id)).first()

    # CREATE
    
    if not faculty:
        user = db.query(User).filter(User.id == body.user_id,User.role == "faculty").first()

        if not user:
            raise HTTPException(400, "Invalid faculty user")
        faculty = Faculty(
            id=faculty_id,
            user_id=body.user_id,
            department=body.department,
            designation=body.designation
        )
        db.add(faculty)

    # UPDATE
    else:
        faculty.department = body.department
        faculty.designation = body.designation

    db.commit()
    db.refresh(faculty)

    return {
        "status": "ok",
        "data": faculty
    }



def get_faculties(db: Session):
    return db.query(Faculty).all()


def update_faculty(request:Request,db: Session,body: FacultyUpdateSchema):
    faculty_id=int(request.query_params.get("faculty_id"))
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(404, "Faculty not found")

        
    faculty.department = body.department
    faculty.designation = body.designation

    db.commit()
    db.refresh(faculty)
    return {
        "status":"ok",
        "name":faculty
    }


def delete_faculty(request:Request, db: Session):
    faculty_id=int(request.query_params.get("faculty_id"))
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(404, "Faculty not found")

    db.delete(faculty)
    db.commit()
    return {"message": "Faculty deleted successfully"}


def delete_faculty_by_user_id(request:Request,db: Session):
    user_id=int(request.query_params.get("user_id"))
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "user not found")

    if user.role != "faculty":
        raise HTTPException(400, "Given user is not a faculty")

    db.delete(user)
    db.commit()

    return {
        "message": "Faculty deleted successfully",
        "deleted_user_id": user
    }
