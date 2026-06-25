from sqlalchemy.orm import Session
from typing import Optional
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    category: Optional[str] = None,
    instructor_id: Optional[int] = None,
):
    query = db.query(Course)
    if title:
        query = query.filter(Course.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Course.category.ilike(f"%{category}%"))
    if instructor_id:
        query = query.filter(Course.instructor_id == instructor_id)
    return query.offset(skip).limit(limit).all()


def count_courses(
    db: Session,
    title: Optional[str] = None,
    category: Optional[str] = None,
    instructor_id: Optional[int] = None,
) -> int:
    query = db.query(Course)
    if title:
        query = query.filter(Course.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Course.category.ilike(f"%{category}%"))
    if instructor_id:
        query = query.filter(Course.instructor_id == instructor_id)
    return query.count()


def get_enrollment_count(db: Session, course_id: int) -> int:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).count()


def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course: CourseUpdate):
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    update_data = course.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = get_course(db, course_id)
    if not db_course:
        return False
    db.delete(db_course)
    db.commit()
    return True


def get_enrolled_students(db: Session, course_id: int):
    course = get_course(db, course_id)
    if not course:
        return None
    return [enrollment.student for enrollment in course.enrollments]
