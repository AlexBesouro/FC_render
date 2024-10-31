import psycopg2
from psql_connetion import psql_connection
from user_profile import User


def body_mass_index(user_weight: float, user_height: float) -> str:
    """
    Calculate Body mass index (BMI) of a person.
    The BMI is defined as the body mass divided by the square of the body height, and is expressed in units of kg/m2,
    resulting from mass in kilograms (kg) and height in metres (m).
    :param user_weight: user's weight in kg (float)
    :param user_height: user's height in cm (float)
    :return: BMI and conclusion about user's BMI (str)
    """

    bmi = (1.3 * user_weight) / (user_height / 100) ** 2.5

    if bmi < 16:
        return f"Your BMI is {bmi}, you are in category 'Underweight (Severe thinness)'"
    elif 16 <= bmi < 17:
        return f"Your BMI is {bmi}, you are in category 'Underweight (Moderate thinness)'"
    elif 17 <= bmi < 18.5:
        return f"Your BMI is {bmi}, you are in category 'Underweight (Mild thinness)'"
    elif 18.5 <= bmi < 25:
        return f"Your BMI is {bmi}, you are in category 'Normal range'"
    elif 25 <= bmi < 30:
        return f"Your BMI is {bmi}, you are in category 'Overweight (Pre-obese)'"
    elif 30 <= bmi < 35:
        return f"Your BMI is {bmi}, you are in category 'Obese (Class I)'"
    elif 35 <= bmi < 40:
        return f"Your BMI is {bmi}, you are in category 'Obese (Class II)'"
    else:
        return f"Your BMI is {bmi}, you are in category 'Obese (Class III, mortal)'"

# print(body_mass_index(80, 180))

def total_daily_energy_expenditure(user_gender: str, user_weight: float, user_height: float, user_age: int,
                                   activity_lvl: int) -> float:
    """
    Calculate TDEE using Mifflin - St. Jeor equation
    :param user_gender: male/female (str)
    :param user_weight: user's weight in kg (float)
    :param user_height: user's height in cm (float)
    :param user_age: user's age from 5 to 100 (int)
    :param activity_lvl: level of physical activity from 1 to 5 (int)
    :return: TDEE (float)
    """

    if user_gender == "male":
        basal_metabolic_rate = 10 * user_weight + 6.25 * user_height - 5 * user_age + 5
    else:
        basal_metabolic_rate = 10 * user_weight + 6.25 * user_height - 5 * user_age - 161

    if activity_lvl == 1:
        tdee = basal_metabolic_rate * 1.2
    elif activity_lvl == 2:
        tdee = basal_metabolic_rate * 1.375
    elif activity_lvl == 3:
        tdee = basal_metabolic_rate * 1.55
    elif activity_lvl == 4:
        tdee = basal_metabolic_rate * 1.725
    else:
        tdee = basal_metabolic_rate * 1.9

    return tdee

# print(total_daily_energy_expenditure('male', 85, 180, 28, 3))

food = {"rice" : 360}

def calorie_consumption_calculator(food_type: str, food_mass: int, food_data: dict) -> float:
    """
    Functions that calculate caloric intake from food
    :param food_type: name of food (str)
    :param food_mass: mass of food in grams (int)
    :param food_data: database of food (dict?) # what type of data from database
    :return: quantity of eaten calories (float)
    """
    quantity_of_eaten_calories = food_mass * food_data[food_type]
    return quantity_of_eaten_calories


def aerobic_exercise_calories_burning(user_weight: int, exercise_name: str, exercise_time: float,
                                      exercise_intensity: int = 3) -> float:
    """
    Function to calculate burned calories after aerobic type of exercise
    :param exercise_name: name of exercise (str)
    :param exercise_time: exercise duration (float)
    :param exercise_intensity: approximate level of intensity (default 3) (int)
    :param user_weight: weight of user (int)
    :return: number of calories (float)
    """
    result = None
    connection, crsr = psql_connection("database.ini", "postgresql")
    exercise_list = crsr.execute("SELECT exercise_name FROM exercises")
    exercise_list = crsr.fetchall()
    exercise_list = [exercise_name[0] for exercise_name in exercise_list]


    if exercise_name in exercise_list:
        exercise_met_average = crsr.execute(f"SELECT exercise_met_average FROM exercises "
                                            f"WHERE exercise_name = '{exercise_name}'")

        exercise_met_average = crsr.fetchall()[0][0]
        # print(exercise_met_average)
        result = (exercise_met_average * 3.5 * user_weight * exercise_time * (exercise_intensity / 3)) / 200
    else:
        print("Exercise not in db")

    if crsr is not None:
        crsr.close()
    if connection is not None:
        connection.close()
        print("Database connection terminated.")


    return result

# print(aerobic_exercise_calories_burning(76, "jum", 60, 3))

def add_new_user(first_name, last_name, gender, age, height, weight):
    user = User(first_name, last_name, gender, age, height, weight)

    connection, crsr = psql_connection("database.ini", "postgresql")
    crsr.execute("SELECT max(user_id) FROM user_list")
    last_id_number = crsr.fetchall()[0][0]
    if last_id_number is None:
        last_id_number = 0

    insert_script = (f"INSERT INTO user_list (user_id, first_name, last_name, user_gender, user_age, "
                     f"user_height, user_weight)"
                     f" VALUES (%s, %s, %s, %s, %s, %s, %s)")
    inserted_values = (last_id_number + 1, first_name, last_name, gender, age, height, weight)

    crsr.execute(insert_script, inserted_values)
    connection.commit()

    if crsr is not None:
        crsr.close()
    if connection is not None:
        connection.close()
        print("Database connection terminated.")

    return user

print(repr(add_new_user("Aleks", "Zhukov","male", 28, 180, 85)))