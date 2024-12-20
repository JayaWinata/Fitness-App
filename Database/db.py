import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def open():
    global db,cursor
    db = mysql.connector.connect(host=os.environ.get('host'),user=os.environ.get('user'),database=os.environ.get('database'),passwd=os.environ.get('password'))
    cursor = db.cursor()

def add_calories(calories: int):
    sum = calories
    cursor.execute("SELECT date FROM daily_calories WHERE date = current_date()")
    if (cursor.fetchone()):
        cursor.execute("SELECT calories FROM daily_calories WHERE date = current_date()")
        today_calories = cursor.fetchone()[0]
        sum += int(today_calories)
        cursor.execute("UPDATE daily_calories SET calories = %s WHERE date = current_date()",(sum,))
        db.commit()
    else:
        cursor.execute("INSERT INTO daily_calories VALUES (current_date(),%s)",(sum,))   
        db.commit()

def get_calories():
    cursor.execute('SELECT calories FROM daily_calories WHERE date = current_date()')
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0

def get_calories_history(limit: int):
    cursor.execute(f'SELECT * from daily_calories ORDER BY date LIMIT {limit}')
    value = cursor.fetchall() 
    return value if value else None

def get_calories_limit():
    cursor.execute('SELECT calories_limit FROM calories_limit ORDER BY date DESC LIMIT 1')
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0

def set_calories_limit(limit):
    cursor.execute('INSERT INTO calories_limit VALUES (current_date(), %s)',(limit,))
    db.commit()

def get_latest_data():
    cursor.execute('SELECT * FROM data ORDER BY date DESC LIMIT 1')
    value = cursor.fetchone()
    return value if value else None

def insert_data(data: tuple):
    cursor.execute('INSERT INTO data VALUES (current_date(),%s,%s,%s,%s,%s)',data)
    db.commit()

def get_history(column_name: str,limit: int):
    if column_name == 'calories_limit':
        cursor.execute(f'SELECT date,{column_name} FROM (SELECT * FROM calories_limit ORDER BY date DESC LIMIT {limit}) AS temp ORDER BY date')
    else:
        cursor.execute(f'SELECT date,{column_name} FROM (SELECT * FROM data ORDER BY date DESC LIMIT {limit}) AS temp ORDER BY date')
    value = cursor.fetchall()
    return value if value else None

def get_schedule(day: str):
    cursor.execute('SELECT * FROM schedule WHERE day = %s ORDER BY menu_order',(day,))
    value = cursor.fetchall()
    return value if value else None

def get_current_schedule():
    cursor.execute('SELECT * FROM schedule WHERE day = dayname(current_date()) ORDER BY menu_order')
    value = cursor.fetchall()
    return value if value else None

def add_schedule(data:tuple):
    cursor.execute('INSERT INTO schedule VALUES (%s,%s,%s)',data)
    db.commit()

def update_schedule(data:list):
    data.extend([data[0],data[-1]])
    data = tuple(data)
    cursor.execute('''UPDATE schedule
                    SET menu_order = %s,
                    menu = %s,
                    day = %s 
                    WHERE menu_order = %s and day = %s''',data)
    db.commit()
    
def delete_schedule(data:tuple):
    cursor.execute('DELETE FROM schedule WHERE menu_order = %s and day = %s',data)
    db.commit()

def close():
    global db, cursor
    if cursor:
        cursor.close()
    if db:
        db.close()