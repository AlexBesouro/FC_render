from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing_extensions import  Literal





class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    user_birthday: date
    gender: str


class UserResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    user_birthday: date
    gender: str
    user_created_at: datetime

class UserData(BaseModel):
    user_height: int
    user_weight: float
    user_activity_level: int

class UserDataResponse(UserData):
    user_tdee_number: float
    user_bmi_number: float

class UserIdResponse(BaseModel):
    User: UserResponse
    UserData: UserDataResponse


class FoodCreate(BaseModel):
    food_name: str
    food_calories_100gr: int


class FoodResponse(BaseModel):
    food_name: str
    food_calories_100gr: int
    food_created_at: datetime

class FoodEaten(BaseModel):
    food_name: str
    food_mass: int

class FoodEatenResponse(BaseModel):
    eaten_food_mass: int
    eaten_food_id: int
    eaten_calories_number: float
    eaten_calories_created_at: datetime

class FoodList(FoodEatenResponse):
    food_name:str

class Exercise(BaseModel):
    exercise_name: str
    exercise_time: float

class ExerciseResponse(BaseModel):
    exercise_name: str
    exercise_met: float

class Total(BaseModel):
    user_id: int
    total_burned_calories_number: float
    total_eaten_calories_number: float
    result_tdee: float
    eaten_calories_created_at: datetime


