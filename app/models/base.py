from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase 
from uuid import uuid4
from sqlalchemy import func 
from datetime import datetime 


class Base(DeclarativeBase): 
    pass 


class TimestampMixin(Base): 
    __abstract__ = True 

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) 