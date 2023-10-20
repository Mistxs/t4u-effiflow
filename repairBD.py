import re
import json
from config import headers
import requests
from concurrent.futures import ThreadPoolExecutor

def parse_sql_string(sql_string):
    pattern = r"WHERE id = (\d+);"
    match = re.search(pattern, sql_string)
    if match:
        client_id = match.group(1)
    else:
        client_id = None

    bd_day_pattern = r"bd_day = (\d+)"
    bd_month_pattern = r"bd_month = (\d+)"
    bd_year_pattern = r"bd_year = (\d+)"
    match_day = re.search(bd_day_pattern, sql_string)
    match_month = re.search(bd_month_pattern, sql_string)
    match_year = re.search(bd_year_pattern, sql_string)
    if match_day and match_month and match_year:
        birth_date = "{:4d}-{:02d}-{:02d}".format(int(match_year.group(1)), int(match_month.group(1)), int(match_day.group(1)))
    else:
        birth_date = None

    phone_pattern = r"phone = '(\d+)'"
    match_phone = re.search(phone_pattern, sql_string)
    if match_phone:
        phone = match_phone.group(1)
    else:
        phone = None

    name_pattern = r"fullname = '([^']+)'"
    match_name = re.search(name_pattern, sql_string)
    if match_name:
        name = match_name.group(1)
    else:
        name = None

    patronymic_pattern = r"patronymic = '([^']+)'"
    match_patronymic = re.search(patronymic_pattern, sql_string)
    if match_patronymic:
        patronymic = match_patronymic.group(1)
    else:
        patronymic = None

    surname_pattern = r"surname = '([^']+)'"
    match_surname = re.search(surname_pattern, sql_string)
    if match_surname:
        surname = match_surname.group(1)
    else:
        surname = None

    result = []
    if client_id and birth_date:
        result = {'clientid': int(client_id), 'birthdate': birth_date, 'phone': phone, 'name': name, 'patronymic': patronymic, 'surname': surname}

    return result

json_result = []
# Открываем файл для чтения
with open('input.sql', 'r', encoding='utf-8') as file:
    # Читаем строки файла поочередно
    for sql_string in file:
        json_result.append(parse_sql_string(sql_string))

print(json_result)

client = [{'clientid': 194368529, 'birthdate': '2012-09-22', 'phone': '79035801616', 'name': 'Бобиков Андрей', 'patronymic': None, 'surname': None}]

def saveResult(salon, data, headers):
    headers['Authorization'] = f'93z5f8fmhcydaa2pj4ca, 2c996af6cb4fd4dc8b33f119f831aae8'

    def process_item(item):
        url = f'https://api.yclients.com/api/v1/client/{salon}/{item["clientid"]}'
        payload = json.dumps({
            "id": item['clientid'],
            "name": item['name'],
            "patronymic": item['patronymic'],
            "phone": item['phone'],
            "surname": item['surname'],
            "birth_date": item['birthdate']

        })
        response = requests.request("PUT", url, headers=headers, data=payload)

    with ThreadPoolExecutor() as executor:
        executor.map(process_item, data)

saveResult(249274, json_result, headers)