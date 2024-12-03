from typing import Optional, List
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas, oauth2
from datetime import datetime
from sqlalchemy import func

date = datetime.today()



# Create a router
router = APIRouter(prefix="/total", tags=["total"])

# Request to find food by name
@router.post("/", response_model=schemas.Total)
def daily_total(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    total_eaten_calories_query = (db.query(func.sum(models.CaloriesConsumptions.eaten_calories_number))
                            .filter(func.date(models.CaloriesConsumptions.eaten_calories_created_at) == '2024-12-04',
                                    models.CaloriesConsumptions.user_id == user_id.id)
                            .group_by(func.date(models.CaloriesConsumptions.eaten_calories_created_at))).first()

    if not total_eaten_calories_query:
        total_eaten_calories = 0
    else:
        total_eaten_calories = total_eaten_calories_query[0]

    total_burned_calories_query = (db.query(func.sum(models.BurnedCalories.burned_calories_number))
                            .filter(func.date(models.BurnedCalories.created_at) == '2024-12-02',
                                    models.BurnedCalories.user_id == user_id.id)
                            .group_by(func.date(models.BurnedCalories.created_at))).first()

    if not total_burned_calories_query:
        total_burned_calories = 0
    else:
        total_burned_calories = total_burned_calories_query[0]

    user_tdee = db.query(models.UserData.user_tdee_number).filter(models.UserData.user_id == user_id.id).scalar()

    daily_result = total_eaten_calories - total_burned_calories - user_tdee

    daily_total_row = models.DailyTotal(user_id=user_id.id, total_burned_calories_number=total_burned_calories,
                                        total_eaten_calories_number=total_eaten_calories, result_tdee=daily_result)
    db.add(daily_total_row)
    db.commit()

    return daily_total_row