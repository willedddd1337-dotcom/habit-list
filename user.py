from app.db.session import SessionLocal, engine
from app.models.base import Base, TimestampMixin
from app.models.user import UserOrm
from app.models.habit import HabitOrm, HabitLogOrm

Base.metadata.create_all(bind=engine)

db = SessionLocal()
user = UserOrm(id="test-user-1", username="test", email="test@test.com")
db.add(user)
db.commit()
print("Пользователь создан!")
db.close()