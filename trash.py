from flask import Flask, render_template, make_response, send_from_directory
from flask_socketio import SocketIO, emit
import json
import io
from openpyxl import Workbook

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('trash.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@socketio.on('convert_and_send')
def convert_and_send(json_data):
    # Преобразование JSON в XLS
    workbook = Workbook()
    sheet = workbook.active

    for data in json.loads(json_data):
        sheet.append(list(data.values()))

    # Сохранение XLS в байтовом объекте
    # Сохранение XLS в байтовом объекте
    xls_io = io.BytesIO()
    workbook.save(xls_io)
    xls_io.seek(0)

    # Сохранение файла на сервере
    filename = 'output.xlsx'
    with open(app.config['DOWNLOAD_FOLDER'] + '/' + filename, 'wb') as file:
        file.write(xls_io.getvalue())

    # Отправка ссылки через WebSocket
    emit('file_link', {'link': f'/download/{filename}'})

if __name__ == '__main__':
    app.config['DOWNLOAD_FOLDER'] = 'downloads'
    socketio.run(app,port=3212,allow_unsafe_werkzeug=True)
