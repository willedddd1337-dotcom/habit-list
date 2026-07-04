from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.models.base import Base
from app.api.routers.habit import router as habit_router
from app.auth.router import router as auth_router

from dotenv import load_dotenv 
import os 

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

print("MAIN FILE LOADED")

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True}
)


@app.get("/")
def root():
    return {
        "message": "Habit Tracker API is running 🚀"
    }


origins = [
    "https://front-willed.vercel.app/",  # Замени на РЕАЛЬНУЮ ссылку твоего фронтенда с Vercel
    "http://localhost",                # На всякий случай для локальных тестов
    "http://localhost:3000",           # (если открываешь код локально)
    "http://127.0.0.1:5500",           # Часто используется для Live Server в VS Code
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешаем запросы только с этих адресов
    allow_credentials=True,
    allow_methods=["*"],              # Разрешаем все методы (POST, GET, OPTIONS, DELETE и т.д.)
    allow_headers=["*"],              # Разрешаем любые заголовки (включая Authorization, Content-Type)
)

# Дальше идет твой остальной код (роуты, логика и т.д.)
app.include_router(auth_router)
app.include_router(habit_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)