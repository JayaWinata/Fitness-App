import sys
sys.path.append('../')
from Database import db


def update_data():
    global data
    data = db.get_latest_data()

def get_bmi():
    weight, height = data[4], data[5]
    bmi =  weight / ((height/100)**2)
    classify = ''
    if bmi <= 18.5:
        classify = 'Underweight'
    elif bmi <= 24.99:
        classify = 'Normal Weight'
    elif bmi <= 29.99:
        classify = 'Overweight'
    else:
        classify = 'Obese'

    return bmi, classify

def get_body_fat():
    bmi = get_bmi()
    age = data[3]
    return (1.2 * bmi) + (0.23 * age) + 5.4

def get_maintenance_calories():
    def get_bmr():
        if data[2] == 'Male':
            return 88.362 + (13.397 * data[4]) + (4.799 * data[5]) - (5.677 * data[3])
        if data[2] == 'Female':
            return 447.593 + (9.247 * data[4]) + (3.098 + data[5]) - (4.330 * data[3])
        else:
            return 0

    activity_factor = {
        'Little': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Hard': 1.725,
        'Very_hard': 1.9
    }

    return get_bmr() * activity_factor[data[6]]
