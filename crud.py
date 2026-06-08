import bcrypt
from database import get_session
from models import User, AnimeList, MangaList, Vtuber, Game
from fastapi import HTTPException
from auth import pwd_context

# USER CRUD


def add_user(username, email, password, bio=None, country=None, favourite_genre=None):
    password = password[:72]
    hashed = pwd_context.hash(password)
    with get_session() as session:
        existing = session.query(User).filter(
            User.username == username).first()
        if existing:
            raise HTTPException(
                status_code=400, detail=f"Username '{username}' already exists!")

        existing_email = session.query(User).filter(
            User.email == email).first()
        if existing_email:
            raise HTTPException(
                status_code=400, detail=f"Email '{email}' already exists!")
        new_user = User(
            username=username,
            email=email,
            password=hashed,
            bio=bio,
            country=country,
            favourite_genre=favourite_genre
        )
        session.add(new_user)
        session.flush()
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "bio": new_user.bio,
            "country": new_user.country,
            "favourite_genre": new_user.favourite_genre,
            "is_active": new_user.is_active
        }


def get_all_users():
    with get_session() as session:
        users = session.query(User).all()
        return [{"id": u.id,
                 "username": u.username,
                 "email": u.email,
                 "password": u.password,
                 "bio": u.bio,
                 "country": u.country,
                 "favourite_genre": u.favourite_genre,
                 "is_active": u.is_active}
                for u in users
                ]


def get_user_by_id(user_id):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return {"id": user.id,
                "username": user.username,
                "email": user.email,
                "bio": user.bio,
                "country": user.country,
                "favourite_genre": user.favourite_genre,
                "is_active": user.is_active}


def update_user(user_id, **kwargs):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User ID {user_id} not found!")
        for key, value in kwargs.items():
            setattr(user, key, value)
        return {"message": f"User {user_id} updated successfully"}


def delete_user(user_id):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User ID {user_id} not found!")
        session.delete(user)
        return {"message": f"User {user_id} deleted successfully"}

# ANIME CRUD


def add_anime(user_id, title, genre, is_favourite, episode_watched, status, rating, review):
    with get_session() as session:
        existing = session.query(AnimeList).filter(
            AnimeList.title == title,
            AnimeList.user_id == user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, detail=f"Anime '{title}' already exists!")

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
        session.flush()
        return {
            "id": new_anime.id,
            "user_id": new_anime.user_id,
            "title": new_anime.title,
            "genre": new_anime.genre,
            "is_favourite": new_anime.is_favourite,
            "episode_watched": new_anime.episode_watched,
            "status": new_anime.status,
            "rating": new_anime.rating,
            "review": new_anime.review
        }


def get_all_anime(user_id: int):
    with get_session() as session:
        animes = session.query(AnimeList).filter(
            AnimeList.user_id == user_id).all()
        return [
            {
                "id": a.id,
                "user_id": a.user_id,
                "title": a.title,
                "genre": a.genre,
                "is_favourite": a.is_favourite,
                "episode_watched": a.episode_watched,
                "status": a.status,
                "rating": a.rating,
                "review": a.review
            } for a in animes
        ]


def get_anime_by_id(anime_id: int, user_id: int):
    with get_session() as session:
        anime = session.query(AnimeList).filter(
            AnimeList.id == anime_id,
            AnimeList.user_id == user_id).first()
        if not anime:
            raise HTTPException(status_code=404, detail="Anime not found!")
        return {"id": anime.id,
                "title": anime.title,
                "rating": anime.rating}


def update_anime(anime_id, **kwargs):
    with get_session() as session:
        anime = session.query(AnimeList).filter(
            AnimeList.id == anime_id).first()
        if not anime:
            raise HTTPException(
                status_code=404, detail=f"Anime {anime_id} not found!")
        for key, value in kwargs.items():
            setattr(anime, key, value)
        return {"message": f"Anime {anime_id} updated successfully!"}


def delete_anime(anime_id):
    with get_session() as session:
        anime = session.query(AnimeList).filter(
            AnimeList.id == anime_id).first()
        if not anime:
            raise HTTPException(
                status_code=404, detail=f"Anime {anime_id} not found!")
        session.delete(anime)
        return {"message": f"Anime {anime_id} deleted successfully!"}

# MANGA CRUD


def add_manga(user_id, title, genre, is_favourite, chapter_read, status, rating, review):
    with get_session() as session:
        existing = session.query(MangaList).filter(
            MangaList.title == title,
            MangaList.user_id == user_id).first()
        if existing:
            raise HTTPException(
                status_code=400, detail=f"Manga '{title}' already exists!")

        new_manga = MangaList(
            user_id=user_id,
            title=title,
            genre=genre,
            is_favourite=is_favourite,
            chapter_read=chapter_read,
            status=status,
            rating=rating,
            review=review
        )
        session.add(new_manga)
        session.flush()
        return {
            "id": new_manga.id,
            "user_id": new_manga.user_id,
            "title": new_manga.title,
            "genre": new_manga.genre,
            "is_favourite": new_manga.is_favourite,
            "chapter_read": new_manga.chapter_read,
            "status": new_manga.status,
            "rating": new_manga.rating,
            "review": new_manga.review
        }


def get_all_manga(user_id: int):
    with get_session() as session:
        manga = session.query(MangaList).filter(
            MangaList.user_id == user_id).all()
        return [
            {
                "id": m.id,
                "user_id": m.user_id,
                "title": m.title,
                "chapters": m.chapter_read,
                "status": m.status,
                "rating": m.rating
            } for m in manga
        ]


def get_manga_by_id(manga_id: int, user_id: int):
    with get_session() as session:
        manga = session.query(MangaList).filter(
            MangaList.id == manga_id,
            MangaList.user_id == user_id).first()
        if not manga:
            raise HTTPException(status_code=404, detail="Manga not found!")
        return {
            "id": manga.id,
            "title": manga.title,
            "genre": manga.genre,
            "rating": manga.rating
        }


def update_manga(manga_id, **kwargs):
    with get_session() as session:
        manga = session.query(MangaList).filter(
            MangaList.id == manga_id).first()
        if not manga:
            raise HTTPException(
                status_code=404, detail=f"Manga {manga_id} not found!")
        for key, value in kwargs.items():
            setattr(manga, key, value)
        return {"message": f"Manga {manga_id} updated successfully!"}


def delete_manga(manga_id):
    with get_session() as session:
        manga = session.query(MangaList).filter(
            MangaList.id == manga_id).first()
        if not manga:
            raise HTTPException(
                status_code=404, detail=f"Manga {manga_id} not found!")
        session.delete(manga)
        return {"message": f"Manga {manga_id} deleted successfully!"}

# VTUBER CRUD


def add_vtuber(user_id, name, gender, agency, rank, debut_date, graduation_date, is_favourite, primary_language, youtube_id, twitter):
    with get_session() as session:
        existing = session.query(Vtuber).filter(
            Vtuber.name == name,
            Vtuber.user_id == user_id).first()
        if existing:
            raise HTTPException(
                status_code=400, detail=f"Vtuber '{name}' already exists!")
        new_vtuber = Vtuber(
            user_id=user_id,
            name=name,
            gender=gender,
            agency=agency,
            rank=rank,
            debut_date=debut_date,
            graduation_date=graduation_date,
            is_favourite=is_favourite,
            primary_language=primary_language,
            youtube_id=youtube_id,
            twitter=twitter
        )
        session.add(new_vtuber)
        session.flush()
        return {
            "id": new_vtuber.id,
            "user_id": new_vtuber.user_id,
            "name": new_vtuber.name,
            "gender": new_vtuber.gender,
            "agency": new_vtuber.agency,
            "rank": new_vtuber.rank,
            "debut_date": new_vtuber.debut_date,
            "graduation_date": new_vtuber.graduation_date,
            "is_favourite": new_vtuber.is_favourite,
            "primary_language": new_vtuber.primary_language,
            "youtube_id": new_vtuber.youtube_id,
            "twitter": new_vtuber.twitter
        }


def get_all_vtubers(user_id: int):
    with get_session() as session:
        vtubers = session.query(Vtuber).filter(
            Vtuber.user_id == user_id).all()
        return [{"id": v.id,
                 "title": v.name,
                 "agency": v.agency,
                 "rank": v.rank}
                for v in vtubers
                ]


def get_vtuber_by_id(vtuber_id: int, user_id: int):
    with get_session() as session:
        vtuber = session.query(Vtuber).filter(
            Vtuber.id == vtuber_id,
            Vtuber.user_id == user_id).first()
        if not vtuber:
            raise HTTPException(status_code=404, detail="Vtuber not found!")
        return {
            "id": vtuber.id,
            "name": vtuber.name,
            "gender": vtuber.gender,
            "agency": vtuber.agency
        }


def update_vtuber(vtuber_id, **kwargs):
    with get_session() as session:
        vtuber = session.query(Vtuber).filter(Vtuber.id == vtuber_id).first()
        if not vtuber:
            raise HTTPException(
                status_code=404, detail=f"Vtuber {vtuber_id} not found!")
        for key, value in kwargs.items():
            setattr(vtuber, key, value)
        return {"message": f"Vtuber {vtuber_id} updated successfully!"}


def delete_vtuber(vtuber_id):
    with get_session() as session:
        vtuber = session.query(Vtuber).filter(Vtuber.id == vtuber_id).first()
        if not vtuber:
            raise HTTPException(
                status_code=404, detail=f"Vtuber {vtuber_id} not found!")
        session.delete(vtuber)
        return {"message": f"Vtuber {vtuber_id} deleted successfully!"}

# GAME CRUD


def add_game(user_id, title, genre, rank, hour_played, started_date, finished_date, rating, notes):
    with get_session() as session:
        existing = session.query(Game).filter(
            Game.title == title,
            Game.user_id == user_id).first()
        if existing:
            raise HTTPException(
                status_code=400, detail=f"Game '{title}' already exists!")
        new_game = Game(
            user_id=user_id,
            title=title,
            genre=genre,
            rank=rank,
            hour_played=hour_played,
            started_date=started_date,
            finished_date=finished_date,
            rating=rating,
            notes=notes
        )
        session.add(new_game)
        session.flush()
        return {
            "id": new_game.id,
            "user_id": new_game.user_id,
            "title": new_game.title,
            "genre": new_game.genre,
            "rank": new_game.rank,
            "hour_played": float(str(new_game.hour_played)),
            "started_date": new_game.started_date,
            "finished_date": new_game.finished_date,
            "rating": new_game.rating,
            "notes": new_game.notes
        }


def get_all_games(user_id: int):
    with get_session() as session:
        games = session.query(Game).filter(
            Game.user_id == user_id).all()
        return [{
                "id": g.id,
                "title": g.title,
                "hour_play": float(str(g.hour_played)),
                "rating": g.rating
                }for g in games
                ]


def get_game_by_id(game_id: int, user_id: int):
    with get_session() as session:
        game = session.query(Game).filter(
            Game.id == game_id,
            Game.user_id == user_id).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found!")
        return {
            "id": game.id,
            "title": game.title,
            "genre": game.genre,
            "rating": game.rating
        }


def update_game(game_id, **kwargs):
    with get_session() as session:
        game = session.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(
                status_code=404, detail=f"Game {game_id} not found!")
        for key, value in kwargs.items():
            setattr(game, key, value)
        return {"message": f"Game {game_id} updated successfully!"}


def delete_game(game_id):
    with get_session() as session:
        game = session.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(
                status_code=404, detail=f"Game {game_id} not found!")
        session.delete(game)
        return {"message": f"Game {game_id} deleted successfully!"}
