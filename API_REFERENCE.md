# API Reference

Complete reference for all Course Enrollment Management API endpoints.

## Base URL

```
http://127.0.0.1:8000
```

## Response Formats

All responses are in JSON format.

### Success Response

```json
{
  "id": 1,
  "field": "value"
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

---

## User Endpoints

### Create User

Create a new user account.

**Endpoint:** `POST /users/`

**Access:** Public

**Request Body:**
```json
{
  "name": "string",
  "email": "string (email format)",
  "role": "student" | "admin"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student"
}
```

**Validation Rules:**
- `name`: Must not be empty or whitespace
- `email`: Must be valid email format
- `role`: Must be exactly "student" or "admin" (case-sensitive)
- `email`: Must be unique (not already registered)

**Error Responses:**
- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Validation error

---

### Get All Users

Retrieve a list of all users.

**Endpoint:** `GET /users/`

**Access:** Public

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  },
  {
    "id": 2,
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  }
]
```

---

### Get User by ID

Retrieve a specific user by their ID.

**Endpoint:** `GET /users/{user_id}`

**Access:** Public

**Path Parameters:**
- `user_id` (integer): User ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student"
}
```

**Error Responses:**
- `404 Not Found`: User not found

---

## Course Endpoints

### Get All Courses

Retrieve a list of all courses.

**Endpoint:** `GET /courses/`

**Access:** Public

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "code": "CS101"
  },
  {
    "id": 2,
    "title": "Data Structures",
    "code": "CS201"
  }
]
```

---

### Get Course by ID

Retrieve a specific course by its ID.

**Endpoint:** `GET /courses/{course_id}`

**Access:** Public

**Path Parameters:**
- `course_id` (integer): Course ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "code": "CS101"
}
```

**Error Responses:**
- `404 Not Found`: Course not found

---

### Create Course

Create a new course (admin only).

**Endpoint:** `POST /courses/`

**Access:** Admin only

**Request Body:**
```json
{
  "title": "string",
  "code": "string",
  "admin_id": 1
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "code": "CS101"
}
```

**Validation Rules:**
- `title`: Must not be empty or whitespace
- `code`: Must not be empty or whitespace
- `code`: Must be unique across all courses
- `admin_id`: Must reference an existing user with role "admin"

**Error Responses:**
- `400 Bad Request`: Course code already exists
- `403 Forbidden`: User is not an admin
- `404 Not Found`: Admin user not found
- `422 Unprocessable Entity`: Validation error

---

### Update Course

Update an existing course (admin only).

**Endpoint:** `PUT /courses/{course_id}`

**Access:** Admin only

**Path Parameters:**
- `course_id` (integer): Course ID

**Request Body:**
```json
{
  "title": "string",
  "code": "string",
  "admin_id": 1
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Advanced Python",
  "code": "CS101A"
}
```

**Validation Rules:**
- Same as Create Course
- `code`: Must be unique except for the course being updated

**Error Responses:**
- `400 Bad Request`: Course code already exists
- `403 Forbidden`: User is not an admin
- `404 Not Found`: Course or admin user not found
- `422 Unprocessable Entity`: Validation error

---

### Delete Course

Delete a course (admin only).

**Endpoint:** `DELETE /courses/{course_id}`

**Access:** Admin only

**Path Parameters:**
- `course_id` (integer): Course ID

**Request Body:**
```json
{
  "admin_id": 1
}
```

**Response:** `200 OK`
```json
{
  "detail": "Course deleted successfully"
}
```

**Side Effects:**
- All enrollments for this course are also deleted

**Error Responses:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: Course or admin user not found

---

## Enrollment Endpoints

### Enroll Student

Enroll a student in a course.

**Endpoint:** `POST /enrollments/`

**Access:** Student only

**Request Body:**
```json
{
  "user_id": 1,
  "course_id": 1
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": 1,
  "course_id": 1
}
```

**Business Rules:**
- Only users with role "student" can enroll
- A student cannot enroll in the same course twice
- Both user and course must exist

**Error Responses:**
- `400 Bad Request`: Student already enrolled in course
- `403 Forbidden`: User is not a student
- `404 Not Found`: User or course not found
- `422 Unprocessable Entity`: Validation error

---

### Deregister Student

Deregister a student from a course.

**Endpoint:** `DELETE /enrollments/{enrollment_id}`

**Access:** Student only (own enrollments)

**Path Parameters:**
- `enrollment_id` (integer): Enrollment ID

**Query Parameters:**
- `user_id` (integer): Student user ID

**Example:**
```
DELETE /enrollments/1?user_id=1
```

**Response:** `200 OK`
```json
{
  "detail": "Successfully deregistered from course"
}
```

**Business Rules:**
- Only students can deregister
- Students can only deregister their own enrollments
- Enrollment must exist

**Error Responses:**
- `403 Forbidden`: User is not a student or trying to deregister another student
- `404 Not Found`: Enrollment or user not found

---

### Get Student Enrollments

Retrieve all enrollments for a specific student.

**Endpoint:** `GET /enrollments/student/{user_id}`

**Access:** Public

**Path Parameters:**
- `user_id` (integer): Student user ID

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "course_id": 1
  },
  {
    "id": 2,
    "user_id": 1,
    "course_id": 2
  }
]
```

**Error Responses:**
- `404 Not Found`: User not found

---

### Get All Enrollments

Retrieve all enrollments in the system (admin only).

**Endpoint:** `GET /enrollments/`

**Access:** Admin only

**Query Parameters:**
- `admin_id` (integer): Admin user ID

**Example:**
```
GET /enrollments/?admin_id=1
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "course_id": 1
  },
  {
    "id": 2,
    "user_id": 2,
    "course_id": 1
  }
]
```

**Error Responses:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: Admin user not found

---

### Get Course Enrollments

Retrieve all enrollments for a specific course (admin only).

**Endpoint:** `GET /enrollments/course/{course_id}`

**Access:** Admin only

**Path Parameters:**
- `course_id` (integer): Course ID

**Query Parameters:**
- `admin_id` (integer): Admin user ID

**Example:**
```
GET /enrollments/course/1?admin_id=1
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "course_id": 1
  },
  {
    "id": 2,
    "user_id": 2,
    "course_id": 1
  }
]
```

**Error Responses:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: Course or admin user not found

---

### Admin Force Deregister

Force deregister any student from a course (admin only).

**Endpoint:** `DELETE /enrollments/admin/{enrollment_id}`

**Access:** Admin only

**Path Parameters:**
- `enrollment_id` (integer): Enrollment ID

**Request Body:**
```json
{
  "admin_id": 1
}
```

**Response:** `200 OK`
```json
{
  "detail": "Student successfully deregistered by admin"
}
```

**Error Responses:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: Enrollment or admin user not found

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Business rule violation |
| 403 | Forbidden | Role-based access denied |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |

---

## Common Error Patterns

### Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Access Denied (403)

```json
{
  "detail": "Only admins can perform this action"
}
```

### Not Found (404)

```json
{
  "detail": "User not found"
}
```

### Business Rule Violation (400)

```json
{
  "detail": "Student is already enrolled in this course"
}
```

---

## Role-Based Access Summary

| Endpoint | Public | Student | Admin |
|----------|--------|---------|-------|
| POST /users/ | ✓ | ✓ | ✓ |
| GET /users/ | ✓ | ✓ | ✓ |
| GET /users/{id} | ✓ | ✓ | ✓ |
| GET /courses/ | ✓ | ✓ | ✓ |
| GET /courses/{id} | ✓ | ✓ | ✓ |
| POST /courses/ | ✗ | ✗ | ✓ |
| PUT /courses/{id} | ✗ | ✗ | ✓ |
| DELETE /courses/{id} | ✗ | ✗ | ✓ |
| POST /enrollments/ | ✗ | ✓ | ✗ |
| DELETE /enrollments/{id} | ✗ | ✓* | ✗ |
| GET /enrollments/student/{id} | ✓ | ✓ | ✓ |
| GET /enrollments/ | ✗ | ✗ | ✓ |
| GET /enrollments/course/{id} | ✗ | ✗ | ✓ |
| DELETE /enrollments/admin/{id} | ✗ | ✗ | ✓ |

*Students can only deregister their own enrollments

---

## Postman Collection

Import this collection into Postman for easy testing:

[Collection URL would go here in a real project]

Alternatively, use the interactive Swagger UI at http://127.0.0.1:8000/docs
