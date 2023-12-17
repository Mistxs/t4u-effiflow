from flask import Blueprint, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
from threading import Thread
import random

dashboard_bp = Blueprint('dashboard', __name__)
socketio = SocketIO()

@dashboard_bp.route('/dashboard')
def index():
    return render_template('/marketplace/dashboard.html')

@dashboard_bp.route('/start')
def start_task():
    # Запуск функции в отдельном потоке, чтобы не блокировать сервер
    task_thread = Thread(target=long_running_task)
    task_thread.start()
    # Ответ клиенту сразу
    return "Task started"

def long_running_task():
    # Долгая операция (замените этот блок на свою логику)
    a = 0
    for i in range(5):
        time.sleep(1)
        print(f"Processing: {i + 1}")
        percent_complete = (i + 1) * 20
        socketio.emit('processing', percent_complete)
    x = random.random()
    data = {"success": "True", "data": f"Вывод json прямо на страницу. Случайное число - {x}"}

    # Отправка сообщения по WebSocket, когда задача завершена
    socketio.emit('task_completed', data)
    time.sleep(10)
    data = {"success": "True", "data": f"Для самых терпеливых, еще одно событие)))"}
    socketio.emit('task_completed', data)
