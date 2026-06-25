from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseWithEnrollmentCount
from app.schemas.student import StudentResponse
from app.crud import course as crud
from app.crud import instructor as instructor_crud

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course."""
    instructor = instructor_crud.get_instructor(db, payload.instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return crud.create_course(db, payload)


@router.get("/", response_model=dict)
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    title: Optional[str] = Query(None, description="Search by title (partial match)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    instructor_id: Optional[int] = Query(None, description="Filter by instructor ID"),
    db: Session = Depends(get_db),
):
    """
    List all courses with optional search/filter:
    - **title**: partial match on course title
    - **category**: filter by category
    - **instructor_id**: filter by instructor
    """
    total = crud.count_courses(db, title=title, category=category, instructor_id=instructor_id)
    items = crud.get_courses(db, skip=skip, limit=limit, title=title, category=category, instructor_id=instructor_id)

    results = []
    for course in items:
        enrolled = crud.get_enrollment_count(db, course.id)
        results.append(
            CourseWithEnrollmentCount(
                **CourseResponse.model_validate(course).model_dump(),
                enrolled_count=enrolled,
                seats_available=max(0, course.capacity - enrolled),
            )
        )

    return {"total": total, "skip": skip, "limit": limit, "data": results}


@router.get("/{course_id}", response_model=CourseWithEnrollmentCount)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a single course with enrollment count."""
    db_course = crud.get_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled = crud.get_enrollment_count(db, course_id)
    return CourseWithEnrollmentCount(
        **CourseResponse.model_validate(db_course).model_dump(),
        enrolled_count=enrolled,
        seats_available=max(0, db_course.capacity - enrolled),
    )


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    """Update a course."""
    if payload.instructor_id:
        instructor = instructor_crud.get_instructor(db, payload.instructor_id)
        if not instructor:
            raise HTTPException(status_code=404, detail="Instructor not found")
    updated = crud.update_course(db, course_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete a course (also removes all enrollments)."""
    deleted = crud.delete_course(db, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")


@router.get("/{course_id}/students", response_model=List[StudentResponse])
def get_enrolled_students(course_id: int, db: Session = Depends(get_db)):
    """List all students enrolled in a course."""
    students = crud.get_enrolled_students(db, course_id)
    if students is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return students
