import threading
from datetime import datetime
from apps.marketplace.dashboard import hookHandler, readTickets
from apps.marketplace.src.api_schemas import route_schemas
from apps.marketplace.moderation import createNewPage


import pymysql
from flask import jsonify, request, Blueprint
from jsonschema import validate, ValidationError
from loguru import logger


from config import db_params


mpHandler = Blueprint('mpHandler', __name__)
logger.add("mpHandler.log", level="INFO", rotation="1 week", retention="2 weeks")

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


def validate_json(route, data):
    try:
        validate(data, route_schemas.get(route, {}))
    except ValidationError as e:
        raise e

@mpHandler.route('/marketplace/chathandler', methods=['POST'])
def readHooks():
    try:
        response = request.json
        ticket_title = response["title"]
        ticket_id = response["ticket_id"]
        text = response["last_comment"]
        savetodb(ticket_title,ticket_id,text)
        hookHandler(response)
        return jsonify({'status': 'success', 'text': f'saved'})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})

@mpHandler.route('/marketplace/chathandler/read', methods=['POST'])
def readAllHooks():
    try:
        response = request.json
        ticket_ids = response["ticket_ids"]
        readTickets(ticket_ids)
        return jsonify({'status': 'success', 'text': f'saved'})
    except Exception as e:
        return jsonify({'status': 'error in readAllHooks', 'text': f'{e}'})


@mpHandler.route('/marketplace/newModeration', methods=['POST'])
def read_new_moderation_request():
    try:
        logger.info(f"Hook received: {request}")
        logger.info(f"Hook payload: {request.json}")


        validate_json('/marketplace/newModeration', request.json)
        response = request.json

        params = {
            "parnter_name": response["name"],
            "status": "Новый",
            "slack_url": response["slack_url"],
            "dev_url": response["dev_url"],
            "app_url": response["app_url"]
        }

        # Запускаем createNewPage в отдельном потоке
        thread = threading.Thread(target=createNewPage, args=(params,))
        thread.start()
        # resp = createNewPage(params)
        # logger.info(f"read_new_moderation_request done : status: success, response: {resp}")


        return jsonify({'status': 'success', 'text': 'saved'})
    except ValidationError as e:
        logger.error(f"status: error in read_new_moderation_request, module validate_json, text: Validation error: {e}")

        return jsonify({'status': 'error in module validate_json', 'text': f'Validation error: {e}'})
    except Exception as e:
        logger.error(f"status: error in read_new_moderation_request, text: {e}")

        return jsonify({'status': 'error in read_new_moderation_request', 'text': f'{e}'})
