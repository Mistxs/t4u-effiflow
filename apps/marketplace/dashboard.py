import json
from datetime import datetime
from pytz import timezone

from flask import Blueprint, render_template, jsonify, request
from config import db_params, eddy_headers

import requests

from flask_socketio import SocketIO, emit
import time
from threading import Thread
import random
import pymysql

connection = pymysql.connect(**db_params)

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/marketplace')
socketio = SocketIO()

ts = datetime.now()
timezone = timezone('Etc/GMT-3')
ts_msk = ts.astimezone(timezone)

@dashboard_bp.route('/dashboard')
def index():
    return render_template('/marketplace/dashboard.html', ts=ts_msk, title="Dashboards")

@dashboard_bp.route('/data')
def get_data():
    # Получение данных из базы данных
    data = get_data_from_database()
    # Возвращение данных в формате JSON
    return jsonify(data)

@dashboard_bp.route('/ticketinfo', methods=['POST'])
def getEddyInfo():
    try:
        ticketid = request.json['ticketid']
        url = f"https://yclients.helpdeskeddy.com/api/v2/tickets/{ticketid}/posts/"
        response = requests.request("GET", url, headers=eddy_headers).json()
        print(response)
        return jsonify({'status': 'success', "dataset" : response['data']})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})


@socketio.on('update_favourite_status')
def handle_favourite_status(data):
    # Обработка события обновления статуса "избранного"
    mp_id = data['id']
    is_favourite = data['is_favourite']
    set_favourite_to_database(mp_id,is_favourite)
    new_data = get_data_from_database()
    socketio.emit('update_table', {'data': list(new_data)})
    emit('favourite_status_updated', {'success': True})


def get_data_from_database():
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = """
        SELECT ticket_id, title,
        COUNT(CASE WHEN is_reading IS NULL THEN id ELSE NULL END) AS unread_count,
        is_favourite, MAX(date)
        FROM marketplace_tickets_logs
        WHERE is_reading IS NULL OR is_favourite = 1
        GROUP BY ticket_id, title, is_favourite
        ORDER BY 4 DESC, 5 DESC;
                       """
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()

        return data
    except Exception as e:
        print(f"Error in get_data_from_database: {e}")

def set_favourite_to_database(ticket_id, flag):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = f"""update marketplace_tickets_logs set is_favourite = {flag} where ticket_id = {ticket_id};"""
        cursor.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def get_favourite_tickets(tickets):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = f"""SELECT is_favourite
                FROM marketplace_tickets_logs
                WHERE ticket_id = {tickets} AND is_favourite IS NOT NULL
                GROUP BY is_favourite;
                       """
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        if data[0] == 1:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")

def set_reading_to_database(ticket_id, flag):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = f"""update marketplace_tickets_logs set is_reading = {flag} where ticket_id = {ticket_id};"""
        cursor.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")



def format_data_for_json(data):
    formatted_data = []
    for row in data:
        formatted_row = list(row)
        # Индекс 4 соответствует столбцу 'date'
        formatted_row[4] = formatted_row[4].strftime("%Y-%m-%d %H:%M:%S")
        formatted_data.append(formatted_row)
    return formatted_data

def hookHandler(data):
    supporter = ["Анатолий Филиппов","Андрей Павлов"]

    #помечаем чат избранным, если сообщение до этого были избранными
    if get_favourite_tickets(data["ticket_id"]):
        set_favourite_to_database(data["ticket_id"],1)
    else:
        set_favourite_to_database(data["ticket_id"],0)

    #помечаем чат прочитанным, если сообщение пришло от человека в списке
    for name in supporter:
        if name in data["last_comment"]:
            set_reading_to_database(data["ticket_id"],1)
            break

    new_data = get_data_from_database()
    formatted_data = format_data_for_json(new_data)
    socketio.emit('update_table', {'data': formatted_data})


