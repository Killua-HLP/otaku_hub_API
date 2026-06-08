from auth import get_current_user
from fastapi import APIRouter, Depends
from schemas import AnimeCreate, AnimeResponse, AnimeUpdate
import crud
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


@router.get("/anime_list", response_model=list[AnimeResponse])
def get_anime_list(current_user_id: int = Depends(get_current_user)):
    return crud.get_all_anime(current_user_id)


@router.get("/anime_list/{anime_id}", response_model=AnimeResponse)
def get_anime_id(anime_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.get_anime_by_id(anime_id, current_user_id)


@router.post("/anime_list", response_model=AnimeResponse)
def add_anime(anime: AnimeCreate, current_user_id: int = Depends(get_current_user)):
    return crud.add_anime(
        user_id=current_user_id,
        title=anime.title,
        genre=anime.genre,
        is_favourite=anime.is_favourite,
        episode_watched=anime.episode_watched,
        status=anime.status,
        rating=anime.rating,
        review=anime.review
    )


@router.put("/anime_list/{anime_id}")
def update_anime(anime_id: int, anime: AnimeUpdate, current_user_id: int = Depends(get_current_user)):
    return crud.update_anime(anime_id, **anime.model_dump(exclude_unset=True))


@router.delete("/anime_list/{anime_id}")
def delete_anime(anime_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.delete_anime(anime_id)
