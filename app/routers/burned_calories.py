from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas, oauth2

# Create a router
router = APIRouter(prefix="/bc", tags=["burned calories"])


# Request to add burned calories
@router.post("/")
def calculate_burned_calories(exercise: schemas.Exercise, db: Session = Depends(get_db),
                              user_id: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.UserData).filter(models.UserData.user_id == user_id.id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    exercise_met = (db.query(models.Exercises.exercise_met)
                          .filter(models.Exercises.exercise_name == exercise.exercise_name).scalar())
    if not exercise_met:
        raise HTTPException(status_code=404, detail="Exercise not found")

    exercise_id= (db.query(models.Exercises.exercise_id)
                          .filter(models.Exercises.exercise_name == exercise.exercise_name).scalar())

    burned_calories_number = (exercise_met * 3.5 * user.user_weight * exercise.exercise_time) / 200


    burned_calories_query = models.BurnedCalories(user_id=user_id.id, exercise_id=exercise_id,
                                             burned_calories_number=burned_calories_number,
                                             exercise_time= exercise.exercise_time)

    db.add(burned_calories_query)
    db.commit()


    return {"message": burned_calories_number}