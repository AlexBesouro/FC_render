from datetime import date


def calculate_tdee(gender:str, weight:float, height:int, age:int, activity_level:int):
    activity_dict = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}

    if gender == "male":
        basal_metabolic_rate = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        basal_metabolic_rate = 10 * weight + 6.25 * height - 5 * age - 161

    tdee_number = basal_metabolic_rate * activity_dict[activity_level]

    return tdee_number

def user_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

def calculate_bmi(weight:float, height:int):
    bmi_number = (1.3 * weight) / (height / 100) ** 2.5
    return bmi_number