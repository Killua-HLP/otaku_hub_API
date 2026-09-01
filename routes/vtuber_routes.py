import crud
from schemas import VtuberCreate, VtuberResponse, VtuberUpdate
from fastapi import APIRouter, Depends
import sys
import os
from auth import get_current_user


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter(prefix="", tags=["Vtuber"])


@router.get("/vtuber", response_model=list[VtuberResponse])
def get_all_vtuber(current_user_id: int = Depends(get_current_user)):
    return crud.get_all_vtubers(current_user_id)


@router.get("/vtuber/{vtuber_id}", response_model=VtuberResponse)
def get_vtuber_id(vtuber_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.get_vtuber_by_id(vtuber_id, current_user_id)


@router.post("/vtuber", response_model=VtuberResponse)
def add_vtuber(vtuber: VtuberCreate, current_user_id: int = Depends(get_current_user)):
    return crud.add_vtuber(
        user_id=current_user_id,
        name=vtuber.name,
        gender=vtuber.gender,
        agency=vtuber.agency,
        rank=vtuber.rank,
        debut_date=vtuber.debut_date,
        graduation_date=vtuber.graduation_date,
        is_favourite=vtuber.is_favourite,
        primary_language=vtuber.primary_language,
        youtube_id=vtuber.youtube_id,
        twitter=vtuber.twitter
    )


@router.put("/vtuber/{vtuber_id}")
def update_vtuber(vtuber_id: int, vtuber: VtuberUpdate, current_user_id: int = Depends(get_current_user)):
    return crud.update_vtuber(vtuber_id, **vtuber.model_dump(exclude_unset=True))


@router.delete("/vtuber/{vtuber_id}")
def delete_vtuber(vtuber_id: int, current_user_id: int = Depends(get_current_user)):
    return crud.delete_vtuber(vtuber_id)
