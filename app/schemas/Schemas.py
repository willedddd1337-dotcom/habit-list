from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class UserCreateSchema(BaseModel):
    username: str
    email: str

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    username: str
    email: str
    created_at: datetime

class HabitCreateSchema(BaseModel):
    title: str
    description: str | None = None
    emoji: str | None = "🎯"

class HabitUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    emoji: str | None = None

class HabitSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    title: str
    description: str | None
    emoji: str | None
    created_at: datetime

class HabitLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    habit_id: str
    logged_date: date