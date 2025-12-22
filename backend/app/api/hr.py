from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.hr import Employee, Department
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/hr", tags=["hr"])

class DepartmentCreate(BaseModel):
    code: str
    name: str

class DepartmentOut(BaseModel):
    id: uuid.UUID
    code: str
    name: str

    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    employee_code: str
    full_name: str
    email: str
    phone: str
    department_id: uuid.UUID
    job_title: str
    base_salary: float
    joined_date: datetime

class EmployeeOut(BaseModel):
    id: uuid.UUID
    employee_code: str
    full_name: str
    email: str
    department_id: uuid.UUID
    job_title: str
    base_salary: float

    class Config:
        from_attributes = True

@router.get("/departments", response_model=List[DepartmentOut])
async def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.post("/departments", response_model=DepartmentOut)
async def create_department(dept_in: DepartmentCreate, db: Session = Depends(get_db)):
    workspace_id = uuid.uuid4() # Mock
    db_dept = Department(**dept_in.dict(), workspace_id=workspace_id)
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.get("/employees", response_model=List[EmployeeOut])
async def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.post("/employees", response_model=EmployeeOut)
async def create_employee(emp_in: EmployeeCreate, db: Session = Depends(get_db)):
    workspace_id = uuid.uuid4() # Mock
    db_emp = Employee(**emp_in.dict(), workspace_id=workspace_id)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp
