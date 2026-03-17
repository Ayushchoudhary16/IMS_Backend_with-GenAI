from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.utills.db import get_db
from src.batch.dtos import *
from src.User.model import User
from src.batch.controller import *
from src.utills.is_authentication import *

batchrouter = APIRouter()

@batchrouter.post("/create_batch")
def create_batch_api(body: BatchCreate,db: Session = Depends(get_db),user: User = Depends(is_admin)):
    return create_batch(db, body)


@batchrouter.get("/get_all_batches")
def get_batches(db: Session = Depends(get_db)):
    return get_all_batches(db)

@batchrouter.get("/get_batch_by_id")
def get_batch(request: Request,db: Session = Depends(get_db)):
    return get_batch_by_id(request, db)


@batchrouter.put("/update_batch")
def update_batch_api(request: Request,body: BatchCreate,db: Session = Depends(get_db),user: User = Depends(is_admin)):
    return update_batch(request, db, body)


@batchrouter.delete("/delete_batch")
def delete_batch_api(request: Request,db: Session = Depends(get_db),user: User = Depends(is_admin)):
    return delete_batch(request, db)
