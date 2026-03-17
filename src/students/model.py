from sqlalchemy import Column, Integer, String, ForeignKey
from src.utills.db import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=True)