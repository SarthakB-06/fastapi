from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from models import Employee
from typing import List

employee_db: List[Employee] = [] 




class User(BaseModel):
    id:int
    name:str


app = FastAPI()

@app.get('/employees' , response_model=List[Employee])
def get_employees():
    return employee_db


@app.get('/employees/{employee_id}' , response_model=Employee)
def get_employee(employee_id:int):
    for index ,employee in enumerate(employee_db):
        if employee.id == employee_id:
            return employee_db[index]
    raise HTTPException(status_code=404,detail='Employee not found')


@app.post('/employees')
def add_employee(new_emp: Employee):
    for emp in employee_db:
        if emp.id == new_emp.id:
            raise HTTPException(status_code=400 , detail='Employee already exists')
    employee_db.append(new_emp)
    return new_emp


@app.put('/update_employee/{emp_id}' , response_model=Employee)
def update_employee(emp_id:int , updated_emp:Employee):
    for i, emp in enumerate(employee_db):
        if emp.id == emp_id:
            employee_db[i] = updated_emp
            return updated_emp
    raise HTTPException(status_code=404, detail='Employee not found')


@app.delete('/delete_employee/{emp_id}')
def delete_employee(emp_id:int):
    for i,emp in enumerate(employee_db):
        if emp.id == emp_id:
            del employee_db[i]
            return {'message' : 'Employee deleted successfully'}
    raise HTTPException(status_code=404, detail='Employee not found')