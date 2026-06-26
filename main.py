from fastapi import FastAPI, Depends
from database import engine, Base
from routers import students, courses
from auth import verify_api_key

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management System",
    description="REST API with FastAPI + SQLAlchemy + PostgreSQL",
    version="1.0.0"
)

app.include_router(students.router)
app.include_router(courses.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "API is running 🚀 visit /docs for Swagger UI"}

@app.get("/me", tags=["Auth"])
def get_me(api_key: str = Depends(verify_api_key)):
    return {"message": "Authenticated ✅", "api_key": api_key}