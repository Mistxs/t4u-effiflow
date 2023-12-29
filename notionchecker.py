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
        select * from notion_database;
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

        for item in new_data:
            cursor.execute("SELECT * FROM notion_database WHERE id = %s", (item['id'],))
            existing_data = cursor.fetchone()

            if existing_data:
                # Если запись существует, обновляем ее
                update_query = """
                    UPDATE notion_database
                    SET title = %s, status = %s, last_edited_time = %s, link = %s
                    WHERE id = %s
                """
                cursor.execute(update_query, (item['title'], item['status'], item['last_edited_time'], item['link'], item['id']))
            else:
                # Если записи нет, вставляем новую запись
                insert_query = """
                    INSERT INTO notion_database (title, status, last_edited_time, id, link)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (item['title'], item['status'], item['last_edited_time'], item['id'], item['link']))

        # Завершаем транзакцию и закрываем соединение
        conn.commit()
        cursor.close()
        conn.close()
        print("Данные успешно синхронизированы с базой данных")

    except Exception as error:
        print("Ошибка при синхронизации данных:", error)

def checkUpdates():
    newdata = getmoderationList()
    currentdata = get_from_notion_database()
    if newdata == currentdata:
        print("OK")
    else:
        synchronize_with_database(newdata)

checkUpdates()

