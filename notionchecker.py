import time

import pymysql
import requests

from apps.marketplace.moderation import getPagesfromNotion, formatNotionData
from config import db_params


def getmoderationList():
    pages = getPagesfromNotion()
    lists = formatNotionData(pages)
    return lists

def insert_into_notion_database(data):

    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        # Подготовьте запрос на вставку данных в таблицу
        query = """
            INSERT INTO notion_database (title, status, last_edited_time, id, link)
            VALUES (%s, %s, %s, %s, %s)
        """

        # Выполните запрос с данными из списка
        for item in data:
            cursor.execute(query, (item['title'], item['status'], item['last_edited_time'], item['id'], item['link']))

        # Завершите транзакцию и закройте соединение
        conn.commit()
        cursor.close()
        conn.close()
        print("Данные успешно добавлены в базу данных")

    except Exception as error:
        print("Ошибка при вставке данных:", error)

def get_from_notion_database():
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = f"""
        select title, status, last_edited_time, id, link from notion_database where deleted = 0;
        """
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error in get_from_DB: {e}")

def synchronize_with_database(new_data):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        # Получаем все записи из базы данных
        cursor.execute("select title, status, last_edited_time, id, link from notion_database where deleted = 0;")
        existing_data = cursor.fetchall()

        # Получаем список id существующих записей в базе данных
        existing_records = {row[3]: dict(zip(['title', 'status', 'last_edited_time', 'id', 'link', 'deleted'], row)) for row in existing_data}
        changed_entities = []

        for item in new_data:
            existing_record = existing_records.get(item['id'])
            if existing_record:
                # Запись существует в базе данных, проверяем, изменились ли данные
                if existing_record != item:
                    # Данные изменились, обновляем запись в базе данных
                    update_query = """
                        UPDATE notion_database
                        SET title = %s, status = %s, last_edited_time = %s, link = %s
                        WHERE id = %s
                    """
                    cursor.execute(update_query, (item['title'], item['status'], item['last_edited_time'], item['link'], item['id']))
                    changed_entities.append(item)
            else:
                # Запись отсутствует в базе данных, вставляем новую запись
                insert_query = """
                    INSERT INTO notion_database (title, status, last_edited_time, id, link, deleted)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (item['title'], item['status'], item['last_edited_time'], item['id'], item['link'], False))
                changed_entities.append(item)
        # Помечаем как удаленные записи, которых нет в новых данных
        deleted_ids = set(existing_records.keys()) - set(item['id'] for item in new_data)
        for deleted_id in deleted_ids:
            cursor.execute("UPDATE notion_database SET deleted = True WHERE id = %s", (deleted_id,))
            changed_entities.append({'id': deleted_id, 'deleted': True})

        # Завершаем транзакцию и закрываем соединение
        conn.commit()
        cursor.close()
        conn.close()
        if changed_entities:
            generateHooks(changed_entities)


    except Exception as error:
        print("Ошибка при синхронизации данных:", error)

def generateHooks(changed_entities):
    url = "https://t4u.rety87nm.ru/marketplace/notion/hooks"
    response = requests.post(url, json=changed_entities)

    if response.status_code != 200:
        print(f"Ошибка при отправке webhook: {response.status_code} - {response.text}")


def checkUpdates():
    newdata = getmoderationList()
    currentdata = get_from_notion_database()
    if newdata != currentdata:
        synchronize_with_database(newdata)


checkUpdates()

