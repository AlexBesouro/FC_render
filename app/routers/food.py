from typing import Optional, List
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas, oauth2

# Create a router
router = APIRouter(prefix="/food", tags=["food"])

# Request to find food by name
@router.get("/", response_model=List[schemas.FoodResponse])
def find_food_by_name(db: Session = Depends(get_db), search: Optional[str] = ""):
    food_query = db.query(models.Food).filter(models.Food.food_name.contains(search))
    food_to_find = food_query.all()
    if not food_to_find:
        raise HTTPException(status_code=404, detail="Food not found")
    return food_to_find

# Request to add a new food
@router.post("/", status_code=201, response_model=schemas.FoodResponse)
def add_food(food:schemas.FoodCreate, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    food_query = db.query(models.Food).filter(models.Food.food_name == food.food_name).first()
    if food_query:
        raise HTTPException(status_code=409, detail=f"This food is already in our database")
    new_food = models.Food(**food.model_dump())
    db.add(new_food)
    db.commit()

    return new_food