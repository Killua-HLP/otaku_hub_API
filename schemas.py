from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    country: Optional[str] = None
    favourite_genre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    country: Optional[str] = None
    favourite_genre: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class AnimeUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    is_favourite: Optional[bool] = None
    episode_watched: Optional[int] = None
    status: Optional[str] = None
    rating: Optional[float] = None
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AnimeCreate(BaseModel):
    title: str
    genre: str
    is_favourite: bool
    episode_watched: int
    status: str
    rating: float
    review: str

    model_config = ConfigDict(from_attributes=True)


class AnimeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    genre: str
    is_favourite: bool
    episode_watched: int
    status: str
    rating: Optional[float] = None
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MangaUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    is_favourite: Optional[bool] = None
    chapter_read: Optional[int] = None
    status: Optional[str] = None
    rating: Optional[float] = None
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MangaCreate(BaseModel):
    title: str
    genre: str
    is_favourite: bool
    chapter_read: int
    status: str
    rating: Optional[float] = None
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MangaResponse(BaseModel):
    id: int
    user_id: int
    title: str
    genre: str
    is_favourite: bool
    chapter_read: int
    status: str
    rating: Optional[float] = None
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VtuberUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    agency: Optional[str] = None
    rank: Optional[int] = None
    debut_date: Optional[date] = None
    graduation_date: Optional[date] = None
    is_favourite: Optional[bool] = None
    primary_language: Optional[str] = None
    youtube_id: Optional[str] = None
    twitter: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VtuberCreate(BaseModel):
    name: str
    gender: str
    agency: str
    rank: Optional[int] = None
    debut_date: Optional[date] = None
    graduation_date: Optional[date] = None
    is_favourite: bool
    primary_language: str
    youtube_id: Optional[str] = None
    twitter: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VtuberResponse(BaseModel):
    id: int
    user_id: int
    name: str
    gender: str
    agency: str
    rank: Optional[int] = None
    debut_date: Optional[date] = None
    graduation_date: Optional[date] = None
    is_favourite: bool
    primary_language: str
    youtube_id: Optional[str] = None
    twitter: Optional[str] = None


class GameUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    rank: Optional[int] = None
    hour_played: Optional[float] = None
    started_date: Optional[date] = None
    finished_date: Optional[date] = None
    rating: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GameCreate(BaseModel):
    title: str
    genre: str
    rank: Optional[int] = None
    hour_played: Optional[float] = None
    started_date: Optional[date] = None
    finished_date: Optional[date] = None
    rating: float

    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GameResponse(BaseModel):
    id: int
    user_id: int
    title: str
    genre: str
    rank: Optional[int] = None
    hour_played: Optional[float] = None
    started_date: Optional[date] = None
    finished_date: Optional[date] = None
    rating: float
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str
