from pydantic import BaseModel
from typing import Optional

class FacultyCreateSchema(BaseModel):
    user_id: Optional[int]= None
    department: str
    designation: str

class FacultyUpdateSchema(BaseModel):
    department: Optional[str] = None
    designation: Optional[str] = None