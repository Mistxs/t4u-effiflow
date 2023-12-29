from datetime import datetime
import pymysql
from config import db_params

# пока в трубу, так как нафига козе боян, а мне две одинаковые таблицы. выезжаю за счет notionchecker

#работа с БД
def insertIntoDB(data):
    try:

        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = """
        INSERT INTO effiflow.marketplace_moderation 
        (title, notion_id, status, prev_status, date_create, is_favourite, is_trash, deleted) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            data.get("title",""),
            data.get("notion_id",""),
            data.get("status",""),
            data.get("prev_status",""),
            data.get("date_create", datetime.strptime("1970-01-01 00:00:00","%Y-%m-%d %H:%M:%S")),
            data.get("is_favourite", False),
            data.get("is_trash", False),
            data.get("deleted", False)
        )

        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return
    except Exception as e:
        print(f"Error in insertIntoDB: {e}")

def get_from_DB(notion_id, moreexp = ""):
    try:

        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = f"""
        select * from marketplace_moderation where notion_id = '{notion_id}' {moreexp};
        """
        cursor.execute(query)
        conn.close()

        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error in get_from_DB: {e}")

def updateDB(notion_id, moreexp="is_favourite = False"):
    try:

        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        query = f"""
        update marketplace_moderation set {moreexp} where notion_id = '{notion_id}';
        """
        cursor.execute(query)
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error in updateDB: {e}")

