# Course Enrollment Management API

A RESTful API built with FastAPI for managing course enrollments with role-based access control.

## Features

- **User Management**: Create and retrieve users with role-based permissions
- **Course Management**: Public course viewing, admin-only course CRUD operations
- **Enrollment System**: Students can enroll/deregister, admins can oversee all enrollments
- **Role-Based Access**: Automatic role validation for protected operations
- **Complete Test Coverage**: Comprehensive test suite for all endpoints

## Project Structure

```
course_enrollment_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models and validation
│   ├── database.py          # In-memory data storage
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User management endpoints
│       ├── courses.py       # Course management endpoints
│       └── enrollments.py   # Enrollment management endpoints
├── tests/
│   ├── __init__.py
│   ├── test_users.py        # User endpoint tests
│   ├── test_courses.py      # Course endpoint tests
│   └── test_enrollments.py  # Enrollment endpoint tests
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pytest
- HTTPx

## Installation

1. **Clone or extract the project**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### Interactive API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app
```

Run specific test file:

```bash
pytest tests/test_users.py
```

## API Endpoints

### User Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/users/` | Create a new user | Public |
| GET | `/users/` | Get all users | Public |
| GET | `/users/{user_id}` | Get user by ID | Public |

### Course Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/courses/` | Get all courses | Public |
| GET | `/courses/{course_id}` | Get course by ID | Public |
| POST | `/courses/` | Create a new course | Admin only |
| PUT | `/courses/{course_id}` | Update a course | Admin only |
| DELETE | `/courses/{course_id}` | Delete a course | Admin only |

### Enrollment Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/enrollments/` | Enroll in a course | Student only |
| DELETE | `/enrollments/{enrollment_id}` | Deregister from course | Student only |
| GET | `/enrollments/student/{user_id}` | Get student's enrollments | Public |
| GET | `/enrollments/` | Get all enrollments | Admin only |
| GET | `/enrollments/course/{course_id}` | Get course enrollments | Admin only |
| DELETE | `/enrollments/admin/{enrollment_id}` | Force deregister student | Admin only |

## Example Usage

### Create a Student User

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }'
```

### Create a Course (Admin)

```bash
curl -X POST "http://127.0.0.1:8000/courses/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "code": "CS101",
    "admin_id": 1
  }'
```

### Enroll in a Course (Student)

```bash
curl -X POST "http://127.0.0.1:8000/enrollments/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "course_id": 1
  }'
```

## Validation Rules

### User
- `name`: Must not be empty
- `email`: Must be valid email format
- `role`: Must be either "student" or "admin"

### Course
- `title`: Must not be empty
- `code`: Must not be empty and must be unique

### Enrollment
- Students cannot enroll in the same course twice
- Both user and course must exist
- Only students can enroll/deregister
- Only admins can perform oversight operations

## Role-Based Access Control

The API enforces role-based restrictions:

- **Admin operations** require `admin_id` in request body
- **Student operations** require the user to have role "student"
- **Public operations** have no role restrictions

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET/PUT/DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Validation errors
- `403 Forbidden`: Role-based access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid input data

## Testing Strategy

The test suite covers:

1. **User Management**: Creation, retrieval, validation
2. **Course Management**: CRUD operations, role restrictions
3. **Enrollment Management**: Enrollment rules, student/admin operations
4. **Edge Cases**: Duplicate enrollments, non-existent resources
5. **Role Validation**: Admin vs student access control


## Development Notes

- Data is stored in-memory and resets on server restart
- IDs are auto-incremented integers
- Email validation uses regex pattern matching
- Role validation is case-sensitive ("student" or "admin")
