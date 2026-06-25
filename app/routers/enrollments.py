from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentDetailResponse
from app.crud import enrollment as crud
from app.crud import student as student_crud

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/", response_model=EnrollmentResponse, status_code=201)
def enroll_student(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    """
    Enroll a student in a course.
    - Returns **400** if student is already enrolled
    - Returns **400** if course is at full capacity
    - Returns **404** if student or course not found
    """
    student = student_crud.get_student(db, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = crud.create_enrollment(db, payload)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Course not found")
    if result == "duplicate":
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")
    if result == "full":
        raise HTTPException(status_code=400, detail="Course has reached its maximum capacity")

    return result


@router.get("/", response_model=dict)
def list_enrollments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all enrollments with pagination."""
    total = crud.count_enrollments(db)
    items = crud.get_enrollments(db, skip=skip, limit=limit)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [EnrollmentResponse.model_validate(e) for e in items],
    }


@router.get("/{enrollment_id}", response_model=EnrollmentDetailResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Get a single enrollment with student and course details."""
    db_enrollment = crud.get_enrollment(db, enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment


@router.delete("/{enrollment_id}", status_code=204)
def unenroll_student(enrollment_id: int, db: Session = Depends(get_db)):
    """Unenroll a student from a course."""
    deleted = crud.delete_enrollment(db, enrollment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Enrollment not found")
