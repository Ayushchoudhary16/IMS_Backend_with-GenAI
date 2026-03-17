from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.faculty.model import *
from src.courses.model import *
from src.students.model import *
from src.User.model import *
from src.enroll.model import Enrollment
from src.students.model import Student
from src.batch.model import Batch
from src.enroll.dtos import *
from src.utills.send_email_students import send_email

async def enroll_student(db: Session, body:EnrollmentCreateSchema):
    student = db.query(Student).filter(Student.id == body.student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    batch = db.query(Batch).filter(Batch.id == body.batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    already_enrolled = db.query(Enrollment).filter(
        Enrollment.student_id == body.student_id,
        Enrollment.batch_id == body.batch_id
    ).first()

    if already_enrolled:
        raise HTTPException(400, "Student already enroll in this batch")

    enrollment = Enrollment(
        student_id=body.student_id,
        batch_id=body.batch_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    # send_email
    student_user = db.query(User).filter(User.id == student.user_id).first()
    course = db.query(Course).filter(Course.id == batch.course_id).first()
    faculty = db.query(Faculty).filter(Faculty.id == course.faculty_id).first()
    faculty_user = db.query(User).filter(User.id == faculty.user_id).first()

    await send_email(
        emails=[student_user.email],
        student_name=student_user.name,
        batch_name=batch.name,
        course_name=course.title,
        faculty_name=faculty_user.name,
        faculty_department=faculty.department,
        faculty_designation=faculty.designation,
        start_date=batch.start_date,
        end_date=batch.end_date
)
    print("sucess")

    return {
        "status": "ok",
        "enrollment": enrollment
    }


def get_all_enrollments(db: Session):
    return db.query(Enrollment).all()


def get_enrollments_by_student(request: Request, db: Session):
    student_id = int(request.query_params.get("student_id"))

    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()

def get_enrollments_by_batch(request: Request, db: Session):
    batch_id = int(request.query_params.get("batch_id"))
    return db.query(Enrollment).filter(
        Enrollment.batch_id == batch_id
    ).all()

def delete_enrollment(request: Request, db: Session):
    enroll_id = int(request.query_params.get("enroll_id"))
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enroll_id
    ).first()
    if not enrollment:
        raise HTTPException(404, "Enrollment not found")
    db.delete(enrollment)
    db.commit()

    return {"message": "Enrollment removed successfully"}




# ayuyadav0307