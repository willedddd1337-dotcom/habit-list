from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.habit import HabitService
from app.schemas.Schemas import HabitSchema, HabitCreateSchema, HabitLogSchema
from app.auth.utils import get_current_user
from app.models.user import UserOrm

router = APIRouter(prefix="/habits", tags=["habits"])

@router.get("", response_model=list[HabitSchema])
def get_habits(
    db: Session = Depends(get_db),
    user: UserOrm = Depends(get_current_user)
):
    service = HabitService(db)
    return service.get_user_habits(user_id=user.id)

@router.post("", response_model=HabitSchema)
def create_habit(
    data: HabitCreateSchema,
    db: Session = Depends(get_db),
    user: UserOrm = Depends(get_current_user)
):
    service = HabitService(db)
    return service.create_habit(
        user_id=user.id,
        title=data.title,
        description=data.description,
        emoji=data.emoji,
    )

@router.delete("/{habit_id}")
def delete_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    user: UserOrm = Depends(get_current_user)
):
    service = HabitService(db)
    try:
        service.delete_habit(user_id=user.id, habit_id=habit_id)
        return {"message": "Привычка удалена"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{habit_id}/log", response_model=HabitLogSchema)
def log_habit(
    habit_id: str,
    db: Session = Depends(get_db),
    user: UserOrm = Depends(get_current_user)
):
    service = HabitService(db)
    try:
        return service.log_habit(user_id=user.id, habit_id=habit_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{habit_id}/stats")
def get_stats(
    habit_id: str,
    db: Session = Depends(get_db),
    user: UserOrm = Depends(get_current_user)
):
    service = HabitService(db)
    try:
        return service.get_stats(user_id=user.id, habit_id=habit_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{habit_id}/calendar")
def get_calendar(
    habit_id: str,
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user: UserOrm = Depends(get_current_user)
):
    service = HabitService(db)
    try:
        dates = service.get_logs_for_month(user_id=user.id, habit_id=habit_id, year=year, month=month)
        return {"dates": dates}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))