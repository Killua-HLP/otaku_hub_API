# Otaku Hub API

All-in-One REST API for tracking Anime, Manga, VTubers, and Games.

## Tech Stack
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication

## Setup
1. Clone the repo
   git clone https://github.com/Killua-HLP/otaku_hub_API

2. Install dependencies
   pip install -r requirements.txt

3. Create .env file
   DB_URL=postgresql://...
   SECRET_KEY=your-secret-key

4. Run the server
   uvicorn main:app --reload

## API Endpoints
### Auth
- POST /login

### Users
- GET    /users
- POST   /users
- GET    /users/{id}
- PUT    /users/{id}
- DELETE /users/{id}
- GET    /me

### Anime
- GET    /anime_list
- POST   /anime_list
- GET    /anime_list/{id}
- PUT    /anime_list/{id}
- DELETE /anime_list/{id}

### Manga, VTuber, Game (same pattern)
