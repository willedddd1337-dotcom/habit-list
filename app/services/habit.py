from sqlalchemy.orm import Session
from app.repositories.habit import HabitRepository
from app.repositories.log import HabitLogRepository
from app.models.habit import HabitOrm, HabitLogOrm
from datetime import date, timedelta

class HabitService:
    def __init__(self, db: Session):
        self.repo = HabitRepository(db)
        self.log_repo = HabitLogRepository(db)
        self.db = db

    def get_user_habits(self, user_id: str) -> list[HabitOrm]:
        return self.repo.get_all_by_user(user_id)

    def create_habit(self, user_id: str, title: str, description: str | None, emoji: str | None) -> HabitOrm:
        habit = self.repo.create(user_id=user_id, title=title, description=description, emoji=emoji)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def delete_habit(self, user_id: str, habit_id: str) -> None:
        habit = self.repo.get_by_id(habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")
        if habit.user_id != user_id:
            raise ValueError("Нет доступа")
        self.repo.delete(habit)
        self.db.commit()

    def log_habit(self, user_id: str, habit_id: str) -> HabitLogOrm:
        habit = self.repo.get_by_id(habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")
        if habit.user_id != user_id:
            raise ValueError("Нет доступа")

        today = date.today()
        existing = self.log_repo.get_by_date(habit_id=habit_id, logged_date=today)
        if existing:
            raise ValueError("Привычка уже отмечена сегодня")

        log = self.log_repo.create(habit_id=habit_id, logged_date=today)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_stats(self, user_id: str, habit_id: str) -> dict:
        habit = self.repo.get_by_id(habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")
        if habit.user_id != user_id:
            raise ValueError("Нет доступа")

        logs = self.log_repo.get_all_by_habit(habit_id)
        dates = sorted({log.logged_date for log in logs})
        last_log = dates[-1] if dates else None

        return {
            "habit_id": habit_id,
            "title": habit.title,
            "total_days": len(dates),
            "current_streak": self._calc_streak(dates),
            "last_log_date": str(last_log) if last_log else None,
        }

    def _calc_streak(self, dates: list[date]) -> int:
        if not dates:
            return 0

        streak = 0
        current = date.today()

        for d in reversed(dates):
            if d == current:
                streak += 1
                current = current - timedelta(days=1)
            else:
                break

        return streak
    
    def get_logs_for_month(self, user_id: str, habit_id: str, year: int, month: int) -> list[str]:
        habit = self.repo.get_by_id(habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")
        if habit.user_id != user_id:
            raise ValueError("Нет доступа")

        logs = self.log_repo.get_all_by_habit(habit_id)
        return [
            str(log.logged_date)
            for log in logs
            if log.logged_date.year == year and log.logged_date.month == month
        ]