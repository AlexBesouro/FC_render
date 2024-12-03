from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas, utils, oauth2
from app.data_func import calculate_tdee, user_age, calculate_bmi


# Create a router for operations with 'users' request
router = APIRouter(prefix="/users", tags=["users"])

# Request to find a user by id
@router.get("/{user_id}", response_model=List[schemas.UserIdResponse]) #
def find_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    user_to_find = user_query.first()
    if not user_to_find:
        raise HTTPException(status_code=404, detail="User not found")

    user_data_query = (db.query(models.User, models.UserData)
                       .filter(models.User.user_id == user_id)
                       .join(models.UserData, models.User.user_id == models.UserData.user_id)
                       .all())

    user_data_query = list(map(lambda x: x._mapping, user_data_query))

    return user_data_query

# Request to create a new user
@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email).first()

    if user_query:
        raise HTTPException(status_code=409, detail=f"User with email: {user.email} already exist")

    user.password = utils.hashing(user.password)

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Request to create a data for user
@router.post("/data", status_code=201, response_model=List[schemas.UserDataResponse])
def create_data(user_data: schemas.UserData, user_id: int = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):

    # print(user_id)
    user_query = db.query(models.User).filter(models.User.user_id == user_id.id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    age = user_age(user.user_birthday)

    tdee_number = calculate_tdee(gender=user.gender, weight=user_data.user_weight, height=user_data.user_height,
                                 age=age, activity_level=user_data.user_activity_level)

    bmi_number = calculate_bmi(weight=user_data.user_weight, height=user_data.user_height)

    data_insert = models.UserData(user_id= user_id.id, user_height= user_data.user_height,
                                  user_weight= user_data.user_weight,
                                  user_activity_level= user_data.user_activity_level,
                                  user_tdee_number= tdee_number,
                                  user_bmi_number= bmi_number)


    db.add(data_insert)
    db.commit()
    query = db.query(models.UserData).filter(models.UserData.user_id == user_id.id).all()
    return query

