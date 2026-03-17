from sqlalchemy import Column, Integer, String, ForeignKey
from src.utills.db import Base

class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    # id = Column(Integer,unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    department = Column(String, nullable=False)
    designation = Column(String, nullable=False)