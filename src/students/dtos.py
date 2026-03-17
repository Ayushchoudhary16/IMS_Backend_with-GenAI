from pydantic import BaseModel
from typing import Optional

class StudentCreateSchema(BaseModel):
    user_id: int
    mobile: str
    gender: Optional[str] = None


class StudentUpdateSchema(BaseModel):
    mobile: Optional[str] = None
    gender: Optional[str] = None