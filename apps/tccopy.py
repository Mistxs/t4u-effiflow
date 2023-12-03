import requests
from tqdm import tqdm
from config import headers,secretkey
from flask import Blueprint, request, jsonify
import urllib.parse

from concurrent.futures import ThreadPoolExecutor


tccopy = Blueprint('tccopy', __name__)

@tccopy.route('/copytcard', methods=['POST'])
def copytcard():
    try:
        dataset = request.json['dataset']
        data = startCopy(dataset["salon_from"], dataset["salon_to"])
        return jsonify({'status': 'success', "dataset" : "Success"})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})


def savecard(data, output_salon):
    for cards in tqdm(data):
        url = f"https://yclients.com/technological_cards/save/{output_salon}/0"

        payload_items = []
        for index, item in enumerate(cards['items']):
            good_name_encoded = urllib.parse.quote_plus(item["good_title"], encoding='utf-8')
            payload_items.append(
                f'card_items[new_{index}][good]={good_name_encoded}&card_items[new_{index}][good_id]={item["good_id"]}&card_items[new_{index}][storage_id]={item["storage_id"]}&card_items[new_{index}][amount]={item["amount"]}')

        title_encoded = urllib.parse.quote_plus(cards['title'], encoding='utf-8')
        # comment_encoded =

        payload = '&'.join(payload_items) + f'&comment=&title={title_encoded}'

        headers = {
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'X-Yclients-Application-Platform': 'legacy JS-1.0',
            'X-Yclients-Application-Name': 'biz.erp.web',
            'X-Yclients-Application-Version': '1.0.0',
            'X-Yclients-Application-Action': 'technological_cards_edit',
            'sec-ch-ua-mobile': '?0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"macOS"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'host': 'yclients.com'}
        print(payload)
        response = requests.request("POST", url+secretkey, headers=headers, data=payload)

        print(response.text)


def getcard(salon):
    url = f"https://api.yclients.com/api/v1/technological_cards/{salon}/?count=1000"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    carddata = []
    for item in response["data"]:
            good_item = []
            print(item)
            for goods in item['technological_card_items']:
                good_item.append({
                    "good_id": goods['good_id'],
                    "storage_id": goods['storage_id'],
                    "amount": goods['amount'],
                    "good_title": goods["good"]["title"]
                })
            carddata.append({
                "title": item['title'],
                "items": good_item
            })

    return carddata



def getNewGood(title,output_salon):
    good_name_encoded = urllib.parse.quote_plus(title, encoding='utf-8')
    url = f"https://api.yclients.com/api/v1/goods/{output_salon}?term={good_name_encoded}"
    response = requests.request("GET", url, headers=headers).json()
    for item in response['data']:
        if item['title'] == title:
            cat = item.get('good_id', '')
            return cat

def getNewStorage(storage,input_salon,output_salon):
    url1 = f"https://api.yclients.com/api/v1/storages/{input_salon}"
    url2 = f"https://api.yclients.com/api/v1/storages/{output_salon}"
    response = requests.request("GET", url1, headers=headers).json()


    for item in response['data']:
        if item["id"] == storage:
            target_title = item["title"]
            response2 = requests.request("GET", url2, headers=headers).json()
            for item2 in response2["data"]:
                if item2["title"] == target_title:
                    return item2['id']


    cat = response.get('data', [])[0].get('good_id', '')
    return cat


def getDataNewSalon(storage, goodTitle,input_salon,output_salon):
    storage_id = getNewStorage(storage,input_salon,output_salon)
    good_id = getNewGood(goodTitle,output_salon)
    return storage_id, good_id

def startCopy(input_salon, output_salon):
    data = getcard(input_salon)
    for item in data:
        for k in item["items"]:
            storage = k["storage_id"]
            good_title = k["good_title"]
            k["storage_id"], k["good_id"] = getDataNewSalon(storage, good_title,input_salon,output_salon)
    savecard(data,output_salon)

