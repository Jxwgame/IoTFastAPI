from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Students).all()

@router_v1.get('/students/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Students).filter(models.Students.id == student_id).first()

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    new_stu = models.Students(id=student['id'], name=student['name'], surname=student['surname'], date=student['date'], sex=student['sex'])
    db.add(new_stu)
    db.commit()
    db.refresh(new_stu)
    response.status_code = 201
    return new_stu

@router_v1.patch('/students/{student_id}')
async def update_book(student_id: int, student : dict,db: Session = Depends(get_db)):
    db_item = db.query(models.Students).filter(models.Students.id == student_id).first()
    if not db_item:
        return {'message' : 'Not found'}
    db_item.name = student['name']
    db_item.surname = student['surname']
    db_item.date = student['date']
    db_item.sex = student['sex']

    db.commit()
    db.refresh(db_item)
    return {'message' : 'Update success'}


@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Students).filter(models.Students.id == student_id).first()
    if not db_item:
        return {'message' : 'Not found'}
    db.delete(db_item)
    db.commit()
    return {'Delete Success' : True}

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
