import os
import sys
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
DB_URL = os.getenv(
    f"DB_URL", "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
if not os.getenv("DB_URL"):
    print("Environment variable 'DB_URL' not found in .env, using default fallback.")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


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
    """Initializes database tables. Set force_recreate=True to reset schema."""
    if force_recreate:
        print("Dropping old tables...")
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Database tables synchronized successfully.")
