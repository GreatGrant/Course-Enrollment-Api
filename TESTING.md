# Testing Documentation

## Overview

This project includes comprehensive automated tests covering all API endpoints and business logic. The test suite ensures that:

- All endpoints function correctly
- Role-based access control is enforced
- Data validation works as expected
- Edge cases are handled properly
- Error responses are appropriate

## Test Structure

```
tests/
├── __init__.py
├── test_users.py          # User management tests
├── test_courses.py        # Course management tests
└── test_enrollments.py    # Enrollment management tests
```

## Test Coverage

### User Management Tests (`test_users.py`)

**Test Classes:**
- `TestUserCreation`: User creation and validation
- `TestUserRetrieval`: Getting users and user lists
- `TestUserValidation`: Edge cases and validation rules

**Key Test Cases:**
-  Create student and admin users
-  Validate name is not empty
-  Validate email format
-  Validate role values (student/admin)
-  Prevent duplicate emails
-  Retrieve users by ID
-  List all users

### Course Management Tests (`test_courses.py`)

**Test Classes:**
- `TestCoursePublicAccess`: Public course viewing
- `TestCourseCreation`: Admin course creation
- `TestCourseUpdate`: Admin course updates
- `TestCourseDelete`: Admin course deletion
- `TestCourseValidation`: Edge cases and validation

**Key Test Cases:**
-  Public access to course lists and details
-  Admin-only course creation
-  Admin-only course updates
-  Admin-only course deletion
-  Students cannot perform admin operations
-  Course code uniqueness validation
-  Prevent empty titles and codes
-  Cascade delete enrollments when course is deleted

### Enrollment Management Tests (`test_enrollments.py`)

**Test Classes:**
- `TestStudentEnrollment`: Student enrollment functionality
- `TestStudentDeregistration`: Student deregistration
- `TestEnrollmentRetrieval`: Getting enrollment data
- `TestAdminEnrollmentOversight`: Admin oversight features
- `TestEnrollmentEdgeCases`: Complex scenarios

**Key Test Cases:**
-  Students can enroll in courses
-  Admins cannot enroll (student-only)
-  Prevent duplicate enrollments
-  Validate user and course exist
-  Students can deregister from courses
-  Students cannot deregister others
-  Admins can view all enrollments
-  Admins can force deregister students
-  Students cannot access admin features
-  Multiple students per course
-  Multiple courses per student

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with detailed output and show print statements
pytest -vv -s
```

### Run Specific Test Files

```bash
# Run only user tests
pytest tests/test_users.py

# Run only course tests
pytest tests/test_courses.py

# Run only enrollment tests
pytest tests/test_enrollments.py
```

### Run Specific Test Classes

```bash
# Run only user creation tests
pytest tests/test_users.py::TestUserCreation

# Run only enrollment tests
pytest tests/test_enrollments.py::TestStudentEnrollment
```

### Run Specific Test Cases

```bash
# Run a single test
pytest tests/test_users.py::TestUserCreation::test_create_student_user
```

### Coverage Reports

```bash
# Run with coverage
pytest --cov=app

# Generate HTML coverage report
pytest --cov=app --cov-report=html

# View HTML report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

## Test Fixtures

The test suite uses pytest fixtures for common setup:

### `reset_database`
- Automatically resets the in-memory database before each test
- Ensures test isolation
- Applied to all tests via `autouse=True`

### `admin_user`
- Creates an admin user for tests requiring admin privileges
- Returns the created user object with ID

### `student_user` / `student_user2`
- Creates student users for enrollment tests
- Returns the created user object with ID

### `sample_course` / `sample_course2`
- Creates courses for enrollment tests
- Requires admin_user fixture
- Returns the created course object with ID

## Test Patterns

### Role-Based Testing Pattern

```python
def test_admin_only_action(self, admin_user, student_user):
    # Verify admin can perform action
    response = client.post(..., json={"admin_id": admin_user["id"]})
    assert response.status_code == 201
    
    # Verify student cannot perform action
    response = client.post(..., json={"admin_id": student_user["id"]})
    assert response.status_code == 403
```

### Validation Testing Pattern

```python
def test_invalid_data(self):
    response = client.post(..., json={"field": "invalid"})
    assert response.status_code == 422  # Validation error
```

### Resource Lifecycle Pattern

```python
def test_resource_lifecycle(self):
    # Create
    create_response = client.post(...)
    assert create_response.status_code == 201
    resource_id = create_response.json()["id"]
    
    # Read
    get_response = client.get(f".../{resource_id}")
    assert get_response.status_code == 200
    
    # Update
    update_response = client.put(f".../{resource_id}", ...)
    assert update_response.status_code == 200
    
    # Delete
    delete_response = client.delete(f".../{resource_id}")
    assert delete_response.status_code == 200
```

## Expected Test Results

When all tests pass, you should see output like:

```
tests/test_users.py::TestUserCreation::test_create_student_user PASSED
tests/test_users.py::TestUserCreation::test_create_admin_user PASSED
tests/test_users.py::TestUserCreation::test_create_user_empty_name PASSED
...
tests/test_courses.py::TestCoursePublicAccess::test_get_all_courses PASSED
...
tests/test_enrollments.py::TestStudentEnrollment::test_enroll_student_in_course PASSED
...

============================================ XX passed in X.XXs ============================================
```

## Continuous Integration

This test suite is designed to be CI/CD friendly:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: pip install -r requirements.txt

- name: Run tests
  run: pytest --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Writing New Tests

When adding new features, follow these guidelines:

1. **Test file naming**: `test_<feature>.py`
2. **Test class naming**: `Test<FeatureName>`
3. **Test method naming**: `test_<what_it_tests>`
4. **Use fixtures**: Leverage existing fixtures for common setup
5. **Test both success and failure**: Test valid and invalid cases
6. **Test role permissions**: Verify role-based access control
7. **Use descriptive assertions**: Make it clear what went wrong

### Example New Test

```python
def test_new_feature(self, student_user, sample_course):
    """Test description of what this tests"""
    # Arrange
    data = {"user_id": student_user["id"], "course_id": sample_course["id"]}
    
    # Act
    response = client.post("/new-endpoint/", json=data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["some_field"] == "expected_value"
```

## Troubleshooting Tests

### Tests Failing Randomly

- Check if database is being reset properly
- Ensure tests don't depend on execution order
- Look for shared state issues

### Import Errors

```bash
# Make sure you're in the project root
cd /path/to/course_enrollment_api

# Install in development mode
pip install -e .
```

### Fixture Not Found

- Check fixture is defined in the same file or conftest.py
- Verify fixture name matches parameter name
- Ensure fixture scope is appropriate

## Test Metrics

Target metrics for this project:
- **Coverage**: 95%+ line coverage
- **Test Count**: 60+ test cases
- **Execution Time**: <5 seconds for full suite
- **Pass Rate**: 100% (all tests must pass)