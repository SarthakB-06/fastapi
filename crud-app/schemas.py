from pydantic import BaseModel , EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    name : str
    email : EmailStr

class EmployeeCreate(EmployeeBase):
    email: Optional[EmailStr]  

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id : int

    class Config:
        orm_mode = True 