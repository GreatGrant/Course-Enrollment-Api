from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import User, UserCreate
from app.database import db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Create a new user.
    
    Validation:
    - name must not be empty
    - email must be valid email format
    - role must be either 'student' or 'admin'
    """
    # Check if email already exists
    if db.email_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = db.create_user(
        name=user.name,
        email=user.email,
        role=user.role
    )
    return new_user


@router.get("/", response_model=List[User])
def get_all_users():
    """
    Retrieve all users.
    """
    return db.get_all_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """
    Retrieve a user by ID.
    """
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
