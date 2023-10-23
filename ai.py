from config import openaikey
import openai
import pymysql
from tqdm import tqdm

db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ose7vgt5',
    'db': 'superbar'
}

openai.api_key = openaikey

connection = pymysql.connect(**db_params)

def loadtickets():
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()
        sql = "select distinct(eddy_id), description from tickets_info limit 1000"
        cursor.execute(sql)
        conn.commit()
        response = cursor.fetchall()
        conn.close()

        tickets = []
        for row in response:
            eddy_id = row[0]
            description = row[1]
            ticket = {"eddy_id": eddy_id, "description": description}
            tickets.append(ticket)

        return tickets

    except pymysql.Error as error:
        print("Failed to load tickets from database:", error)

def chat_with_model(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты умеешь находить главное в текстах"},
            {"role": "system", "content": "Твоя подготовить ответ так, чтобы по нему можно было найти баг в бэклоге"},
            {"role": "user", "content": "Напиши основную мысль текста в двух словах: "},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def update_tables(id,words):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()
        sql = f'''update tickets_info set keyword_v1 = '{words}' where eddy_id = {id};'''
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return "OK"
    except pymysql.Error as error:
        print("Failed to update tickets from database:", error)

lists = loadtickets()


for item in tqdm(lists):
    preProcessing = chat_with_model(item["description"])
    update_tables(item["eddy_id"],preProcessing)


