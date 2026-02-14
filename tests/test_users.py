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


class TestUserCreation:
    """Test user creation endpoint"""
    
    def test_create_student_user(self):
        """Test creating a student user"""
        response = client.post(
            "/users/",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "role": "student"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["role"] == "student"
        assert "id" in data
    
    def test_create_admin_user(self):
        """Test creating an admin user"""
        response = client.post(
            "/users/",
            json={
                "name": "Admin User",
                "email": "admin@example.com",
                "role": "admin"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Admin User"
        assert data["email"] == "admin@example.com"
        assert data["role"] == "admin"
    
    def test_create_user_empty_name(self):
        """Test that empty name fails validation"""
        response = client.post(
            "/users/",
            json={
                "name": "",
                "email": "test@example.com",
                "role": "student"
            }
        )
        assert response.status_code == 422
    
    def test_create_user_whitespace_name(self):
        """Test that whitespace-only name fails validation"""
        response = client.post(
            "/users/",
            json={
                "name": "   ",
                "email": "test@example.com",
                "role": "student"
            }
        )
        assert response.status_code == 422
    
    def test_create_user_invalid_email(self):
        """Test that invalid email fails validation"""
        response = client.post(
            "/users/",
            json={
                "name": "Test User",
                "email": "invalid-email",
                "role": "student"
            }
        )
        assert response.status_code == 422
    
    def test_create_user_invalid_role(self):
        """Test that invalid role fails validation"""
        response = client.post(
            "/users/",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "role": "teacher"
            }
        )
        assert response.status_code == 422
    
    def test_create_user_duplicate_email(self):
        """Test that duplicate email fails"""
        # Create first user
        client.post(
            "/users/",
            json={
                "name": "First User",
                "email": "duplicate@example.com",
                "role": "student"
            }
        )
        
        # Try to create second user with same email
        response = client.post(
            "/users/",
            json={
                "name": "Second User",
                "email": "duplicate@example.com",
                "role": "admin"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()


class TestUserRetrieval:
    """Test user retrieval endpoints"""
    
    def test_get_all_users_empty(self):
        """Test getting all users when database is empty"""
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_users(self):
        """Test getting all users"""
        # Create multiple users
        client.post(
            "/users/",
            json={
                "name": "User 1",
                "email": "user1@example.com",
                "role": "student"
            }
        )
        client.post(
            "/users/",
            json={
                "name": "User 2",
                "email": "user2@example.com",
                "role": "admin"
            }
        )
        
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "User 1"
        assert data[1]["name"] == "User 2"
    
    def test_get_user_by_id(self):
        """Test getting a user by ID"""
        # Create a user
        create_response = client.post(
            "/users/",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "role": "student"
            }
        )
        user_id = create_response.json()["id"]
        
        # Get the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
    
    def test_get_user_not_found(self):
        """Test getting a non-existent user"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUserValidation:
    """Test user validation edge cases"""
    
    def test_role_case_sensitive(self):
        """Test that role is case-sensitive"""
        response = client.post(
            "/users/",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "role": "Student"  # Capital S
            }
        )
        assert response.status_code == 422
    
    def test_valid_email_formats(self):
        """Test various valid email formats"""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user123@sub.example.org"
        ]
        
        for i, email in enumerate(valid_emails):
            response = client.post(
                "/users/",
                json={
                    "name": f"User {i}",
                    "email": email,
                    "role": "student"
                }
            )
            assert response.status_code == 201, f"Failed for email: {email}"
