import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    db.reset()
    yield
    db.reset()


@pytest.fixture
def admin_user():
    """Create an admin user"""
    response = client.post(
        "/users/",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "role": "admin"
        }
    )
    return response.json()


@pytest.fixture
def student_user():
    """Create a student user"""
    response = client.post(
        "/users/",
        json={
            "name": "Student User",
            "email": "student@example.com",
            "role": "student"
        }
    )
    return response.json()


@pytest.fixture
def student_user2():
    """Create a second student user"""
    response = client.post(
        "/users/",
        json={
            "name": "Student User 2",
            "email": "student2@example.com",
            "role": "student"
        }
    )
    return response.json()


@pytest.fixture
def sample_course(admin_user):
    """Create a sample course"""
    response = client.post(
        "/courses/",
        json={
            "title": "Introduction to Python",
            "code": "CS101",
            "admin_id": admin_user["id"]
        }
    )
    return response.json()


@pytest.fixture
def sample_course2(admin_user):
    """Create a second sample course"""
    response = client.post(
        "/courses/",
        json={
            "title": "Data Structures",
            "code": "CS201",
            "admin_id": admin_user["id"]
        }
    )
    return response.json()


class TestStudentEnrollment:
    """Test student enrollment functionality"""
    
    def test_enroll_student_in_course(self, student_user, sample_course):
        """Test enrolling a student in a course"""
        response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == student_user["id"]
        assert data["course_id"] == sample_course["id"]
        assert "id" in data
    
    def test_enroll_admin_fails(self, admin_user, sample_course):
        """Test that admins cannot enroll in courses"""
        response = client.post(
            "/enrollments/",
            json={
                "user_id": admin_user["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response.status_code == 403
        assert "student" in response.json()["detail"].lower()
    
    def test_enroll_nonexistent_student(self, sample_course):
        """Test enrolling a non-existent student"""
        response = client.post(
            "/enrollments/",
            json={
                "user_id": 999,
                "course_id": sample_course["id"]
            }
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_enroll_in_nonexistent_course(self, student_user):
        """Test enrolling in a non-existent course"""
        response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": 999
            }
        )
        assert response.status_code == 404
        assert "course not found" in response.json()["detail"].lower()
    
    def test_duplicate_enrollment_fails(self, student_user, sample_course):
        """Test that a student cannot enroll in the same course twice"""
        # First enrollment
        response1 = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response1.status_code == 201
        
        # Second enrollment (should fail)
        response2 = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response2.status_code == 400
        assert "already enrolled" in response2.json()["detail"].lower()
    
    def test_student_enroll_multiple_courses(self, student_user, sample_course, sample_course2):
        """Test that a student can enroll in multiple courses"""
        # Enroll in first course
        response1 = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response1.status_code == 201
        
        # Enroll in second course
        response2 = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course2["id"]
            }
        )
        assert response2.status_code == 201
        
        # Verify both enrollments
        enrollments = client.get(f"/enrollments/student/{student_user['id']}").json()
        assert len(enrollments) == 2
    
    def test_multiple_students_same_course(self, student_user, student_user2, sample_course):
        """Test that multiple students can enroll in the same course"""
        # Enroll first student
        response1 = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response1.status_code == 201
        
        # Enroll second student
        response2 = client.post(
            "/enrollments/",
            json={
                "user_id": student_user2["id"],
                "course_id": sample_course["id"]
            }
        )
        assert response2.status_code == 201


class TestStudentDeregistration:
    """Test student deregistration functionality"""
    
    def test_deregister_student(self, student_user, sample_course):
        """Test deregistering a student from a course"""
        # First enroll
        enroll_response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        enrollment_id = enroll_response.json()["id"]
        
        # Then deregister
        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": student_user["id"]}
        )
        assert response.status_code == 200
        assert "deregistered" in response.json()["detail"].lower()
        
        # Verify enrollment is deleted
        enrollments = client.get(f"/enrollments/student/{student_user['id']}").json()
        assert len(enrollments) == 0
    
    def test_deregister_nonexistent_enrollment(self, student_user):
        """Test deregistering from a non-existent enrollment"""
        response = client.delete(
            "/enrollments/999",
            params={"user_id": student_user["id"]}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_deregister_as_admin_fails(self, admin_user, student_user, sample_course):
        """Test that admins cannot use student deregister endpoint"""
        # Enroll student
        enroll_response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        enrollment_id = enroll_response.json()["id"]
        
        # Try to deregister as admin
        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": admin_user["id"]}
        )
        assert response.status_code == 403
        assert "student" in response.json()["detail"].lower()
    
    def test_deregister_other_student_enrollment(self, student_user, student_user2, sample_course):
        """Test that a student cannot deregister another student's enrollment"""
        # Enroll first student
        enroll_response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        enrollment_id = enroll_response.json()["id"]
        
        # Try to deregister as second student
        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": student_user2["id"]}
        )
        assert response.status_code == 403
        assert "own" in response.json()["detail"].lower()
    
    def test_deregister_with_nonexistent_user(self, student_user, sample_course):
        """Test deregistering with non-existent user ID"""
        # Enroll student
        enroll_response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        enrollment_id = enroll_response.json()["id"]
        
        # Try to deregister with non-existent user
        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": 999}
        )
        assert response.status_code == 404


class TestEnrollmentRetrieval:
    """Test enrollment retrieval endpoints"""
    
    def test_get_student_enrollments(self, student_user, sample_course, sample_course2):
        """Test getting enrollments for a specific student"""
        # Enroll in multiple courses
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course2["id"]
            }
        )
        
        # Get enrollments
        response = client.get(f"/enrollments/student/{student_user['id']}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(e["user_id"] == student_user["id"] for e in data)
    
    def test_get_student_enrollments_empty(self, student_user):
        """Test getting enrollments for student with no enrollments"""
        response = client.get(f"/enrollments/student/{student_user['id']}")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_student_enrollments_nonexistent_user(self):
        """Test getting enrollments for non-existent user"""
        response = client.get("/enrollments/student/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestAdminEnrollmentOversight:
    """Test admin enrollment oversight functionality"""
    
    def test_admin_get_all_enrollments(self, admin_user, student_user, student_user2, 
                                       sample_course, sample_course2):
        """Test admin getting all enrollments"""
        # Create multiple enrollments
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user2["id"],
                "course_id": sample_course2["id"]
            }
        )
        
        # Get all enrollments as admin
        response = client.get(
            "/enrollments/",
            params={"admin_id": admin_user["id"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_student_cannot_get_all_enrollments(self, student_user):
        """Test that students cannot get all enrollments"""
        response = client.get(
            "/enrollments/",
            params={"admin_id": student_user["id"]}
        )
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_admin_get_course_enrollments(self, admin_user, student_user, student_user2, 
                                          sample_course):
        """Test admin getting enrollments for a specific course"""
        # Enroll multiple students in same course
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user2["id"],
                "course_id": sample_course["id"]
            }
        )
        
        # Get course enrollments as admin
        response = client.get(
            f"/enrollments/course/{sample_course['id']}",
            params={"admin_id": admin_user["id"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(e["course_id"] == sample_course["id"] for e in data)
    
    def test_student_cannot_get_course_enrollments(self, student_user, sample_course):
        """Test that students cannot get course enrollments"""
        response = client.get(
            f"/enrollments/course/{sample_course['id']}",
            params={"admin_id": student_user["id"]}
        )
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_admin_get_course_enrollments_nonexistent_course(self, admin_user):
        """Test admin getting enrollments for non-existent course"""
        response = client.get(
            "/enrollments/course/999",
            params={"admin_id": admin_user["id"]}
        )
        assert response.status_code == 404
        assert "course not found" in response.json()["detail"].lower()
    
    def test_admin_force_deregister(self, admin_user, student_user, sample_course):
        """Test admin force deregistering a student"""
        # Enroll student
        enroll_response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        enrollment_id = enroll_response.json()["id"]
        
        # Admin force deregister
        response = client.delete(
            f"/enrollments/admin/{enrollment_id}?admin_id={admin_user['id']}"
        )
        assert response.status_code == 200
        assert "admin" in response.json()["detail"].lower()
        
        # Verify enrollment is deleted
        enrollments = client.get(f"/enrollments/student/{student_user['id']}").json()
        assert len(enrollments) == 0
    
    def test_student_cannot_force_deregister(self, student_user, student_user2, sample_course):
        """Test that students cannot use admin force deregister"""
        # Enroll first student
        enroll_response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        enrollment_id = enroll_response.json()["id"]
        
        # Try to force deregister as student
        response = client.delete(
            f"/enrollments/admin/{enrollment_id}?admin_id={student_user2['id']}"
        )
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_admin_force_deregister_nonexistent_enrollment(self, admin_user):
        """Test admin force deregistering non-existent enrollment"""
        response = client.delete(
            f"/enrollments/admin/999?admin_id={admin_user['id']}"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestEnrollmentEdgeCases:
    """Test enrollment edge cases and complex scenarios"""
    
    def test_enrollment_after_course_recreation(self, admin_user, student_user, sample_course):
        """Test enrollment behavior when a course is deleted and recreated"""
        # Enroll student
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        
        # Delete course (should delete enrollment)
        client.delete(
            f"/courses/{sample_course['id']}?admin_id={admin_user['id']}"
        )
        
        # Create new course with same code
        new_course = client.post(
            "/courses/",
            json={
                "title": "New Python Course",
                "code": "CS101",
                "admin_id": admin_user["id"]
            }
        ).json()
        
        # Should be able to enroll in new course (different ID)
        response = client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": new_course["id"]
            }
        )
        assert response.status_code == 201
    
    def test_multiple_enrollments_same_student(self, student_user, admin_user):
        """Test student enrolling in many courses"""
        # Create multiple courses
        course_ids = []
        for i in range(5):
            course = client.post(
                "/courses/",
                json={
                    "title": f"Course {i}",
                    "code": f"CS{100 + i}",
                    "admin_id": admin_user["id"]
                }
            ).json()
            course_ids.append(course["id"])
        
        # Enroll in all courses
        for course_id in course_ids:
            response = client.post(
                "/enrollments/",
                json={
                    "user_id": student_user["id"],
                    "course_id": course_id
                }
            )
            assert response.status_code == 201
        
        # Verify all enrollments
        enrollments = client.get(f"/enrollments/student/{student_user['id']}").json()
        assert len(enrollments) == 5
