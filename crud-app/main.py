from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from database import engine , SessionLocal , Base
from typing import List
import models , schemas , crud


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/employees' , response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db:Session = Depends(get_db)):
    db_employee = crud.create_employee(db=db , employee=employee)
    return db_employee


@app.get('/employees' , response_model=List[schemas.EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    employees = crud.get_employees(db)
    return employees


@app.get('/employees/{emo_id}' , response_model=schemas.EmployeeOut)
def get_employee(emo_id:int , db:Session = Depends(get_db)):
    db_employee = crud.get_employee(db=db , emp_id=emo_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.put('/employees/{emo_id}' , response_model=schemas.EmployeeOut)
def update_employee(emo_id:int , employee:schemas.EmployeeUpdate, db:Session = Depends(get_db)):
    db_employee = crud.update_employee(db=db , emp_id=emo_id , employee=employee)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee 


@app.delete('/employees/{emo_id}' , response_model=dict)
def delete_employee(emo_id:int , db:Session = Depends(get_db)):
    db_employee = crud.delete_employee(db=db , emp_id=emo_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {'detail' : 'Employee deleted successfully', 'employee_id': emo_id}