from auth import get_current_user
from fastapi import APIRouter, Depends
from schemas import UserCreate, UserResponse, UserUpdate
import crud
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def get_users(current_user_id: int = Depends(get_current_user)):
    return crud.get_all_users()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return crud.get_user_by_id(user_id)


@router.post("/users", response_model=UserResponse)
def add_users(user: UserCreate):
    return crud.add_user(
        username=user.username,
        email=user.email,
        password=user.password
    )


@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    return crud.update_user(user_id, **user.model_dump(exclude_unset=True))


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return crud.delete_user(user_id)


@router.get("/me", response_model=UserResponse)
def get_me(current_user_id: int = Depends(get_current_user)):
    return crud.get_user_by_id(current_user_id)


@router.put("/me")
def update_me(user: UserUpdate, current_user_id: int = Depends(get_current_user)):
    return crud.update_user(current_user_id, **user.model_dump(exclude_unset=True))


@router.delete("/me")
def delete_me(current_user_id: int = Depends(get_current_user)):
    return crud.delete_user(current_user_id)
