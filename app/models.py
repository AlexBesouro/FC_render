from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP, Date
from sqlalchemy.sql.expression import text

# Create a class for all your database model classes to inherit from.
Base = declarative_base()


# Create a model for data table of users in postgres
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_birthday = Column(Date, nullable=False)
    gender = Column(Enum("male", "female", name="gender_enum"), nullable=False)
    user_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

class UserData(Base):
    __tablename__ = "users_data"
    user_id = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_height = Column(Integer, nullable=False)
    user_weight = Column(Float, nullable=False)
    user_activity_level = Column(Integer, nullable=False)
    user_tdee_number = Column(Integer, nullable=False)
    user_bmi_number = Column(Integer, nullable=False)
    data_created_at = Column(TIMESTAMP(timezone=True), nullable=False,  primary_key=True, server_default=text("CURRENT_DATE"))


class Food(Base):
    __tablename__ = "foods"
    food_id = Column(Integer, nullable=False, primary_key=True)
    food_name = Column(String, unique=True, nullable=False)
    food_calories_100gr = Column(Integer, nullable=False)
    food_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_DATE"))


class CaloriesConsumptions(Base):
    __tablename__ = "calories_consumptions"
    user_id = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    eaten_food_id = Column(Integer, ForeignKey("foods.food_id", ondelete="CASCADE"), nullable=False)
    eaten_food_mass = Column(Integer, nullable=False)
    eaten_calories_number = Column(Integer, nullable=False)
    eaten_calories_created_at = Column(TIMESTAMP(timezone=True), nullable=False, primary_key=True, server_default=text("NOW()"))


class Exercises(Base):
    __tablename__ = "exercises_data"
    exercise_id = Column(Integer, primary_key=True, nullable=False)
    exercise_name = Column(String, nullable=False)
    exercise_met = Column(Float, nullable=False)

class BurnedCalories(Base):
    __tablename__ = "burned_calories"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises_data.exercise_id", ondelete="CASCADE"), nullable=False)
    exercise_time = Column(Float, nullable=False)
    burned_calories_number = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, primary_key=True, server_default=text("NOW()"))


class DailyTotal(Base):
    __tablename__ = "totals"
    user_id = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    total_burned_calories_number = Column(Float, nullable=False)
    total_eaten_calories_number = Column(Integer, nullable=False)
    result_tdee = Column(Float, nullable=False)
    eaten_calories_created_at = Column(TIMESTAMP(timezone=True), nullable=False, primary_key=True, server_default=text("CURRENT_DATE"))