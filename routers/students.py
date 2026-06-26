from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from auth import verify_api_key

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=schemas.StudentResponse, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    if db.query(models.Student).filter(models.Student.email == student.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    new = models.Student(**student.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@router.get("/", response_model=List[schemas.StudentResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.is_active == True).all()

@router.get("/branch/{branch}", response_model=List[schemas.StudentResponse])
def get_by_branch(branch: str, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.branch == branch, models.Student.is_active == True).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found in this branch")
    return students

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_one(student_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Student).filter(models.Student.id == student_id, models.Student.is_active == True).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    return s

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, updated: schemas.StudentUpdate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    s = db.query(models.Student).filter(models.Student.id == student_id, models.Student.is_active == True).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    for k, v in updated.model_dump().items():
        setattr(s, k, v)
    db.commit(); db.refresh(s)
    return s

@router.patch("/{student_id}", response_model=schemas.StudentResponse)
def patch_student(student_id: int, updates: schemas.StudentPatch, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    s = db.query(models.Student).filter(models.Student.id == student_id, models.Student.is_active == True).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    for k, v in updates.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    db.commit(); db.refresh(s)
    return s

@router.delete("/{student_id}")
def soft_delete(student_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    s = db.query(models.Student).filter(models.Student.id == student_id, models.Student.is_active == True).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    s.is_active = False
    db.commit()
    return {"message": "Student deactivated (soft deleted)"}

@router.delete("/{student_id}/hard")
def hard_delete(student_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    s = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    db.delete(s); db.commit()
    return {"message": "Student permanently deleted"}

@router.get("/{student_id}/courses", response_model=List[schemas.EnrollmentResponse])
def get_courses(student_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    return s.enrollments