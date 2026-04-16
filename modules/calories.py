def calculate_bmr(weight, height, age):  # basal metabolic rate
    return 10 * weight + 6.25 * height - 5 * age + 5


def calculate_maintenance(bmr, activity_level):
    return bmr * activity_level


def get_calorie_target(goal, maintenance):
    if goal == "Fat Loss":
        return maintenance - 500
    elif goal == "Muscle Gain":
        return maintenance + 500
    else:
        return maintenance
