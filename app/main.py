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


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True}
)


@app.get("/")
def root():
    return {
        "message": "Habit Tracker API is running 🚀"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(habit_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)