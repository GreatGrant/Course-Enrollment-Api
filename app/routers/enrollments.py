from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Enrollment, EnrollmentCreate
from app.database import db

router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)


def verify_student(user_id: int):
    """Helper function to verify student role"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can perform this action"
        )
    return user


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


@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment: EnrollmentCreate):
    """
    Enroll a student in a course.
    
    Student-only access.
    
    Rules:
    - Only users with role 'student' can enroll
    - A student cannot enroll in the same course more than once
    - Enrollment must fail if the student or course does not exist
    """
    # Verify student
    verify_student(enrollment.user_id)
    
    # Check if course exists
    course = db.get_course(enrollment.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if already enrolled
    if db.enrollment_exists(enrollment.user_id, enrollment.course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course"
        )
    
    new_enrollment = db.create_enrollment(
        user_id=enrollment.user_id,
        course_id=enrollment.course_id
    )
    return new_enrollment


@router.delete("/{enrollment_id}", status_code=status.HTTP_200_OK)
def deregister_student(enrollment_id: int, user_id: int):
    """
    Deregister a student from a course.
    
    Student-only access.
    
    Rules:
    - Only students can deregister themselves
    - Deregistration must fail if the enrollment does not exist
    - Students can only deregister their own enrollments
    """
    # Get enrollment
    enrollment = db.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Verify student
    verify_student(user_id)
    
    # Verify the enrollment belongs to this student
    if enrollment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Students can only deregister their own enrollments"
        )
    
    db.delete_enrollment(enrollment_id)
    return {"detail": "Successfully deregistered from course"}


@router.get("/student/{user_id}", response_model=List[Enrollment])
def get_student_enrollments(user_id: int):
    """
    Retrieve enrollments for a specific student.
    
    Public access - anyone can view a student's enrollments.
    """
    # Check if user exists
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    enrollments = db.get_enrollments_by_student(user_id)
    return enrollments


@router.get("/", response_model=List[Enrollment])
def get_all_enrollments(admin_id: int):
    """
    Retrieve all enrollments.
    
    Admin-only access.
    """
    # Verify admin
    verify_admin(admin_id)
    
    return db.get_all_enrollments()


@router.get("/course/{course_id}", response_model=List[Enrollment])
def get_course_enrollments(course_id: int, admin_id: int):
    """
    Retrieve enrollments for a specific course.
    
    Admin-only access.
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
    
    enrollments = db.get_enrollments_by_course(course_id)
    return enrollments


@router.delete("/admin/{enrollment_id}", status_code=status.HTTP_200_OK)
def admin_force_deregister(enrollment_id: int, admin_id: int):
    """
    Force deregister a student from a course.
    
    Admin-only access.
    
    Allows admins to remove any student enrollment.
    """
    # Verify admin
    verify_admin(admin_id)
    
    # Get enrollment
    enrollment = db.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    db.delete_enrollment(enrollment_id)
    return {"detail": "Student successfully deregistered by admin"}
