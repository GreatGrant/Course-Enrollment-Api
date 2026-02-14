"""
Sample Data Script

This script populates the API with sample data for demonstration and testing purposes.
Run this after starting the API server.

Usage:
    python populate_sample_data.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def create_user(name, email, role):
    """Create a user"""
    response = requests.post(
        f"{BASE_URL}/users/",
        json={"name": name, "email": email, "role": role}
    )
    if response.status_code == 201:
        user = response.json()
        print(f"Created {role}: {name} (ID: {user['id']})")
        return user
    else:
        print(f"Failed to create {name}: {response.json()}")
        return None


def create_course(title, code, admin_id):
    """Create a course"""
    response = requests.post(
        f"{BASE_URL}/courses/",
        json={"title": title, "code": code, "admin_id": admin_id}
    )
    if response.status_code == 201:
        course = response.json()
        print(f"Created course: {title} (ID: {course['id']})")
        return course
    else:
        print(f"Failed to create {title}: {response.json()}")
        return None


def enroll_student(user_id, course_id):
    """Enroll a student in a course"""
    response = requests.post(
        f"{BASE_URL}/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    if response.status_code == 201:
        enrollment = response.json()
        print(f"Enrolled student {user_id} in course {course_id} (Enrollment ID: {enrollment['id']})")
        return enrollment
    else:
        print(f"Failed to enroll: {response.json()}")
        return None


def main():
    print("=" * 60)
    print("Course Enrollment API - Sample Data Population")
    print("=" * 60)
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("API is not responding. Please start the server first.")
            return
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Please start the server first:")
        print("  uvicorn app.main:app --reload")
        return
    
    print("API is running. Creating sample data...\n")
    
    # Create Admin Users
    print("Creating Admin Users:")
    admin1 = create_user("Dr. Chukwu Okafor", "chukwu.okafor@university.edu", "admin")
    admin2 = create_user("Prof. Amara Nwosu", "amara.nwosu@university.edu", "admin")
    print()
    
    # Create Student Users
    print("Creating Student Users:")
    student1 = create_user("Chioma Oluwaseun", "chioma.oluwaseun@student.edu", "student")
    student2 = create_user("Adedayo Hassan", "adedayo.hassan@student.edu", "student")
    student3 = create_user("Kunle Adeniran", "kunle.adeniran@student.edu", "student")
    student4 = create_user("Ife Adebayo", "ife.adebayo@student.edu", "student")
    student5 = create_user("Emeka Ugwu", "emeka.ugwu@student.edu", "student")
    print()
    
    if not admin1 or not student1:
        print("Failed to create required users. Exiting.")
        return
    
    # Create Courses
    print("Creating Courses:")
    course1 = create_course(
        "Introduction to Python Programming",
        "CS101",
        admin1["id"]
    )
    course2 = create_course(
        "Data Structures and Algorithms",
        "CS201",
        admin1["id"]
    )
    course3 = create_course(
        "Web Development with FastAPI",
        "CS301",
        admin2["id"]
    )
    course4 = create_course(
        "Database Management Systems",
        "CS202",
        admin2["id"]
    )
    course5 = create_course(
        "Machine Learning Fundamentals",
        "CS401",
        admin1["id"]
    )
    print()
    
    if not course1:
        print("Failed to create courses. Exiting.")
        return
    
    # Create Enrollments
    print("Creating Enrollments:")
    
    # Student 1 enrolls in 3 courses
    enroll_student(student1["id"], course1["id"])
    enroll_student(student1["id"], course2["id"])
    enroll_student(student1["id"], course3["id"])
    
    # Student 2 enrolls in 2 courses
    enroll_student(student2["id"], course1["id"])
    enroll_student(student2["id"], course4["id"])
    
    # Student 3 enrolls in 4 courses
    enroll_student(student3["id"], course1["id"])
    enroll_student(student3["id"], course2["id"])
    enroll_student(student3["id"], course3["id"])
    enroll_student(student3["id"], course5["id"])
    
    # Student 4 enrolls in 1 course
    enroll_student(student4["id"], course5["id"])
    
    # Student 5 enrolls in 2 courses
    enroll_student(student5["id"], course2["id"])
    enroll_student(student5["id"], course4["id"])
    
    print()
    print("=" * 60)
    print("Sample Data Creation Complete!")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  - 2 Admins created")
    print(f"  - 5 Students created")
    print(f"  - 5 Courses created")
    print(f"   12 Enrollments created")
    print()
    print("You can now:")
    print(f"  - View all courses: {BASE_URL}/courses/")
    print(f"  - View all users: {BASE_URL}/users/")
    print(f"   View interactive docs: {BASE_URL}/docs")
    print()


if __name__ == "__main__":
    main()
