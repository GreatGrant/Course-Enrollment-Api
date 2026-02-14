from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Literal


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Literal["student", "admin"]

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    title: str
    code: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v

    @field_validator("code")
    @classmethod
    def code_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("code must not be empty")
        return v


class CourseCreate(CourseBase):
    admin_id: int  # ID of the admin creating the course


class CourseUpdate(CourseBase):
    admin_id: int  # ID of the admin updating the course


class Course(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CourseDelete(BaseModel):
    admin_id: int  # ID of the admin deleting the course


class EnrollmentDelete(BaseModel):
    admin_id: int  # ID of the admin forcing deregistration
