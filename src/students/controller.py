from fastapi import HTTPException,Request
from sqlalchemy.orm import Session
from src.User.model import User
from src.students.model import Student
from src.students.dtos import *

def create_student(db: Session,body:StudentCreateSchema):
    user = db.query(User).filter(
        User.id == body.user_id,
        User.role == "student"
    ).first()

    if not user:
        raise HTTPException(400, "Invalid student user")

    student = Student(
        user_id=body.user_id,
        mobile=body.mobile,
        gender=body.gender
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "status": "ok",
        "student": student
    }


def get_all_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(request:Request, db: Session):
    student_id = int(request.query_params.get("student_id"))
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    return student


def update_student(request:Request, db: Session, body: StudentUpdateSchema):
    student_id = int(request.query_params.get("student_id"))

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    student.mobile = body.mobile
    student.gender = body.gender

    db.commit()
    db.refresh(student)

    return {
        "status": "ok",
        "student": student
    }


def delete_student(request: Request, db: Session):
    student_id = int(request.query_params.get("student_id"))

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student":student
    }


def delete_student_by_user_id(request: Request, db: Session):
    user_id = int(request.query_params.get("user_id"))

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    if user.role != "student":
        raise HTTPException(400, "Given user is not a student")

    db.delete(user)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "user": user
    }