from typing import Optional, List
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas

# Create a router for operations with 'users' request
router = APIRouter(prefix="/exercises", tags=["exercises"])


# # Request to find exercise MET by name
@router.get("/", response_model=List[schemas.ExerciseResponse])
def find_exercise_by_name(db: Session = Depends(get_db), search: Optional[str] = ""):
    exercise_query = db.query(models.Exercises).filter(models.Exercises.exercise_name.contains(search))
    exercise_to_find = exercise_query.all()
    if not exercise_to_find:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return  exercise_to_find