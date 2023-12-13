from datetime import datetime

from flask import jsonify, request, Blueprint

from config import bearer, db_params, headers
from concurrent.futures import ThreadPoolExecutor

import pymysql


chatHandler = Blueprint('chatHandler', __name__)

connection = pymysql.connect(**db_params)

def create_table():
    conn = pymysql.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS marketplace_tickets_logs (id INT AUTO_INCREMENT PRIMARY KEY, ticket_id INT, comment TEXT, title VARCHAR(255), date DATETIME);'
    )

    conn.commit()
    conn.close()


create_table()

def savetodb(ticket_title, ticket_id, text):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()
        current_time = datetime .now()

        query = """
                           INSERT INTO marketplace_tickets_logs (ticket_id, comment, title, date)
                           VALUES (%s, %s, %s, %s)
                       """



        values = (int(ticket_id), text, ticket_title, current_time)
        cursor.execute(query, values)

        conn.commit()
        conn.close()

        print("Data successfully saved in the 'marketplace_tickets_logs' table.")
    except Exception as e:
        print(f"Error: {e}")


@chatHandler.route('/marketplace/chathandler', methods=['POST'])
def readHooks():
    try:
        response = request.json
        ticket_title = response["title"]
        ticket_id = response["ticket_id"]
        text = response["last_comment"]
        savetodb(ticket_title,ticket_id,text)
        return jsonify({'status': 'success', 'text': f'saved'})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})

