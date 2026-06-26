from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    branch: str
    year: int

class StudentUpdate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    branch: str
    year: int

class StudentPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    branch: str
    year: int
    is_active: bool
    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    instructor: str

class CourseUpdate(BaseModel):
    name: str
    code: str
    credits: int
    instructor: str

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    instructor: str
    class Config:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: Optional[float]
    class Config:
        from_attributes = True

class GradeUpdate(BaseModel):
    grade: float