from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import verify_password, create_access_token
from schemas import Token
from contextlib import asynccontextmanager
from database import init_db
import crud
from routes.user_routes import router as user_router
from routes.anime_routes import router as anime_router
from routes.manga_routes import router as manga_router
from routes.vtuber_routes import router as vtuber_router
from routes.game_routes import router as game_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(anime_router)
app.include_router(manga_router)
app.include_router(vtuber_router)
app.include_router(game_router)



@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = crud.get_all_users()
    user = next(
        (u for u in users if u["username"] == form_data.username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username!")
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password!")
    token = create_access_token({"user_id": user["id"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def root():
    return {"message": "Welcome to ----Otaku Hub----!"}
