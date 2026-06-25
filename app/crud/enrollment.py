from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.schemas.enrollment import EnrollmentCreate


def get_enrollment(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def get_enrollments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Enrollment).offset(skip).limit(limit).all()


def count_enrollments(db: Session) -> int:
    return db.query(Enrollment).count()


def get_existing_enrollment(db: Session, student_id: int, course_id: int):
    return (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student_id, Enrollment.course_id == course_id)
        .first()
    )


def get_course_enrollment_count(db: Session, course_id: int) -> int:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).count()


def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    """
    Enroll a student in a course.
    Returns:
        Enrollment object on success
        "duplicate"  if already enrolled
        "full"       if course has no seats left
        "not_found"  if course doesn't exist
    """
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        return "not_found"

    existing = get_existing_enrollment(db, enrollment.student_id, enrollment.course_id)
    if existing:
        return "duplicate"

    current_count = get_course_enrollment_count(db, enrollment.course_id)
    if current_count >= course.capacity:
        return "full"

    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = get_enrollment(db, enrollment_id)
    if not db_enrollment:
        return False
    db.delete(db_enrollment)
    db.commit()
    return True
