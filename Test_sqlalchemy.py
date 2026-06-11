import os
from contextlib import contextmanager
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import (
    Column, Integer, Boolean, String, Float, Text, Date, TIMESTAMP,
    Numeric, SmallInteger, CheckConstraint, ForeignKey, create_engine, inspect
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import func

load_dotenv()
DB_URL = os.getenv(
    "DB_URL", "fpostgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
if not os.getenv("DB_URL"):
    print("Environment variable 'DB_URL' not found in .env, using default fallback.")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), unique=True, nullable=False)
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
    title = Column(String(200))
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


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db(force_recreate=False):
    """Initializes the database tables. Set force_recreate=True to fix structure mismatches."""
    if force_recreate:
        print("Dropping old tables to sync structure changes...")
        Base.metadata.drop_all(engine)

    print("Models defined in SQLAlchemy Base:")
    for table in Base.metadata.tables:
        print(f"  - {table}")

    Base.metadata.create_all(engine)
    print("Database tables created successfully.")


def print_current_db_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Actual tables present in the database:", tables)


def add_user(username, email, password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    with get_session() as session:
        new_user = User(
            user_name=username,
            email=email,
            password=hashed.decode("utf-8")
        )
        session.add(new_user)
    print(f"Successfully added user: {username}")


def get_all_user():
    with get_session() as session:
        users = session.query(User).all()
        for user in users:
            print(user.user_name, user.email)


def get_user_by_id(user_id):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            print(f"User ID {user_id} not found!")
            return
        print(user.user_name)


def update_user(user_id, new_email):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            print(f"User ID {user_id} not found!")
            return
        user.email = new_email
        print(f"Successfully changed email for User ID {user_id}")


def delete_user(user_id):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            print(f"User ID {user_id} not found!")
            return
        session.delete(user)
        print(f"Successfully deleted User ID: {user_id}")


def add_anime(user_id, title, genre, is_favourite, episode_watched, status, rating, review):
    with get_session() as session:
        new_anime = AnimeList(
            user_id=user_id,
            title=title,
            genre=genre,
            is_favourite=is_favourite,
            episode_watched=episode_watched,
            status=status,
            rating=rating,
            review=review
        )
        session.add(new_anime)


def get_all_anime():
    with get_session() as session:
        animes = session.query(AnimeList).all()
        for anime in animes:
            print(anime.user_id, anime.title, anime.genre, anime.is_favourite,
                  anime.episode_watched, anime.rating, anime.review)


def get_anime_by_id(anime_id):
    with get_session() as session:
        anime = session.query(AnimeList).filter(
            AnimeList.id == anime_id).first()
        if anime is None:
            print(f"Anime ID: {anime_id} not found!")
            return
        print(anime.title)


def update_anime(anime_id, **kwargs):
    with get_session() as session:
        anime = session.query(AnimeList).filter(
            AnimeList.id == anime_id).first()
        if anime is None:
            print(f"Anime ID: {anime_id} not found!")
            return
        for key, value in kwargs.items():
            setattr(anime, key, value)
        print("Successfully changed anime details")


def delete_anime(anime_id):
    with get_session() as session:
        anime = session.query(AnimeList).filter(
            AnimeList.id == anime_id).first()
        if anime is None:
            print(f"Anime ID: {anime_id} not found!")
            return
        session.delete(anime)


if __name__ == "__main__":
    init_db(force_recreate=False)

    try:
        add_user("killua", "killua@gmail.com", "pass123")
    except Exception:
        print("User 'killua' already exists, moving on...")

    print("\nAttempting to add anime...")
    add_anime(
        user_id=1,
        title="Hunter x Hunter (2011)",
        genre="Action, Shonen",
        is_favourite=True,
        episode_watched=148,
        status="Completed",
        rating=10.0,
        review="The Chimera Ant arc is a masterpiece."
    )
    print("\n--- Current Anime List ---")
    get_all_anime()
