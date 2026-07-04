from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.habit import HabitOrm

class HabitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_user(self, user_id: str) -> list[HabitOrm]:
        return self.db.scalars(
            select(HabitOrm).where(HabitOrm.user_id == user_id)
        ).all()

    def get_by_id(self, habit_id: str) -> HabitOrm | None:
        return self.db.get(HabitOrm, habit_id)

    def create(self, user_id: str, title: str, description: str | None, emoji: str | None) -> HabitOrm:
        habit = HabitOrm(user_id=user_id, title=title, description=description, emoji=emoji)
        self.db.add(habit)
        return habit

    def delete(self, habit: HabitOrm) -> None:
        self.db.delete(habit)