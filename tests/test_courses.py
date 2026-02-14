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


class TestCoursePublicAccess:
    """Test public course access endpoints"""
    
    def test_get_all_courses_empty(self):
        """Test getting all courses when database is empty"""
        response = client.get("/courses/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_courses(self, admin_user):
        """Test getting all courses"""
        # Create multiple courses
        client.post(
            "/courses/",
            json={
                "title": "Course 1",
                "code": "CS101",
                "admin_id": admin_user["id"]
            }
        )
        client.post(
            "/courses/",
            json={
                "title": "Course 2",
                "code": "CS102",
                "admin_id": admin_user["id"]
            }
        )
        
        response = client.get("/courses/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Course 1"
        assert data[1]["title"] == "Course 2"
    
    def test_get_course_by_id(self, sample_course):
        """Test getting a course by ID"""
        response = client.get(f"/courses/{sample_course['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_course["id"]
        assert data["title"] == sample_course["title"]
        assert data["code"] == sample_course["code"]
    
    def test_get_course_not_found(self):
        """Test getting a non-existent course"""
        response = client.get("/courses/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCourseCreation:
    """Test course creation (admin only)"""
    
    def test_create_course_as_admin(self, admin_user):
        """Test creating a course as admin"""
        response = client.post(
            "/courses/",
            json={
                "title": "Data Structures",
                "code": "CS201",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Data Structures"
        assert data["code"] == "CS201"
        assert "id" in data
    
    def test_create_course_as_student_fails(self, student_user):
        """Test that students cannot create courses"""
        response = client.post(
            "/courses/",
            json={
                "title": "Unauthorized Course",
                "code": "CS999",
                "admin_id": student_user["id"]
            }
        )
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_create_course_nonexistent_admin(self):
        """Test creating course with non-existent admin ID"""
        response = client.post(
            "/courses/",
            json={
                "title": "Test Course",
                "code": "CS999",
                "admin_id": 999
            }
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_create_course_empty_title(self, admin_user):
        """Test that empty title fails validation"""
        response = client.post(
            "/courses/",
            json={
                "title": "",
                "code": "CS101",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 422
    
    def test_create_course_whitespace_title(self, admin_user):
        """Test that whitespace-only title fails validation"""
        response = client.post(
            "/courses/",
            json={
                "title": "   ",
                "code": "CS101",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 422
    
    def test_create_course_empty_code(self, admin_user):
        """Test that empty code fails validation"""
        response = client.post(
            "/courses/",
            json={
                "title": "Test Course",
                "code": "",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 422
    
    def test_create_course_duplicate_code(self, admin_user, sample_course):
        """Test that duplicate course code fails"""
        response = client.post(
            "/courses/",
            json={
                "title": "Different Course",
                "code": sample_course["code"],  # Duplicate code
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()


class TestCourseUpdate:
    """Test course update (admin only)"""
    
    def test_update_course_as_admin(self, admin_user, sample_course):
        """Test updating a course as admin"""
        response = client.put(
            f"/courses/{sample_course['id']}",
            json={
                "title": "Advanced Python",
                "code": "CS101A",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Advanced Python"
        assert data["code"] == "CS101A"
        assert data["id"] == sample_course["id"]
    
    def test_update_course_as_student_fails(self, student_user, sample_course):
        """Test that students cannot update courses"""
        response = client.put(
            f"/courses/{sample_course['id']}",
            json={
                "title": "Hacked Course",
                "code": "HACK",
                "admin_id": student_user["id"]
            }
        )
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_update_nonexistent_course(self, admin_user):
        """Test updating a non-existent course"""
        response = client.put(
            "/courses/999",
            json={
                "title": "Ghost Course",
                "code": "GH999",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_course_duplicate_code(self, admin_user):
        """Test updating course with duplicate code"""
        # Create two courses
        course1 = client.post(
            "/courses/",
            json={
                "title": "Course 1",
                "code": "CS101",
                "admin_id": admin_user["id"]
            }
        ).json()
        
        course2 = client.post(
            "/courses/",
            json={
                "title": "Course 2",
                "code": "CS102",
                "admin_id": admin_user["id"]
            }
        ).json()
        
        # Try to update course2 with course1's code
        response = client.put(
            f"/courses/{course2['id']}",
            json={
                "title": "Updated Course 2",
                "code": "CS101",  # Duplicate
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
    
    def test_update_course_same_code(self, admin_user, sample_course):
        """Test that updating with the same code works"""
        response = client.put(
            f"/courses/{sample_course['id']}",
            json={
                "title": "Updated Title",
                "code": sample_course["code"],  # Same code
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 200


class TestCourseDelete:
    """Test course deletion (admin only)"""
    
    def test_delete_course_as_admin(self, admin_user, sample_course):
        """Test deleting a course as admin"""
        response = client.delete(
            f"/courses/{sample_course['id']}?admin_id={admin_user['id']}"
        )
        assert response.status_code == 200
        assert "deleted" in response.json()["detail"].lower()
        
        # Verify course is deleted
        get_response = client.get(f"/courses/{sample_course['id']}")
        assert get_response.status_code == 404
    
    def test_delete_course_as_student_fails(self, student_user, sample_course):
        """Test that students cannot delete courses"""
        response = client.delete(
            f"/courses/{sample_course['id']}?admin_id={student_user['id']}"
        )
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_delete_nonexistent_course(self, admin_user):
        """Test deleting a non-existent course"""
        response = client.delete(
            f"/courses/999?admin_id={admin_user['id']}"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_delete_course_removes_enrollments(self, admin_user, student_user, sample_course):
        """Test that deleting a course also removes all enrollments"""
        # Enroll student in course
        client.post(
            "/enrollments/",
            json={
                "user_id": student_user["id"],
                "course_id": sample_course["id"]
            }
        )
        
        # Verify enrollment exists
        enrollments_before = client.get(
            f"/enrollments/student/{student_user['id']}"
        ).json()
        assert len(enrollments_before) == 1
        
        # Delete course
        client.delete(
            f"/courses/{sample_course['id']}?admin_id={admin_user['id']}"
        )
        
        # Verify enrollments are deleted
        enrollments_after = client.get(
            f"/enrollments/student/{student_user['id']}"
        ).json()
        assert len(enrollments_after) == 0


class TestCourseValidation:
    """Test course validation edge cases"""
    
    def test_course_code_uniqueness_case_sensitive(self, admin_user):
        """Test that course codes are case-sensitive for uniqueness"""
        # Create course with lowercase code
        client.post(
            "/courses/",
            json={
                "title": "Course 1",
                "code": "cs101",
                "admin_id": admin_user["id"]
            }
        )
        
        # Should be able to create with uppercase code
        response = client.post(
            "/courses/",
            json={
                "title": "Course 2",
                "code": "CS101",
                "admin_id": admin_user["id"]
            }
        )
        assert response.status_code == 201
