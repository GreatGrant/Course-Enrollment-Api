from typing import List, Optional
from app.models import User, Course, Enrollment


class Database:
    def __init__(self):
        self.users: List[User] = []
        self.courses: List[Course] = []
        self.enrollments: List[Enrollment] = []
        self.user_id_counter = 1
        self.course_id_counter = 1
        self.enrollment_id_counter = 1

    def reset(self):
        """Reset all data - useful for testing"""
        self.users = []
        self.courses = []
        self.enrollments = []
        self.user_id_counter = 1
        self.course_id_counter = 1
        self.enrollment_id_counter = 1

    # User operations
    def create_user(self, name: str, email: str, role: str) -> User:
        user = User(
            id=self.user_id_counter,
            name=name,
            email=email,
            role=role
        )
        self.users.append(user)
        self.user_id_counter += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_all_users(self) -> List[User]:
        return self.users.copy()

    def email_exists(self, email: str) -> bool:
        return any(user.email == email for user in self.users)

    # Course operations
    def create_course(self, title: str, code: str) -> Course:
        course = Course(
            id=self.course_id_counter,
            title=title,
            code=code
        )
        self.courses.append(course)
        self.course_id_counter += 1
        return course

    def get_course(self, course_id: int) -> Optional[Course]:
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def get_all_courses(self) -> List[Course]:
        return self.courses.copy()

    def course_code_exists(self, code: str, exclude_id: Optional[int] = None) -> bool:
        for course in self.courses:
            if course.code == code and course.id != exclude_id:
                return True
        return False

    def update_course(self, course_id: int, title: str, code: str) -> Optional[Course]:
        for course in self.courses:
            if course.id == course_id:
                course.title = title
                course.code = code
                return course
        return None

    def delete_course(self, course_id: int) -> bool:
        for i, course in enumerate(self.courses):
            if course.id == course_id:
                del self.courses[i]
                # Also delete all enrollments for this course
                self.enrollments = [
                    e for e in self.enrollments if e.course_id != course_id
                ]
                return True
        return False

    # Enrollment operations
    def create_enrollment(self, user_id: int, course_id: int) -> Enrollment:
        enrollment = Enrollment(
            id=self.enrollment_id_counter,
            user_id=user_id,
            course_id=course_id
        )
        self.enrollments.append(enrollment)
        self.enrollment_id_counter += 1
        return enrollment

    def get_enrollment(self, enrollment_id: int) -> Optional[Enrollment]:
        for enrollment in self.enrollments:
            if enrollment.id == enrollment_id:
                return enrollment
        return None

    def get_all_enrollments(self) -> List[Enrollment]:
        return self.enrollments.copy()

    def get_enrollments_by_student(self, user_id: int) -> List[Enrollment]:
        return [e for e in self.enrollments if e.user_id == user_id]

    def get_enrollments_by_course(self, course_id: int) -> List[Enrollment]:
        return [e for e in self.enrollments if e.course_id == course_id]

    def enrollment_exists(self, user_id: int, course_id: int) -> bool:
        return any(
            e.user_id == user_id and e.course_id == course_id
            for e in self.enrollments
        )

    def delete_enrollment(self, enrollment_id: int) -> bool:
        for i, enrollment in enumerate(self.enrollments):
            if enrollment.id == enrollment_id:
                del self.enrollments[i]
                return True
        return False


# Global database instance
db = Database()
