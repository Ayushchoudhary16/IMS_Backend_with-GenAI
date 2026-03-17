from sqlalchemy import Column, Integer, String ,ForeignKey
from src.utills.db import Base

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    faculty_id = Column(Integer,ForeignKey("faculty.id"),nullable=True)




    # [
    # {
    #     "description": "FastAPI + React",
    #     "id": 1,
    #     "faculty_id": 2,
    #     "title": "Python Full Stack"
    # },
    # {
    #     "description": "AI + GenAI",
    #     "id": 2,
    #     "faculty_id": 6,
    #     "title": "java Full Stack"
    # },