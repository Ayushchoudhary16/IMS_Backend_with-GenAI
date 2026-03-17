from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from src.batch.model import Batch
from src.batch.dtos import *
from src.User.model import User
from src.faculty.model import *
from src.courses.model import Course

def create_batch(db: Session, body: BatchCreate):
    # faculty = db.query(Faculty).filter(Faculty.id == body.faculty_id).first()
    # if not faculty:
    #     raise HTTPException(400,"Faculty with id does not exist")

    # user = db.query(User).filter(User.id == faculty.user_id).first()
    # if not user:
    #     raise HTTPException(400,"User for faculty id  does not exist")

    course = db.query(Course).filter(Course.id == body.course_id).first()
    if not course:
        raise HTTPException(400,"Invalid course")
    
    existing_batch=db.query(Batch).filter(Batch.name == body.name).first()
    if existing_batch:
        raise HTTPException(400,"Batch with name already exists")

    new_batch = Batch(
        name=body.name,
        course_id=body.course_id,
        batch_fee=body.batch_fee,
        start_date=body.start_date,
        end_date=body.end_date
    )

    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    return {
        "status": "ok",
        "batch": new_batch
    }

def get_all_batches(db: Session):
    return db.query(Batch).all()


def get_batch_by_id(request: Request, db: Session):
    batch_id = int(request.query_params.get("batch_id"))

    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    return {
        "status": "ok",
        "batch": batch
    }

def update_batch(request: Request, db: Session, body: BatchCreate):
    batch_id = int(request.query_params.get("batch_id"))

    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    # faculty = db.query(Faculty).filter(Faculty.id == body.faculty_id).first()
    # if not faculty:
    #     raise HTTPException(400, "Faculty does not exist")

    # user = db.query(User).filter(User.id == faculty.user_id,User.role == "faculty").first()
    # if not user:
    #     raise HTTPException(400, "Faculty user does not exist")

    course = db.query(Course).filter(Course.id == body.course_id).first()
    if not course:
        raise HTTPException(400, "Invalid course")

    batch.name = body.name
    batch.course_id = body.course_id
    batch.batch_fee=body.batch_fee
    batch.start_date = body.start_date
    batch.end_date = body.end_date

    db.commit()
    db.refresh(batch)

    return {
        "status": "ok",
        "batch": batch
    }

def delete_batch(request: Request, db: Session):
    batch_id = int(request.query_params.get("batch_id"))

    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(404, "Batch not found")

    db.delete(batch)
    db.commit()

    return {
        "message": "Batch deleted successfully",
        "batch": batch
    }
