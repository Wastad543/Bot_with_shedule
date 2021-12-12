import psycopg2
import datetime

# Соединение с БД
def conn_to_bd(numero_week, day):
    abr = numero_week[0]

    if abr + str(day) == 'CFriday':
        return 'Congratulations, you have a day off!'

    else:
        conn = psycopg2.connect(dbname='vuzt', user='postgres',
                                password='2003', host='localhost', port='5432')

        cursor = conn.cursor()

        cursor.execute('SELECT * FROM ' + abr + str(day))

        timetable = cursor.fetchall()

        total_timetable = numero_week+' week'+'\n\n'
        for i in timetable:
            total_timetable += '\n'.join(i) + '\n\n'

        return total_timetable


def know_week():
    today = datetime.datetime.today()
    week = today.isocalendar()[1]


    if week % 2 == 1:
        numero_week = 'Chetnaya'
    else:
        numero_week = 'Nechetnaya'

    return numero_week