import requests
from tqdm import tqdm
from urllib.parse import quote

input_salon = 175262
output_salon = 895975



headers = {
    'Accept': 'application/vnd.yclients.v2+json',
    'Content-Type': 'application/json',
    'Authorization': 'rj257pguzmdk9fgaz8cr, e69793634796c00b57cb4bfd34f361d8',
    'Cookie': '__cf_bm=DpSJxFcP5x49BlwSV8fx7HA3Gk3yq2.xbqLx0eCWc0o-1693478558-0-AfLG/u6lL3HhMTKdAvxgnJG8Sca9wA6nbu7z783gyKV7VssaycYBpBHbKy8Mrz2prG2Oo3uNLEcNR10AHblnzH0=; _cfuvid=15nbJ8Gw2X16Drnvx8LFVcGFMrq2IIZ4Ib2TPJ3Hv.M-1693478558393-0-604800000; app_service_group=9; auth=hpa9rgcnut92h45ess4h7r42vcaf106r9p9rdtv2d06p70jcbhqrdpeqr3e7rmc7; ycl_language_id=1'
}


def savecard(data):
    for cards in tqdm(data):
        url = f"https://yclients.com/technological_cards/save/{output_salon}/0"

        payload_items = []
        for index, item in enumerate(cards['items']):
            good_name_encoded = quote(item["good_title"], safe='')
            payload_items.append(
                f'card_items[new_{index}][good]={good_name_encoded}&card_items[new_{index}][good_id]={item["good_id"]}&card_items[new_{index}][storage_id]={item["storage_id"]}&card_items[new_{index}][amount]={item["amount"]}')

        title_encoded = quote(cards['title'], safe='')

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
            'host': 'yclients.com',
            'Cookie': '_gcl_au=1.1.1587250222.1690210968; _gid=GA1.2.401797508.1693215578; _ym_d=1690210968; _ym_uid=1690210968176861506; adrcid=AfD0aZtHF2yUcPnS4q3lhsQ; analytics-udid=UA9oUEI7W0mG6GaSmxsbmrc51fN23kDClJ1Mc1nO; browser_lang=ru; landing_lang=ru; tmr_lvid=d5b464eb90ba0d2418e59e80b26f8eb3; tmr_lvidTS=1690210968449; tracking-index=106; yc_referer_full=https%3A%2F%2Fwww.yclients.com%2F; yc_utm_medium=referral; yc_utm_source=https%3A%2F%2Fwww.yclients.com%2F; ycl_language_id=1; x-feature-waiting-room-web=1; tmr_detect=0%7C1693326144925; _ga=GA1.2.361283387.1690210968; _ga_4Z5R7DZBLZ=GS1.2.1693351919.13.1.1693351921.58.0.0; auth=u-11946640-e4de37c619cb4745981cf; yc_user_id=11946640; _ga_P2LM7D8KSM=GS1.1.1693351917.16.1.1693351924.53.0.0; _ga_3M9TPBMV14=GS1.1.1693351917.15.1.1693351924.53.0.0; _ga_X3P164PV59=GS1.1.1693351917.16.1.1693351924.53.0.0; yc_utm_campaign=; yc_utm_content=; yc_utm_term=; yc_utm_click_id=; app_service_group=9; __cf_bm=xAZTdrcVk.jwpI1zKgWsn5_xtJ7ot.4IKTWqaQL1R5g-1693390733-0-AYHHgehaSazXp4wE/RsvpN0QsNRHlmNJ3iR05maNaedeZD9nVluVVSO7/P25oo+c6C+yiTH6+avdY6vun9dOtas=; _cfuvid=b7fviRrKOSff9pN1HLDPWSIio9qFYS8WZHxZrLXro0M-1693390733910-0-604800000; cf_clearance=vp0D6S_RMbg_T91V.S9O4V9ILN3iMtDe3hw.G5YZeDs-1693390740-0-1-19fc3a48.6310fa93.56065ab0-0.2.1693390740; yc_company_id=892538; yc_referral_url=https%3A%2F%2Fyclients.com%2Ftechnological_cards%2F892538%3Fsearch_term%3D%26page%3D1%26editable_length%3D25; __cf_bm=I3NuABAo5D4ffAidzxngktIK0SFV2.TwTHGcJNBEolw-1693391969-0-AQFnCS8Km3Ztnwedp9uTQEpiIsX3r6sMPA+0RzT3rzcQ8vpyz8LWVsUuI6yzflI+CTRSVU+wr4fNG/p7VYiVUlg=; _cfuvid=TQhNSiiO4G2GOYmUJGTTl2G9VNhAkfpsbRmnsIXriGE-1693391935146-0-604800000; app_service_group=0; auth=hpa9rgcnut92h45ess4h7r42vcaf106r9p9rdtv2d06p70jcbhqrdpeqr3e7rmc7; ycl_language_id=1'
        }
        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


def getcard(salon):
    url = f"https://api.yclients.com/api/v1/technological_cards/{salon}/?count=1000"

    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    carddata = []
    for item in response["data"]:
        # if item['title'] == 'Комплекс 7 диодный лазер':
            good_item = []
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

data=(getcard(input_salon))

def getNewGood(title):
    url = f"https://api.yclients.com/api/v1/goods/{output_salon}?term={title}"
    response = requests.request("GET", url, headers=headers).json()
    for item in response['data']:
        if item['title'] == title:
            cat = item.get('good_id', '')
            return cat

def getNewStorage(storage):
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


def getDataNewSalon(storage, goodTitle):
    storage_id = getNewStorage(storage)
    good_id = getNewGood(goodTitle)
    return storage_id, good_id

# print(data)
#
for item in tqdm(data):
    for k in item["items"]:
        storage = k["storage_id"]
        good_title = k["good_title"]
        k["storage_id"], k["good_id"] = getDataNewSalon(storage, good_title)

# print(data)

savecard(data)

# print(getNewGood('Крем для рук'))