from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine

db_URL="postgresql://postgres:Ayushsql@localhost:5433/institutemanagementsystem"

Base=declarative_base()

db_init=create_engine(db_URL)

local_Session=sessionmaker(bind=db_init)

def get_db():
    db=local_Session()
    try:
        yield db
    finally:
        db.close()
