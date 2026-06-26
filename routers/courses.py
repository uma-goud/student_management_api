from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from auth import verify_api_key

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=schemas.CourseResponse, status_code=201)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    if db.query(models.Course).filter(models.Course.code == course.code).first():
        raise HTTPException(status_code=400, detail="Course code already exists")
    new = models.Course(**course.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@router.get("/", response_model=List[schemas.CourseResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_one(course_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not c: raise HTTPException(status_code=404, detail="Course not found")
    return c

@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, updated: schemas.CourseUpdate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    c = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not c: raise HTTPException(status_code=404, detail="Course not found")
    for k, v in updated.model_dump().items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    c = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not c: raise HTTPException(status_code=404, detail="Course not found")
    db.delete(c); db.commit()
    return {"message": "Course deleted"}

@router.post("/{course_id}/enroll/{student_id}", response_model=schemas.EnrollmentResponse, status_code=201)
def enroll(course_id: int, student_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    s = db.query(models.Student).filter(models.Student.id == student_id, models.Student.is_active == True).first()
    if not s: raise HTTPException(status_code=404, detail="Student not found")
    c = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not c: raise HTTPException(status_code=404, detail="Course not found")
    if db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id, models.Enrollment.course_id == course_id).first():
        raise HTTPException(status_code=400, detail="Already enrolled")
    e = models.Enrollment(student_id=student_id, course_id=course_id)
    db.add(e); db.commit(); db.refresh(e)
    return e

@router.patch("/enrollment/{enrollment_id}/grade", response_model=schemas.EnrollmentResponse)
def update_grade(enrollment_id: int, grade_data: schemas.GradeUpdate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    e = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not e: raise HTTPException(status_code=404, detail="Enrollment not found")
    e.grade = grade_data.grade
    db.commit(); db.refresh(e)
    return e