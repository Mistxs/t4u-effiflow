from flask import Blueprint, request, jsonify
import requests
import json
import datetime
from config import yakey

tsearch = Blueprint('tsearch', __name__)

@tsearch.route('/search', methods=['POST'])
def search():
    text = request.args.get('text')
    data = yasearch(text)  # Ваш список словарей
    count = yacount(text)
    return jsonify({'data': data, 'count': count, 'statuses': list(set([item['status'] for item in data]))})

def yasearch(value):
    print(value)
    url = "https://api.tracker.yandex.net/v2/issues/_search?perPage=1000"
    payload = json.dumps({
            "query": value
        })
    headers = {
        'Authorization': f'{yakey}',
        'X-Org-ID': '167455',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    keys = [item["key"] for item in response]
    description = [item["summary"] for item in response]
    status = [item["status"]["display"] for item in response]
    count = len(keys)
    # data = [{"key": key, "summary": description} for key, description in zip(keys, description)]
    data = [{"key": f"<a href='https://tracker.yandex.ru/{key}' target='_blank'>{key}</a>", "summary": description, "status": status} for key, description, status in zip(keys, description, status)]

    return data


def yacount(value):
    url = "https://api.tracker.yandex.net/v2/issues/_count"
    payload = json.dumps({
        "query": value
    })

    headers = {
        'Authorization': f'{yakey}',
        'X-Org-ID': '167455',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response
