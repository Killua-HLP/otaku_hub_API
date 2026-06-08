from database import Base
from sqlalchemy import (
    Column, Integer, Boolean, String, Float, Text, Date, TIMESTAMP,
    Numeric, SmallInteger, CheckConstraint, ForeignKey
)
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    profile_picture = Column(String(255))
    bio = Column(Text)
    favourite_genre = Column(String(100))
    country = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())


class AnimeList(Base):
    __tablename__ = "anime_list"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    genre = Column(String(200))
    is_favourite = Column(Boolean, default=True)
    episode_watched = Column(Integer, default=0)
    status = Column(String(100))
    rating = Column(Float)
    review = Column(Text)


class MangaList(Base):
    __tablename__ = "manga_list"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    genre = Column(String(200))
    is_favourite = Column(Boolean, default=True)
    chapter_read = Column(Integer, default=0)
    status = Column(String(100))
    rating = Column(Float)
    review = Column(Text)


class Vtuber(Base):
    __tablename__ = "vtuber"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(200))
    gender = Column(String(200))
    agency = Column(String(200))
    rank = Column(Integer)
    debut_date = Column(Date)
    graduation_date = Column(Date)
    is_favourite = Column(Boolean, default=True)
    primary_language = Column(String(10))
    youtube_id = Column(String(50))
    twitter = Column(String(50))


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    genre = Column(String(200))
    rank = Column(Integer)
    hour_played = Column(Numeric(6, 1))
    started_date = Column(Date)
    finished_date = Column(Date)
    rating = Column(SmallInteger, CheckConstraint("rating BETWEEN 1 AND 10"))
    notes = Column(Text)
