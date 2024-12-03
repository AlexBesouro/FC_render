from typing import List, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas, oauth2

# Create a router
router = APIRouter(prefix="/cc", tags=["calories consumption"])

# Request to find all eaten food by user
@router.get("/", response_model=List[schemas.FoodList]) #
def find_eaten_food(db: Session = Depends(get_db), search: Optional[str] = "",
                    user_id: int = Depends(oauth2.get_current_user)):

    food_query = (
        db.query(
            models.CaloriesConsumptions.eaten_food_mass,
            models.CaloriesConsumptions.eaten_food_id,
            models.CaloriesConsumptions.eaten_calories_number,
            models.CaloriesConsumptions.eaten_calories_created_at,
            models.Food.food_name
        )
        .filter(models.CaloriesConsumptions.user_id == user_id.id)
        .filter(models.Food.food_name.contains(search))
        .join(models.Food, models.Food.food_id == models.CaloriesConsumptions.eaten_food_id)
        .all()
    )
    food_query = list(map(lambda x: x._mapping, food_query))
    return  food_query


# Request to calculate user's calories consumption
@router.post("/", response_model=schemas.FoodEatenResponse)
def add_eaten_calories(food: schemas.FoodEaten, db: Session = Depends(get_db),
                       user_id: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(models.User.user_id == user_id.id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    calories_query = (db.query(models.Food.food_calories_100gr, models.Food.food_id)
                      .filter(models.Food.food_name == food.food_name).all())

    calories_query = list(map(lambda x: x._mapping, calories_query))
    if not calories_query:
        raise HTTPException(status_code=404, detail="Food is not in our database. You can add it if you want")

    food_id = calories_query[0]["food_id"]
    calories_100gr = calories_query[0]["food_calories_100gr"]

    eaten_calories_number = calories_100gr * (food.food_mass / 100)

    eaten_food_query =  models.CaloriesConsumptions(user_id=user_id.id, eaten_food_id=food_id,
                                                    eaten_food_mass=food.food_mass,
                                                    eaten_calories_number=eaten_calories_number)

    db.add(eaten_food_query)
    db.commit()
    db.refresh(eaten_food_query)
    return eaten_food_query
