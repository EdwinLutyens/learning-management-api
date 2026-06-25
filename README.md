# Learning Management API

A RESTful API for managing an online learning platform built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework & API routing |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM (Object Relational Mapper) |
| Alembic | Database migrations |
| Pydantic v2 | Request/response validation |
| Uvicorn | ASGI server |

---

## Project Structure

```
learning_management_api/
├── app/
│   ├── main.py              # FastAPI app, router registration
│   ├── database.py          # DB engine, session, Base
│   ├── models/              # SQLAlchemy table models
│   │   ├── instructor.py
│   │   ├── course.py
│   │   ├── student.py
│   │   └── enrollment.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── instructor.py
│   │   ├── course.py
│   │   ├── student.py
│   │   └── enrollment.py
│   ├── routers/             # API route handlers
│   │   ├── instructors.py
│   │   ├── courses.py
│   │   ├── students.py
│   │   └── enrollments.py
│   └── crud/                # Database query logic
│       ├── instructor.py
│       ├── course.py
│       ├── student.py
│       └── enrollment.py
├── alembic/                 # Migration scripts
│   ├── env.py
│   └── versions/
│       └── 001_initial_tables.py
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/learning_management_api.git
cd learning_management_api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/lms_db
```

### 5. Create the PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE lms_db;
\q
```

### 6. Run Alembic migrations

```bash
alembic upgrade head
```

### 7. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

Swagger UI docs: **http://localhost:8000/docs**

---

## API Endpoints

### Instructors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/instructors/` | Create instructor |
| GET | `/instructors/` | List all (paginated) |
| GET | `/instructors/{id}` | Get by ID |
| PUT | `/instructors/{id}` | Update |
| DELETE | `/instructors/{id}` | Delete |

### Courses

| Method | Endpoint | Description |
|---|---|---|
| POST | `/courses/` | Create course |
| GET | `/courses/` | List/search courses |
| GET | `/courses/{id}` | Get by ID (with seat info) |
| PUT | `/courses/{id}` | Update |
| DELETE | `/courses/{id}` | Delete |
| GET | `/courses/{id}/students` | List enrolled students |

**Search query params:** `?title=python&category=AI&instructor_id=1`

### Students

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students/` | Register student |
| GET | `/students/` | List all (paginated) |
| GET | `/students/{id}` | Get by ID |
| PUT | `/students/{id}` | Update |
| DELETE | `/students/{id}` | Delete |

### Enrollments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/enrollments/` | Enroll student in course |
| GET | `/enrollments/` | List all enrollments |
| GET | `/enrollments/{id}` | Get enrollment details |
| DELETE | `/enrollments/{id}` | Unenroll student |

---

## Business Rules

- A student **cannot enroll twice** in the same course → `400 Already enrolled`
- A course **cannot exceed its capacity** → `400 Course is at full capacity`
- Deleting a course **removes all its enrollments** (cascade delete)
- Deleting a student **removes all their enrollments** (cascade delete)

---

## Pagination

All list endpoints support:

```
GET /courses/?skip=0&limit=10
```

Response format:
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "data": [...]
}
```

---

## Database Schema Diagram

```
┌─────────────────┐          ┌──────────────────────────┐
│   instructors   │          │         courses          │
├─────────────────┤          ├──────────────────────────┤
│ id (PK)         │◄────────┤ instructor_id (FK)        │
│ name            │          │ id (PK)                  │
│ email (unique)  │          │ title                    │
│ bio             │          │ description              │
│ created_at      │          │ category                 │
└─────────────────┘          │ capacity                 │
                             │ created_at               │
                             └────────────┬─────────────┘
                                          │
                                          │
┌─────────────────┐          ┌────────────▼─────────────┐
│    students     │          │       enrollments        │
├─────────────────┤          ├──────────────────────────┤
│ id (PK)         │◄────────┤ student_id (FK)           │
│ name            │          │ course_id (FK) ──────────┘
│ email (unique)  │          │ id (PK)
│ created_at      │          │ enrolled_at              │
└─────────────────┘          │ UNIQUE(student_id,       │
                             │        course_id)        │
                             └──────────────────────────┘
```

---

## Running Alembic Commands

```bash
# Apply all migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1

# Create a new migration after changing models
alembic revision --autogenerate -m "add_new_column"

# View migration history
alembic history
```
