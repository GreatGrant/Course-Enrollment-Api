# Course Enrollment Management API - Project Summary

## Project Overview

A complete RESTful API built with FastAPI that manages a course enrollment system with role-based access control. This project demonstrates API development with comprehensive testing, validation, and documentation.

## Key Features

### Core Functionality
- **User Management**: Create and manage users with student/admin roles
- **Course Management**: Public course viewing with admin-only CRUD operations
- **Enrollment System**: Student self-enrollment with admin oversight capabilities
- **Role-Based Access Control**: Automatic enforcement of role-specific permissions

### Technical Features
- **59 Automated Tests**: Comprehensive test coverage for all endpoints
- **Data Validation**: Pydantic models with custom validators
- **In-Memory Storage**: Fast, lightweight data management
- **RESTful Design**: Proper HTTP methods and status codes
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc

## Project Structure

```
course_enrollment_api/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization
│   ├── models.py                 # Pydantic models with validation
│   ├── database.py               # In-memory data storage
│   └── routers/                  # API endpoints
│       ├── users.py              # User management
│       ├── courses.py            # Course management
│       └── enrollments.py        # Enrollment management
├── tests/                        # Comprehensive test suite
│   ├── test_users.py             # 18 user tests
│   ├── test_courses.py           # 20 course tests
│   └── test_enrollments.py       # 25+ enrollment tests
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── API_REFERENCE.md              # Complete API reference
├── TESTING.md                    # Testing documentation
├── ASSESSMENT.md                 # Project assessment checklist
├── setup.sh                      # Setup automation script
├── run_tests.sh                  # Test execution script
└── populate_sample_data.py       # Sample data generator
```

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### Run the API
```bash
uvicorn app.main:app --reload
```
Visit: http://127.0.0.1:8000/docs

### Run Tests
```bash
pytest -v
```

## Test Coverage

| Test Suite | Test Count | Coverage |
|------------|-----------|----------|
| User Management | 18 | 100% |
| Course Management | 20 | 100% |
| Enrollment Management | 25+ | 100% |
| **Total** | **63** | **100%** |

### Test Categories
- Endpoint functionality
- Role-based access control
- Data validation
- Error handling
- Edge cases
- Business rules

## API Endpoints

### User Management (3 endpoints)
- `POST /users/` - Create user
- `GET /users/` - List all users
- `GET /users/{id}` - Get user by ID

### Course Management (5 endpoints)
- `GET /courses/` - List all courses (public)
- `GET /courses/{id}` - Get course by ID (public)
- `POST /courses/` - Create course (admin only)
- `PUT /courses/{id}` - Update course (admin only)
- `DELETE /courses/{id}` - Delete course (admin only)

### Enrollment Management (6 endpoints)
- `POST /enrollments/` - Enroll student
- `DELETE /enrollments/{id}` - Deregister student
- `GET /enrollments/student/{id}` - Get student enrollments
- `GET /enrollments/` - Get all enrollments (admin)
- `GET /enrollments/course/{id}` - Get course enrollments (admin)
- `DELETE /enrollments/admin/{id}` - Force deregister (admin)

##  Role-Based Access Control

| Role | Permissions |
|------|------------|
| **Public** | View courses, view users, view student enrollments |
| **Student** | Enroll in courses, deregister from own courses |
| **Admin** | Create/update/delete courses, view all enrollments, force deregister students |

## Validation Rules

### User
- Name: Must not be empty
- Email: Valid email format, unique
- Role: Must be "student" or "admin" (case-sensitive)

### Course
- Title: Must not be empty
- Code: Must not be empty, unique across all courses

### Enrollment
- User must exist and be a student
- Course must exist
- No duplicate enrollments per student/course pair
- Students can only deregister their own enrollments

## Documentation

The project includes extensive documentation:

1. **README.md** - Project overview and setup instructions
2. **QUICKSTART.md** - Quick start guide with examples
3. **API_REFERENCE.md** - Complete endpoint documentation
4. **TESTING.md** - Testing guide and strategies
5. **ASSESSMENT.md** - Project assessment checklist

## Technologies Used

- **FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation using Python type hints
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server
- **HTTPx** - HTTP client for testing

## Getting Help

- Check `README.md` for setup instructions
- See `QUICKSTART.md` for quick examples
- Review `API_REFERENCE.md` for endpoint details
- Read `TESTING.md` for testing guidance
- Visit http://127.0.0.1:8000/docs for interactive documentation
