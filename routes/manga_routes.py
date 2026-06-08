from auth import get_current_user
from fastapi import APIRouter, Depends
from schemas import MangaCreate, MangaResponse, MangaUpdate
import crud
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


@router.get("/manga_list", response_model=list[MangaResponse])
def get_all_manga(current_user_id: int = Depends(get_current_user)):
    return crud.get_all_manga(current_user_id)


@router.get("/manga_list/{manga_id}", response_model=MangaResponse)
def get_manga_id(manga_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.get_manga_by_id(manga_id, current_user_id)


@router.post("/manga_list", response_model=MangaResponse)
def add_manga(manga: MangaCreate, current_user_id: int = Depends(get_current_user)):
    return crud.add_manga(
        user_id=current_user_id,
        title=manga.title,
        genre=manga.genre,
        is_favourite=manga.is_favourite,
        chapter_read=manga.chapter_read,
        status=manga.status,
        rating=manga.rating,
        review=manga.review
    )


@router.put("/manga_list/{manga_id}")
def update_manga(manga_id: int, manga: MangaUpdate, current_user_id: int = Depends(get_current_user)):
    return crud.update_manga(manga_id, **manga.model_dump(exclude_unset=True))


@router.delete("/manga_list/{manga_id}")
def delete_manga(manga_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.delete_manga(manga_id)
