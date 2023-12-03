from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
from slack_sdk import WebClient
from config import headers, slack_token, secretkey

fsr = Blueprint('fsr', __name__)

baseurl = "https://yclients.com"

channel = "#innachannel"  # Замените на имя канала, в который хотите отправить сообщение

def send_slack_message(message):
    client = WebClient(token=slack_token)
    response = client.chat_postMessage(
        channel=channel,
        text=message
    )
    if response["ok"]:
        return True
    return False

def getdata(url):

    # Отправляем GET-запрос с передачей Cookie
    global document_id
    response = requests.get(url+secretkey)
    kkm_response = {}
    # Проверяем код состояния ответа (200 означает успешный запрос)
    if response.status_code == 200:
        html_content = response.text
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html_content, "html.parser")
        # Находим все элементы с классом "ibox-content"
        ibox_contents = soup.find_all("div", class_="ibox-content")
        # Находим все элементы <td> внутри таблицы
        td_elements = soup.find("table", class_="table").find_all("td")
        # Получаем содержимое нужного элемента <td> по индексу
        document_id = td_elements[1].get_text(strip=True)

        # Находим элемент <li> с классом "calendar-toggle"
        li_element = soup.find("li", class_="calendar-toggle")
        # Находим элемент <a> внутри элемента <li>
        a_element = li_element.find("a")
        # Получаем значение атрибута href
        href_value = a_element.get("href")
        # Извлекаем значение после префикса "/timetable/"
        salon_id = href_value.split("/timetable/")[1]
        # Вывод значения переменной value

        # Проверяем, есть ли второй блок
        if len(ibox_contents) >= 2:
            # Получаем второй блок с классом "ibox-content"
            second_block = ibox_contents[1]

            # Извлекаем текст из второго блока
            second_content = second_block.get_text(strip=True)
            kkm_response = json.loads(second_content)




        else:
            print("Не удалось найти второй блок с классом 'ibox-content'.")
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

    kkm_id = url.split("/")[-2]
    return kkm_id,kkm_response,document_id,salon_id

@fsr.route('/check_document', methods=['POST'])
def check_document():
    try:
        kkm_link = request.json['kkm_link']
        if not is_valid_link(kkm_link):
            return jsonify({'status': 'error', 'text': f'Некорректная ссылка'})
        return jsonify({'status': 'success', 'text': getdocumentstatus(kkm_link)})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})


@fsr.route('/run_force', methods=['POST'])
def run_force():
    try:
        kkm_link = request.json['kkm_link']
        if not is_valid_link(kkm_link):
            return jsonify({'status': 'error', 'text': f'Некорректная ссылка'})
        kkm, resp, document, salon_id = getdata(kkm_link)
        return jsonify({'status': 'success', 'text': execute_force(kkm, resp, salon_id)})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})


def is_valid_link(kkm_link):
    valid_prefix = f'{baseurl}/kkm/transactions/details/'
    return kkm_link.startswith(valid_prefix)

def getdocumentstatus(url):
    kkm, resp, document,salon_id = getdata(url)
    bpsatatus = {
        1: "Статус 1 - не напечатан чек",
        2: "Статус 2 - печатается чек продажи",
        3: "Статус 3 - напечатан чек продажи",
        4: "Статус 4 - печатается чек возврата",
        5: "Статус 5 - напечатан чек возврата"
    }
    url = f"{baseurl}/api/v1/company/{salon_id}/sale/{document}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    bps = response["data"]["kkm_state"]["transactions"][0]["document"]["bill_print_status"]
    return bpsatatus.get(bps)

def execute_force(kkm_id,kkm_response,salon):
    if "CheckNumber" in kkm_response:
        check = kkm_response["CheckNumber"]
    else:
        check = ""

    if "SessionNumber" in kkm_response:
        session = kkm_response["SessionNumber"]
    else:
        session = ""
    url = f"{baseurl}/api/v1/kkm_transactions/{kkm_id}/save_result"
    payload = json.dumps({
        "kkm_transaction_id": kkm_id,
        "result_check_number": check,
        "result_session_number": session,
        "status": 0,
        "error": "",
        "type": "sale",
        "sessionState": 0,
        "kkm_response": kkm_response
    })
    response = requests.request("POST", url, headers=headers, data=payload).json()
    message = f"Нажали исправить документ. KKMID: {kkm_id}, филиал {salon} "
    send_slack_message(message)
    return response

