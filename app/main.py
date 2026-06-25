from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import instructors, courses, students, enrollments

app = FastAPI(
    title="Learning Management API",
    description="""
A REST API for managing an online learning platform.

## Features
- **Instructors** – Create and manage instructors
- **Courses** – Create courses with capacity limits, search by title/category/instructor
- **Students** – Register and manage students
- **Enrollments** – Enroll students, track capacity, list enrolled students
    """,
    version="1.0.0",
    contact={"name": "Kapish", "email": "kapish@example.com"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(instructors.router)
app.include_router(courses.router)
app.include_router(students.router)
app.include_router(enrollments.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Learning Management API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
