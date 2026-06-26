# 🎓 Student Management System API

A REST API built with **FastAPI**, **SQLAlchemy ORM**, and **PostgreSQL**  
as part of the **Generative AI Internship** selection project.

---

## 🛠️ Tech Stack

| Technology   | Purpose              |
| ------------ | -------------------- |
| Python 3.12  | Programming Language |
| FastAPI      | API Framework        |
| SQLAlchemy   | ORM                  |
| PostgreSQL   | Database             |
| Pydantic     | Data Validation      |
| Uvicorn      | ASGI Server          |
| API Key Auth | Authentication       |

---

## 📁 Project Structure

student_management/

├── main.py # FastAPI app entry point

├── database.py # SQLAlchemy engine + session

├── models.py # ORM models (DB tables)

├── schemas.py # Pydantic schemas

├── auth.py # API Key authentication

├── routers/

│ ├── students.py

│ └── courses.py

├── .env # Environment variables

└── README.md

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/student-management-api.git
cd student-management-api
```

### 2. Install dependencies

```bash
uv add fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv "pydantic[email]"
```

### 3. Configure environment

Create `.env` file:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/student_management

API_KEY=mysecretapikey123

### 4. Run the application

```bash
uv run uvicorn main:app --reload
```

### 5. Open Swagger UI

http://127.0.0.1:8000/docs

---

## 🔐 Authentication

This API uses **API Key based Authentication**.  
Add this header to protected requests:
X-API-Key: mysecretapikey123
In Swagger UI → click **Authorize 🔓** → enter the key.

---

## 📡 API Endpoints

### Students

| Method | Endpoint                    | Auth | Description      |
| ------ | --------------------------- | ---- | ---------------- |
| POST   | `/students/`                | ✅   | Create student   |
| GET    | `/students/`                | ❌   | Get all students |
| GET    | `/students/{id}`            | ❌   | Get by ID        |
| GET    | `/students/branch/{branch}` | ❌   | Filter by branch |
| PUT    | `/students/{id}`            | ✅   | Full update      |
| PATCH  | `/students/{id}`            | ✅   | Partial update   |
| DELETE | `/students/{id}`            | ✅   | Soft delete      |
| DELETE | `/students/{id}/hard`       | ✅   | Hard delete      |
| GET    | `/students/{id}/courses`    | ❌   | Student courses  |

### Courses

| Method | Endpoint                            | Auth | Description     |
| ------ | ----------------------------------- | ---- | --------------- |
| POST   | `/courses/`                         | ✅   | Create course   |
| GET    | `/courses/`                         | ❌   | Get all courses |
| GET    | `/courses/{id}`                     | ❌   | Get by ID       |
| PUT    | `/courses/{id}`                     | ✅   | Update course   |
| DELETE | `/courses/{id}`                     | ✅   | Delete course   |
| POST   | `/courses/{id}/enroll/{student_id}` | ✅   | Enroll student  |
| PATCH  | `/courses/enrollment/{id}/grade`    | ✅   | Update grade    |

---

## 🗄️ Database Schema

students

├── id (Primary Key)

├── name

├── email (unique)

├── phone

├── branch

├── year

└── is_active (soft delete)
courses

├── id (Primary Key)

├── name

├── code (unique)

├── credits

└── instructor
enrollments

├── id (Primary Key)

├── student_id (Foreign Key)

├── course_id (Foreign Key)

└── grade

---

## 🧪 Sample Request & Response

**POST /students/**

```json
{
  "name": "Uma Baleboyina",
  "email": "uma@example.com",
  "phone": "7569697423",
  "branch": "CSE",
  "year": 4
}
```

**Response:**

```json
{
  "id": 1,
  "name": "Uma Baleboyina",
  "email": "uma@example.com",
  "phone": "7569697423",
  "branch": "CSE",
  "year": 4,
  "is_active": true
}
```

---

## 👤 Author

**Uma Baleboyina**  
B.Tech CSE — Anurag Engineering College, Kodad  
Generative AI Internship Project — 2026
