from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.instructor import InstructorCreate, InstructorUpdate, InstructorResponse
from app.crud import instructor as crud

router = APIRouter(prefix="/instructors", tags=["Instructors"])


@router.post("/", response_model=InstructorResponse, status_code=201)
def create_instructor(payload: InstructorCreate, db: Session = Depends(get_db)):
    """Create a new instructor."""
    existing = crud.get_instructor_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_instructor(db, payload)


@router.get("/", response_model=dict)
def list_instructors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """List all instructors with pagination."""
    total = crud.count_instructors(db)
    items = crud.get_instructors(db, skip=skip, limit=limit)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [InstructorResponse.model_validate(i) for i in items],
    }


@router.get("/{instructor_id}", response_model=InstructorResponse)
def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    """Get a single instructor by ID."""
    db_instructor = crud.get_instructor(db, instructor_id)
    if not db_instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return db_instructor


@router.put("/{instructor_id}", response_model=InstructorResponse)
def update_instructor(instructor_id: int, payload: InstructorUpdate, db: Session = Depends(get_db)):
    """Update an instructor."""
    if payload.email:
        existing = crud.get_instructor_by_email(db, payload.email)
        if existing and existing.id != instructor_id:
            raise HTTPException(status_code=400, detail="Email already in use")
    updated = crud.update_instructor(db, instructor_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return updated


@router.delete("/{instructor_id}", status_code=204)
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    """Delete an instructor."""
    deleted = crud.delete_instructor(db, instructor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Instructor not found")
