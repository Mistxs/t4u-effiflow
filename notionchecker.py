import pymysql

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
        cursor.execute("SELECT * FROM notion_database")
        existing_data = cursor.fetchall()

        # Получаем список id существующих записей в базе данных
        existing_ids = set(row[3] for row in existing_data)

        for item in new_data:
            if item['id'] in existing_ids:
                # Запись существует в базе данных, обновляем ее значения
                update_query = """
                    UPDATE notion_database
                    SET title = %s, status = %s, last_edited_time = %s, link = %s
                    WHERE id = %s
                """
                cursor.execute(update_query, (item['title'], item['status'], item['last_edited_time'], item['link'], item['id']))
            else:
                # Запись отсутствует в базе данных, вставляем новую запись
                insert_query = """
                    INSERT INTO notion_database (title, status, last_edited_time, id, link, deleted)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (item['title'], item['status'], item['last_edited_time'], item['id'], item['link'], False))

        # Помечаем как удаленные записи, которых нет в новых данных
        deleted_ids = existing_ids - set(item['id'] for item in new_data)
        for deleted_id in deleted_ids:
            cursor.execute("UPDATE notion_database SET deleted = True WHERE id = %s", (deleted_id,))

        # Завершаем транзакцию и закрываем соединение
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as error:
        print("Ошибка при синхронизации данных:", error)


def checkUpdates():
    newdata = getmoderationList()
    print(newdata)
    currentdata = get_from_notion_database()
    print(currentdata)
    if newdata != currentdata:
        print("ne ok")
        synchronize_with_database(newdata)


checkUpdates()

