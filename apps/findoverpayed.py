import requests
import json
from config import headers

from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, request, jsonify

overpay = Blueprint('overpayed', __name__)

@overpay.route('/findoverpayed', methods=['POST'])
def overpayed():
    try:
        dataset = request.json['dataset']
        data = getTransactions(dataset["salon_id"], dataset["start_date"], dataset["end_date"])
        return jsonify({'status': 'success', "dataset" : data})
    except Exception as e:
        return jsonify({'status': 'error', 'text': f'{e}'})

def checkDocuments(salon, docid):
    url = f"https://api.yclients.com/api/v1/company/{salon}/sale/{docid}"
    response = requests.request("GET", url, headers=headers).json()

    if response["data"] is not None:
        tt_services = []
        services = response["data"]["state"]["items"]
        payments = response["data"]["state"]["payment_transactions"]
        loyalty = response["data"]["state"]["loyalty_transactions"]
        sumItems = 0
        sumPayments = 0
        sumLoyalty = 0
        overpay = 0
        for item in services:
            sumItems += item["cost_to_pay_total"]
            tt_services.append(item["id"])

        for item in payments:
            sumPayments += item["amount"]
            if item["sale_item_id"] == None:
                overpay = item["amount"]
                return overpay

        for item in loyalty:
            if item["sale_item_id"] in tt_services:
                sumLoyalty += item["amount"]

        if sumLoyalty + sumPayments != sumItems:
            overpay = sumLoyalty + sumPayments - sumItems
            return overpay

def getTransactions(salon, startdate, enddate):
    url = f"https://api.yclients.com/api/v1/transactions/{salon}"
    data = []
    payload = json.dumps({
        "start_date": startdate,
        "end_date": enddate,
        'count': 1000
    })
    response = requests.request("GET", url, headers=headers, data=payload).json()
    lenght = len(response["data"])

    if lenght > 999:
        raise Exception("Вероятность пропуска транзакций, уменьши период")

    transactions = response["data"]
    def process_item(item):
        if item["expense"]["id"] != 11:
            if checkDocuments(salon,item["document_id"]):
                overpay = checkDocuments(salon,item["document_id"])
                transactionLink = f'''<a target=_blank href='https://yclients.com/finances/transactions/edit/{salon}/{item["id"]}'>{item["id"]}</a>'''
                date = item.get("date","")
                date_for_link = date.split("T")[-2]
                date_link = f'<a target=_blank href="https://yclients.com/timetable/{salon}#main_date={date_for_link}&open_modal_by_record_id={item["record_id"]}">{item["record_id"]}</a>'
                data.append({
                    "id": transactionLink,
                    "date": item["date"],
                    "amount": item["amount"],
                    "record_id": date_link,
                    "overpay": overpay
                })

    with ThreadPoolExecutor() as executor:
        executor.map(process_item, transactions)

    return data
