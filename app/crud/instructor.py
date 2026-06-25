from sqlalchemy.orm import Session
from app.models.instructor import Instructor
from app.schemas.instructor import InstructorCreate, InstructorUpdate


def get_instructor(db: Session, instructor_id: int):
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()


def get_instructor_by_email(db: Session, email: str):
    return db.query(Instructor).filter(Instructor.email == email).first()


def get_instructors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Instructor).offset(skip).limit(limit).all()


def count_instructors(db: Session) -> int:
    return db.query(Instructor).count()


def create_instructor(db: Session, instructor: InstructorCreate):
    db_instructor = Instructor(**instructor.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor


def update_instructor(db: Session, instructor_id: int, instructor: InstructorUpdate):
    db_instructor = get_instructor(db, instructor_id)
    if not db_instructor:
        return None
    update_data = instructor.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_instructor, key, value)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor


def delete_instructor(db: Session, instructor_id: int):
    db_instructor = get_instructor(db, instructor_id)
    if not db_instructor:
        return False
    db.delete(db_instructor)
    db.commit()
    return True
