from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date
from datetime import date
from .base import TimestampMixin

class HabitOrm(TimestampMixin):
    __tablename__ = "habits"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None]
    emoji: Mapped[str | None]
    logs: Mapped[list["HabitLogOrm"]] = relationship(back_populates="habit")

class HabitLogOrm(TimestampMixin):
    __tablename__ = "habit_logs"

    habit_id: Mapped[str] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    logged_date: Mapped[date] = mapped_column(Date)

    habit: Mapped["HabitOrm"] = relationship(back_populates="logs")