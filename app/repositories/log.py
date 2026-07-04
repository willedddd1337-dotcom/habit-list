# repositories/log.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.habit import HabitLogOrm
from datetime import date

class HabitLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_habit(self, habit_id: str) -> list[HabitLogOrm]:
        return self.db.scalars(
            select(HabitLogOrm).where(HabitLogOrm.habit_id == habit_id)
        ).all()

    def get_by_date(self, habit_id: str, logged_date: date) -> HabitLogOrm | None:
        return self.db.scalars(
            select(HabitLogOrm).where(
                HabitLogOrm.habit_id == habit_id,
                HabitLogOrm.logged_date == logged_date
            )
        ).first()

    def create(self, habit_id: str, logged_date: date) -> HabitLogOrm:
        log = HabitLogOrm(habit_id=habit_id, logged_date=logged_date)
        self.db.add(log)
        return log