import requests
from tqdm import tqdm
from config import headers
import urllib.parse

input_salon = 758849
output_salon = 867328



def savecard(data):
    for cards in tqdm(data):
        url = f"https://yclients.com/technological_cards/save/{output_salon}/0"

        payload_items = []
        for index, item in enumerate(cards['items']):
            good_name_encoded = urllib.parse.quote_plus(item["good_title"], encoding='utf-8')
            payload_items.append(
                f'card_items[new_{index}][good]={good_name_encoded}&card_items[new_{index}][good_id]={item["good_id"]}&card_items[new_{index}][storage_id]={item["storage_id"]}&card_items[new_{index}][amount]={item["amount"]}')

        title_encoded = urllib.parse.quote_plus(cards['title'], encoding='utf-8')

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
            'Cookie': '__ddg1_=exsBazo8eGkna9M9Uomc; __utma=143647594.1928824817.1674055633.1689936300.1689936300.1; __utmz=143647594.1689936300.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _cmg_csst1lPaz=1678712167; _comagic_id1lPaz=6941324878.10216608865.1678712167; _fbp=fb.1.1681128751602.1057597157; _ga_6EVFCY524B=GS1.1.1681134483.7.0.1681134486.0.0.0; _ga_6HM2D67C72=GS1.1.1688584993.2.0.1688584993.60.0.0; _ga_DQPQ734JS8=GS1.2.1688137041.3.1.1688138051.60.0.0; _ga_EMDSRZNPWN=GS1.1.1686922592.3.0.1686922592.0.0.0; _ga_RK4DYY87HR=GS1.1.1688572806.3.0.1688572806.60.0.0; _gcl_au=1.1.2124500160.1689798607; _ym_d=1689838624; _ym_uid=1674055633835203884; adrcid=AWjpZrOjq6FN88BP4tS2H8A; analytics-udid=d4KtI8cmnlKw5KusIoRO1dcgC500YFH6ZCu3lnpP; browser_lang=ru; landing_lang=ru; tmr_lvid=35025bf4d92d6dc445d8f77c6cd09cfd; tmr_lvidTS=1674055632559; yc_referer_full=https%3A%2F%2Fwww.yclients.com%2F; yc_utm_medium=referral; yc_utm_source=https%3A%2F%2Fwww.yclients.com%2F; ycl_language_id=1; x-feature-waiting-room-web=1; lang=1; erp_language_id=1; original_utm_source_v2=(direct); original_utm_medium_v2=(none); original_utm_campaign_v2=(not_set); original_utm_term_v2=(not_set); original_utm_referer_v2=(not_set); yc_utm_campaign=; yc_utm_content=; yc_utm_term=; yc_utm_click_id=; tracking-index=3461; _gid=GA1.2.1592518728.1695729521; app_service_group=9; _ga_CZ0CKD8R74=GS1.1.1695739281.2.0.1695739281.0.0.0; _cfuvid=BbYRBg7s7ZVoJeXGdnZmXCFgb7nlagx0.lrPnpuV0RA-1695800315348-0-604800000; _ym_isad=2; tmr_detect=0%7C1695808377414; _ga=GA1.1.1928824817.1674055633; _ga_4Z5R7DZBLZ=GS1.2.1695808270.21.1.1695808379.13.0.0; auth=u-11946640-77d53a568198450abfeeb; yc_user_id=11946640; _ga_P2LM7D8KSM=GS1.1.1695808269.54.1.1695808415.60.0.0; _ga_3M9TPBMV14=GS1.1.1695808269.26.1.1695808415.60.0.0; _ga_X3P164PV59=GS1.1.1695808269.21.1.1695808415.60.0.0; cf_clearance=lH1AoWvvx3SP27dwTKgB_mllEj4y5z82dnZE2dHkNyo-1695811801-0-1-e5c4913d.4383478b.33fa8b05-0.2.1695811801; __cf_bm=kN0QCy0wqbKT6d1GvU7wwbCE9g5F2_9LhP4hpGS5C.s-1695812912-0-ATWJWDYUbQIERkyMeLaBVHQ1+ZMj1W8dzrg8a6L6tOL0eilJQLrnPo0ztIGezs7eMlw2VzI71XhTHQFTvFn5HDQ=; yc_company_id=908361; yc_referral_url=https%3A%2F%2Fyclients.com%2Fstorages%2Fstorages%2Flist%2F908361; __cfwaitingroom=ChhQYUJFV2pPOUgyNmVpRTBOeXJ0UmxRPT0SrAIzb2RZUmJjOEhOam1jekhycjZBazMrV2g2aWcxWk1jM3drakM3Q25LSC96MlpHQXJYNGNjWFA2L3NSWjlvUituMVlwUjJENmtBU05neWE5NWpNSVk1REUzdmVPSGZvOEgrVE9FY1Qxcmo0K0JnNytWYWR6S00vZHlCYUFuZURLb1NCRWJkaCtTZEVPajc4TlNyOWcvWFNTMTVJall2VlF0OEltdm9Qc3NWUk5WRUZwYjhXY1kyOXA1bkNEZmhmUGJHN21OMXhRakEvZllNWFAzN3NuNFN1RGo5bTUrdDhMbHdIOU1QcGQrTVp0eUVlbkhBb3V5MkN3VElXZm9RdGJOc2VlN25xRG9EYzYwcXVZbStuamwvOHAzL1Z0eWZ5bE5XN3FnRVNMZnV0bz0%3D'
        }
        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


def getcard(salon):
    url = f"https://api.yclients.com/api/v1/technological_cards/{salon}/?count=1000"

    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    carddata = []
    # cards = [248753,248754,248765,248767,248768,248769,248801,248813,248815,465756]
    # cards = [248752]
    for item in response["data"]:
        # if item['id'] in cards:
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
    good_name_encoded = urllib.parse.quote_plus(title, encoding='utf-8')
    url = f"https://api.yclients.com/api/v1/goods/{output_salon}?term={good_name_encoded}"
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


savecard(data)
