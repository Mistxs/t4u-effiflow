#вспомогательный модуль для обработки тикетов из браузера (серверная часть расширения)



from flask import Blueprint, request, jsonify
from slack_sdk import WebClient

from apps.search import yasearch, yacount
from config import user_slack_token

import json
import datetime
import requests
import spacy
from bs4 import BeautifulSoup
import re
import codecs

superbar = Blueprint('superbar', __name__)
def getTicketInfo(ticket):
    url = f"https://yclients.helpdeskeddy.com/api/v2/tickets/{ticket}/posts"
    headers = {
        'Authorization': 'Basic cC5wb3BvdmFAeWNsaWVudHMudGVjaDphOTk3YzU5Mi02ZGU3LTRhMDUtYTc3ZC1kYjUwNzJmZjZiNjk='
    }
    response = requests.request("GET", url, headers=headers).json()
    posts = response["data"]

    # Проверяем, что есть хотя бы одно сообщение
    if len(posts) == 0:
        print("Сообщений не найдено")
        return None

    # Находим сообщение с самой ранней датой создания
    min_date_created = datetime.datetime.now()  # Инициализируем сегодняшней датой
    min_post_text = ""
    for post in posts:
        date_created = datetime.datetime.strptime(post["date_created"],
                                                  "%H:%M:%S %d.%m.%Y")  # Преобразуем строку в datetime
        if date_created < min_date_created:
            min_date_created = date_created
            min_post_text = post["text"]

    print(f"Результат работы getTicketInfo: {min_post_text}")
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
    print(f"Результат работы clearTicket: {result}")
    return result

def preProcessing(clearText):
    # Загрузка модели spaCy для русского языка
    nlp = spacy.load("ru_core_news_sm")

    # Обработка текста с помощью spaCy
    doc = nlp(clearText)

    # Извлечение подлежащего и сказуемого
    subject = ""
    predicate = ""

    for token in doc:
        # Находим первый глагол в тексте как сказуемое
        if token.pos_ == "VERB":
            predicate = token.text
            break

    # Извлекаем слова, предшествующие сказуемому, как подлежащее
    for token in doc:
        if token.text == predicate:
            break
        subject += token.text + " "

    # Удаляем лишние пробелы в начале и конце
    subject = subject.strip()

    key = f"{subject} {predicate}"
    print(f"результат работы spacy: {key}")
    return key

def magicSearch(keywords):
    url = f"https://t4u.rety87nm.ru/search?text={keywords}"
    response = requests.request("POST", url).json()
    opentask = []
    for item in response["data"]:
        if item["status"] == "Беклог":
            opentask.append(item)
    return opentask

def search_in_slack(query):
    client = WebClient(token=user_slack_token)
    response = client.search_messages(query=query, count=100, sort='score')
    search_results = []
    print(response)
    for message in response["messages"]["matches"]:
        result = {
            "text": message["text"],
            "link": message["permalink"],
            "user": message["user"],
            "channel": message["channel"]["name"],
            "timestamp": message["ts"],
        }
        search_results.append(result)
    return search_results

@superbar.route('/process_ticket', methods=['POST'])
def process_ticket():
    ticket_id = request.json['ticket_id']
    print(ticket_id)
    drafttext = getTicketInfo(ticket_id)
    clearText = clearTicket(drafttext)
    keySearch = preProcessing(clearText)
    # tasks = magicSearch(keySearch)
    # for task in tasks:
    #     print(task["summary"])

    response = {
        "clearticket": clearText,
        "preProcessing": keySearch
    }
    return jsonify(response)

@superbar.route('/supersearch', methods=['POST'])
def supSearch():
    text = request.args.get('text')
    yandexdata = yasearch(text)
    yandexcount = yacount(text)
    slackdata = search_in_slack(text)
    return jsonify({'yandexdata': yandexdata, 'count': yandexcount, 'statuses': list(set([item['status'] for item in yandexdata])), 'slackdata': slackdata})


