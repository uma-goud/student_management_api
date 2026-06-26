from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"
    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    email     = Column(String, unique=True, nullable=False)
    phone     = Column(String)
    branch    = Column(String, nullable=False)
    year      = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    code       = Column(String, unique=True, nullable=False)
    credits    = Column(Integer, nullable=False)
    instructor = Column(String, nullable=False)
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id  = Column(Integer, ForeignKey("courses.id"), nullable=False)
    grade      = Column(Float, nullable=True)
    student    = relationship("Student", back_populates="enrollments")
    course     = relationship("Course", back_populates="enrollments")