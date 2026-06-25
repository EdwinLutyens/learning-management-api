from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.crud import student as crud

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    """Register a new student."""
    existing = crud.get_student_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, payload)


@router.get("/", response_model=dict)
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all students with pagination."""
    total = crud.count_students(db)
    items = crud.get_students(db, skip=skip, limit=limit)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [StudentResponse.model_validate(s) for s in items],
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a single student by ID."""
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    """Update a student."""
    if payload.email:
        existing = crud.get_student_by_email(db, payload.email)
        if existing and existing.id != student_id:
            raise HTTPException(status_code=400, detail="Email already in use")
    updated = crud.update_student(db, student_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student."""
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
