from fastapi import HTTPException,FastAPI,Depends,Request
from src.utills.db import db_init,Base
from src.User.router import userrouter
from src.courses.router import courserouter
from src.faculty.router import facultyrouter
from src.batch.router import batchrouter
from src.students.router import studentrouter
from src.enroll.router import enrollrouter
from src.genAI.router import genairouter
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(db_init)

app=FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userrouter,prefix="/users",tags=["Users"])
app.include_router(courserouter,prefix="/courses",tags=["Courses"])
app.include_router(facultyrouter,prefix="/faculties",tags=["faculties"])
app.include_router(batchrouter,prefix="/batchs",tags=["batchs"])
app.include_router(studentrouter,prefix="/students",tags=["students"])
app.include_router(enrollrouter,prefix="/enrolls",tags=["enrolls"])
app.include_router(genairouter,prefix="/genAi",tags=["genAI"])


@app.get("/")
def read_root():
    return {"message": "Institute Management System API is running"}






