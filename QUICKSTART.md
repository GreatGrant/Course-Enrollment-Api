# Quick Start Guide

## Installation

### Option 1: Using the setup script (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
uvicorn app.main:app --reload
```

The API will be available at: http://127.0.0.1:8000

## Running Tests

### Option 1: Using the test runner script

```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Option 2: Manual test execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py
pytest tests/test_courses.py
pytest tests/test_enrollments.py
```

## Example API Usage

### 1. Create Users

```bash
# Create an admin user
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  }'

# Create a student user
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }'
```

### 2. Create Course (Admin Only)

```bash
curl -X POST "http://127.0.0.1:8000/courses/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "code": "CS101",
    "admin_id": 1
  }'
```

### 3. Enroll Student in Course

```bash
curl -X POST "http://127.0.0.1:8000/enrollments/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "course_id": 1
  }'
```

### 4. View Enrollments

```bash
# Get all courses (public)
curl http://127.0.0.1:8000/courses/

# Get student's enrollments
curl http://127.0.0.1:8000/enrollments/student/2

# Get all enrollments (admin only)
curl "http://127.0.0.1:8000/enrollments/?admin_id=1"
```

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

These provide interactive documentation where you can test all endpoints directly from your browser.

## Common Issues

### Import Errors

Make sure the virtual environment is activated:
```bash
source venv/bin/activate
```

### Port Already in Use

If port 8000 is already in use, specify a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Tests Not Found

Make sure you're in the project root directory and pytest is installed:
```bash
pip install pytest httpx
```
