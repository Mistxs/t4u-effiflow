import datetime
import json
import time
import re

from config import headers, slack_token, dslotsheaders
import requests
from flask import request, jsonify, Blueprint
import sqlite3
from slack_sdk import WebClient

import logging


DB_NAME = 'dslots.db'

dslots = Blueprint('dslots', __name__)



# работа с БД:
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS dslots (id INTEGER PRIMARY KEY AUTOINCREMENT, salon_id INTEGER , datecreated TIMESTAMP)')
    cursor.execute('CREATE TABLE IF NOT EXISTS shedules (id INTEGER  PRIMARY KEY AUTOINCREMENT, salon_id INTEGER , staff INTEGER, sheduledata TEXT, date DATE)')
    conn.commit()
    conn.close()
create_table()
def get_salons():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT salon_id FROM dslots')
    salons = [row[0] for row in cursor.fetchall()]
    conn.close()
    return salons
def safeshedule(salon,data):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        currentdate = datetime.datetime.now()
        for item in data:
            staff = int(item["staff"])
            schedule = json.dumps(item["shedule"])
            cursor.execute("""
                   INSERT INTO shedules (salon_id, staff, sheduledata, date)
                   VALUES (?, ?, ?, ?)
               """, (int(salon), staff, schedule, currentdate))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error {e}")
def selectShedule(salon):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        query = f"SELECT DISTINCT staff, sheduledata FROM shedules where salon_id = {salon} and date(date) = '{date}'"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        data = []
        for row in result:
            staff, scheduledata = row
            data.append({
                "staff": staff,
                "shedule": scheduledata
            })
        return data
    except Exception as e:
        print(f"Error {e}")
def isCopy(salon_id, staff):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    query = f"select * from shedules where salon_id = {salon_id} and staff = {staff} and date(date) = '{date}'"
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    if len(result) == 0:
        return False
    else:
        return True



#роуты для приложения
@dslots.route('/save_salon', methods=['POST'])
def save_salon():
    try:
        salon_id = request.form['salon_id']
        now = datetime.datetime.now()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO dslots (salon_id,datecreated) VALUES (?,?)', (salon_id, now,))
        conn.commit()
        conn.close()
        salons = get_salons()  # Получение списка салонов
        return jsonify({'status': 'success', 'salons': salons})
    except sqlite3.IntegrityError:
        print(f"Ошибка: запись с id {salon_id} уже существует и не может быть добавлена в таблицу records.")
@dslots.route('/get_salons')
def get_salons_route():
    salons = get_salons()
    return jsonify({'status': 'success', 'salons': salons})
@dslots.route('/delete_salon', methods=['POST'])
def delete_salon():
    salon_id = request.form['salon_id']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dslots WHERE salon_id = ?', (salon_id,))
    conn.commit()
    conn.close()
    salons = get_salons()  # Получение списка салонов
    return jsonify({'status': 'success', 'salons': salons})
@dslots.route('/rsafe', methods=['POST'])
def rsafe():
    salon = request.json['salon']
    try:
        staff_shedule = getshedule(salon)
        resafe(salon, staff_shedule)
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})
    return jsonify({'status': 'success', 'text': f'Пересохранение расписания по салону {salon} без удаления выполнено успешно'})
@dslots.route('/safeshedule', methods=['POST'])
def safeToDb():
    salon = request.json['salon']
    try:
        staff_shedule = getshedule(salon)
        safeshedule(salon,staff_shedule)
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})
    return jsonify({'status': 'success',  'text': f'Сохранение расписания в БД по салону {salon} успешно'})
@dslots.route('/repairshedule', methods=['POST'])
def repairFromDb():
    salon = request.json['salon']
    try:
        restoreShedule(salon)
    except Exception as e:
        return jsonify({'status': 'error', 'text': f"{e}"})
    return jsonify({'status': 'success', 'text': 'Восстановили успешно'})
@dslots.route('/clearshedule', methods=['POST'])
def clearShed():
    salon = request.json['salon']
    try:
        staffList = getStaff(salon)
        for i in range(30):
            print(f"start cycle {i}")
            for staff in staffList:
                try:
                    clearShedule(salon,staff)
                except Exception as e:
                    logger.error(f"Нет копии расписания у сотрудника {staff} в салоне {salon}. Попытка удаления прервана")
                    return jsonify({'status': 'error', 'text' : f"Нет копии расписания у сотрудника {staff} в салоне {salon}. Попытка удаления прервана"})
            print(f"end cycle {i}")
        return jsonify({'status': 'success', 'text' : f"Удаление расписания в салоне {salon} выполнено успешно."})
    except Exception as e:
        return jsonify({'status': 'error',
                        'text': f"{e}"})
@dslots.route('/logs')
def get_logs():
    with open('dslots2.log', 'r', encoding='utf-8') as file:
        logs = file.readlines()
    data = []
    for log in logs:
        log_parts = re.split(r' - \w+ - ', log)
        if len(log_parts) >= 2:
            timestamp = log_parts[0]
            message = ' - '.join(log_parts[1:]).strip()
            data.append({'timestamp': timestamp, 'message': message})
    return jsonify(data)



# основные функции, работа с API
def getStaff(salon):
    staff_url = f"https://api.alteg.io/api/v1/company/{salon}/staff/"
    response = requests.request("GET", staff_url, headers=headers).json()
    staff = [item["id"] for item in (response["data"])]
    return staff
def getshedule(salon):
    staff = getStaff(salon)
    data = []
    for item in staff:
        get_shedule_url = f"https://api.alteg.io/api/v1/schedule/{salon}/{item}/2024-01-01/2024-12-31"
        response = requests.request("GET", get_shedule_url, headers=headers).json()
        data.append({
            "staff": item,
            "shedule": response["data"]
        })
    return data
def resafe(salon,data):
    try:
        for i in range(15):
            for item in data:
                put_shedule_url = f"https://api.alteg.io/api/v1/schedule/{salon}/{item['staff']}"
                payload = json.dumps(item['shedule'])
                response = requests.request("PUT", put_shedule_url, headers=headers, data=payload).json()
    except Exception as e:
        message = f"Ошибка в выполнении DSlots.resafe({salon})! Попытка восстановления из бэкапа"
        send_slack_message(message)
        # backupRestore(salon)
def clearShedule(salon, staff):
        for i in range(15):
            if isCopy(salon, staff):
                url = f"https://app.alteg.io/settings/master_save/schedule"
                # payload = f'confirm=0&shed_pat_count=2&shed_pat_after=2&shed_date=&shed_pat_time_start_hours=9&shed_pat_time_start_minutes=0&shed_pat_time_end_hours=20&shed_pat_time_end_minutes=0&shed_pat_week_count=1&repeat=30&id=1653649&salon_id=39184&sched=%5B%5D&date=1704052800'
                payload = f'confirm=0&date=1722801600&id={staff}&repeat=30&salon_id={salon}&sched=%5B%5D&shed_date=&shed_pat_after=2&shed_pat_count=2&shed_pat_time_end_hours=20&shed_pat_time_end_minutes=0&shed_pat_time_start_hours=9&shed_pat_time_start_minutes=0&shed_pat_week_count=1'
                response = requests.request("POST", url, headers=dslotsheaders, data=payload)
                print(response.text)
                # logger.info(response.text)
                # logger.info(f"Удалили расписание сотрудника {staff}, ответ: {response}")
            else:
                raise Exception(f"Нет резервной копии расписания в салоне {salon} для сотрудника {staff}")

def restoreShedule(salon):
    data = selectShedule(salon)
    if not data:
        raise Exception("Отсутствует расписание на выбранную дату в БД")
    for item in data:
        put_shedule_url = f"https://api.alteg.io/api/v1/schedule/{salon}/{item['staff']}"
        payload = item['shedule']
        response = requests.request("PUT", put_shedule_url, headers=headers, data=payload).json()
        # logger.info(f"Сохранили расписание сотрудника {item['staff']}, ответ: {response}")



# функции для запуска приложения, вспомогательные функции
# def error_listener(event):
#     if event.exception:
#         logger.error(f"Ошибка выполнения задачи: {event.exception}")
#     else:
#         logger.error(f"Пропущено выполнение задачи: {event.job_id}")
def job():
    # logger.info(f"Запуск DSlotsRepair.job")
    salons = get_salons()
    for salon in salons:
        staff_shedule = getshedule(salon)
        resafe(salon, staff_shedule)
# def runSheduler():
#     try:
#         logger.info(f"Запуск DSlotsRepair.runSheduler")
#         scheduler = BlockingScheduler()
#         scheduler.add_listener(error_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
#         scheduler.add_job(job, 'interval', hours=2)
#         scheduler.start()
#     except Exception as e:
#         message = f"Ошибка в выполнении DSlots.runSheduler! Попытка повторного запуска через 10 сек"
#         logger.error(f"Произошла ошибка в функции runSheduler: {e}. Попытка повторного запуска через 10 сек")
#         time.sleep(10)
#         runSheduler()
def send_slack_message(message):
    client = WebClient(token=slack_token)
    response = client.chat_postMessage(
        channel="#innachannel",
        text=message
    )
    if response["ok"]:
        return True
    return False