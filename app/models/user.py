from sqlalchemy.orm import Mapped, mapped_column
from .base import TimestampMixin 


class UserOrm(TimestampMixin): 
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    