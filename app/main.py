from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.models.base import Base
from app.models.user import UserOrm
from app.models.habit import HabitOrm, HabitLogOrm
from app.api.routers.habit import router as habit_router
from app.auth.router import router as auth_router
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True}
)

@app.get("/")
def root():
    return {"message": "Habit Tracker API is running"}

origins = [
    "https://front-willed.vercel.app",
    "https://front-willed.vercel.app/",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]

app.add_middleware(       
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(habit_router)

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=10000, reload=True)