import re
import threading
import time
from datetime import datetime

import requests
import concurrent.futures
import pymysql
from bs4 import BeautifulSoup
from multiprocessing import Pool




headers = {
    'Authorization': 'Basic cC5wb3BvdmFAeWNsaWVudHMudGVjaDphOTk3YzU5Mi02ZGU3LTRhMDUtYTc3ZC1kYjUwNzJmZjZiNjk=',
}


db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ose7vgt5',
    'db': 'superbar'
}


connection = pymysql.connect(**db_params)

def getTickets(page):
    result = []
    # time.sleep(0.5)
    url = f"https://yclients.helpdeskeddy.com/api/v2/tickets/?department_list=7&page={page}"
    print(url)
    response = requests.request("GET", url, headers=headers).json()
    count = response["pagination"]["total"]
    totalpages = response["pagination"]["total_pages"]
    for ticket_id, ticket in response["data"].items():
        # time.sleep(0.5)
        drafttext = getTicketInfo(ticket_id)
        clearText = clearTicket(drafttext)
        tracker_id = ''
        tracker_description = ''
        for fields in ticket["custom_fields"]:
            if fields["id"] == 25 and fields["field_value"] != "":
                tracker_id = fields["field_value"]
                tracker_description = yandex(tracker_id)
        result.append({
            "eddy_id": ticket["id"],
            "description": clearText,
            "tracker_id" : tracker_id,
            "tracker_title": tracker_description
        })

        # time.sleep(0.4)  # Добавляем задержку 0.2 секунды перед каждым запросом
    saveTickets(result)
    return result


def saveTickets(tickets):
    try:
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()
        for ticket in tickets:
                sql = "INSERT IGNORE INTO tickets_info (eddy_id, tracker_id, description, tracker_title) VALUES (%s, %s, %s, %s)"
                values = (ticket["eddy_id"], ticket["tracker_id"],  ticket["description"], ticket["tracker_title"])
                cursor.execute(sql, values)
        conn.commit()
        conn.close()
        print("Tickets saved to database successfully!")
    except pymysql.Error as error:
        print("Failed to save tickets to database:", error)

def yandex(issue):
    try:
        url = f"https://api.tracker.yandex.net/v2/issues/{issue}"
        print(url)
        payload = {}
        headers = {

            'Authorization': 'OAuth y0_AgAEA7qiLv7tAAg9bgAAAADl015VJPztpzEaTDat1gvNxxZ3lSjg02k',
            'X-Org-ID': '167455',
            'Content-Type': 'application/json',
            'Cookie': 'uid=blUAAGU1tECuIgDnDfb8Ag=='
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response["summary"]
    except:
        return "error"

def getTicketInfo(ticket):
    url = f"https://yclients.helpdeskeddy.com/api/v2/tickets/{ticket}/posts"
    print(url)
    headers = {
        'Authorization': 'Basic cC5wb3BvdmFAeWNsaWVudHMudGVjaDphOTk3YzU5Mi02ZGU3LTRhMDUtYTc3ZC1kYjUwNzJmZjZiNjk='
    }
    response = requests.request("GET", url, headers=headers).json()
    # print(response)
    posts = response["data"]
    # Проверяем, что есть хотя бы одно сообщение
    if len(posts) == 0:
        print("Сообщений не найдено")
        return None
    # Находим сообщение с самой ранней датой создания
    min_date_created = datetime.now()  # Инициализируем сегодняшней датой
    min_post_text = ""
    for post in posts:
        date_created = datetime.strptime(post["date_created"],
                                                  "%H:%M:%S %d.%m.%Y")  # Преобразуем строку в datetime
        if date_created < min_date_created:
            min_date_created = date_created
            min_post_text = post["text"]
    # print(f"Результат работы getTicketInfo: {min_post_text}")
    return min_post_text

def clearTicket(text):
    draft_text = text
    start_index = draft_text.find("Проблема с технической точки зрения") + len("Проблема с технической точки зрения: ")
    second_start_index = draft_text.find("Описание проблемы") + len("Описание проблемы: ")
    output_text = draft_text[start_index:] if start_index > second_start_index else draft_text[second_start_index:]
    soup = BeautifulSoup(output_text, "html.parser")
    text_without_links = soup.get_text().strip()
    pattern = r"http[s]?://\S+"
    result = re.sub(pattern, "", text_without_links)
    result = result.strip()
    # print(f"Результат работы clearTicket: {result}")
    return result

for i in range (989, 2116):
    getTickets(i)


# if __name__ == "__main__":
#
#     pool = Pool()  # Создаем пул процессов
#     pages = range(1, 2116)  # Список страниц
#     results = pool.map(getTickets, pages)  # Вызываем функцию getTickets с каждой страницей в пуле процессов
#     pool.close()
#     pool.join()  # Дожидаемся завершения всех процессов
#     for result in results:
#         saveTickets(result)





