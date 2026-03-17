from pydantic import BaseModel
from datetime import date

class BatchCreate(BaseModel):
    name: str
    course_id: int
    batch_fee:int
    start_date: date
    end_date: date