from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    description: str
    faculty_id: int