import sys
sys.path.append('../')
from Database import db


def update_data():
    global data
    data = db.get_latest_data()

def get_bmi():
    weight, height = data[3], data[4]
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
    age = data[2]
    return (1.2 * bmi) + (0.23 * age) + 5.4

def get_maintenance_calories():
    def get_bmr():
        if data[1] == 'Male':
            return 88.362 + (13.397 * data[3]) + (4.799 * data[4]) - (5.677 * data[2])
        if data[1] == 'Female':
            return 447.593 + (9.247 * data[3]) + (3.098 + data[4]) - (4.330 * data[2])
        else:
            return 0

    activity_factor = {
        'Little': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Hard': 1.725,
        'Very_hard': 1.9
    }

    return get_bmr() * activity_factor[data[5]]

def get_activity_mapper(key = None,reversed: bool = False):
    activity_mapper = {
        'Little': 'Sedentary (Office job)',
        'Light': 'Light Exercise (1-3 days/week)',
        'Moderate': 'Moderate Exercise (3-5 days/week)',
        'Hard': 'Heavy Exercise (6-7 days a week)',
        'Very_hard': 'Athlete (2x a day)'
    }
    if not key:
        return activity_mapper
    if reversed:
        activity_mapper = {value: key for key,value in activity_mapper.items()}
        return activity_mapper[key]
    else:
        return activity_mapper[key]
    
def get_body_metrics():
    obj = {
        'Gender': data[1],
        'Age': data[2],
        'Weight': data[3],
        'Height': data[4],
        'Activity': get_activity_mapper(data[5]),
        'BMI Score': f'{round(get_bmi()[0],2)} ({get_bmi()[1]})',
        'Maintenance Calories': round(get_maintenance_calories())
    }
    return obj