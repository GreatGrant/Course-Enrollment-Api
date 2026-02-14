from fastapi import FastAPI
from app.routers import users, courses, enrollments

app = FastAPI(
    title="Course Enrollment Management API",
    description="A RESTful API for managing course enrollments with role-based access control",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/")
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Course Enrollment Management API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
