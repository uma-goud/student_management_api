from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db
from routers import students, courses
from auth import verify_api_key
import logging
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management System",
    description="REST API with FastAPI + SQLAlchemy + PostgreSQL",
    version="1.0.0"
)


# ERROR HANDLERS


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid input data",
            "details": exc.errors()
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.error(f"404 Not Found: {request.url}")
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "Resource not found"
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )


# ROUTERS

app.include_router(students.router)
app.include_router(courses.router)


# ROUTES

@app.get("/", tags=["Health"])
def root(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected ✅"
    except Exception:
        db_status = "disconnected ❌"
    logger.info("Health check called")
    return {
        "status": "healthy",
        "message": "API is running 🚀",
        "database": db_status,
        "version": "1.0.0",
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.get("/me", tags=["Auth"])
def get_me(api_key: str = Depends(verify_api_key)):
    return {"message": "Authenticated ✅", "api_key": api_key}