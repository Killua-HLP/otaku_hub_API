from auth import get_current_user
from fastapi import APIRouter, Depends
from schemas import GameCreate, GameResponse, GameUpdate
import crud
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


@router.get("/game", response_model=list[GameResponse])
def get_all_game(current_user_id: int = Depends(get_current_user)):
    return crud.get_all_games(current_user_id)


@router.get("/game/{game_id}", response_model=GameResponse)
def get_game_id(game_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.get_game_by_id(game_id, current_user_id)


@router.post("/game", response_model=GameResponse)
def add_game(game: GameCreate, current_user_id: int = Depends(get_current_user)):
    return crud.add_game(
        user_id=current_user_id,
        title=game.title,
        genre=game.genre,
        rank=game.rank,
        hour_played=game.hour_played,
        started_date=game.started_date,
        finished_date=game.finished_date,
        rating=game.rating,
        notes=game.notes
    )


@router.put("/game/{game_id}")
def update_game(game_id: int, game: GameUpdate, current_user_id: int = Depends(get_current_user)):
    return crud.update_game(game_id, **game.model_dump(exclude_unset=True))


@router.delete("/game/{game_id}")
def delete_game(game_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.delete_game(game_id)
