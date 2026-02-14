from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Course, CourseCreate, CourseUpdate
from app.database import db

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)


def verify_admin(admin_id: int):
    """Helper function to verify admin role"""
    user = db.get_user(admin_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin user not found"
        )
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action"
        )
    return user


@router.get("/", response_model=List[Course])
def get_all_courses():
    """
    Retrieve all courses.
    
    Public access - anyone can view courses.
    """
    return db.get_all_courses()


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    """
    Retrieve a course by ID.
    
    Public access - anyone can view a course.
    """
    course = db.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    """
    Create a new course.
    
    Admin-only access.
    
    Validation:
    - title must not be empty
    - code must not be empty and must be unique
    """
    # Verify admin
    verify_admin(course.admin_id)
    
    # Check if course code already exists
    if db.course_code_exists(course.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    
    new_course = db.create_course(
        title=course.title,
        code=course.code
    )
    return new_course


@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course: CourseUpdate):
    """
    Update a course.
    
    Admin-only access.
    
    Validation:
    - title must not be empty
    - code must not be empty and must be unique
    """
    # Verify admin
    verify_admin(course.admin_id)
    
    # Check if course exists
    existing_course = db.get_course(course_id)
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if course code already exists (excluding current course)
    if db.course_code_exists(course.code, exclude_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    
    updated_course = db.update_course(
        course_id=course_id,
        title=course.title,
        code=course.code
    )
    return updated_course


@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def delete_course(course_id: int, admin_id: int):
    """
    Delete a course.
    
    Admin-only access.
    
    Also deletes all enrollments for this course.
    """
    # Verify admin
    verify_admin(admin_id)
    
    # Check if course exists
    course = db.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    db.delete_course(course_id)
    return {"detail": "Course deleted successfully"}
