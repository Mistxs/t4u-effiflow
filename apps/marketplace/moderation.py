import requests
import json
from apps.marketplace.src.newpageblocks import blocks
from config import NOTION_TOKEN, ntn_db_id



default_params = {
    "parnter_name": "test4",
    "status": "Новый",
    "slack_url": "https://yclients-dev.slack.com/archives/C03V39JQJF5/p1699532227677849",
    "dev_url": "https://yclients.com/appstore/developers/3/4785/general_info/",
    "app_url": "https://yclients.com/e/mp_4785_wahelpzadachi/",
    "statusdict": ["Новый", "Автопроверка","Ручная проверка","В процессе","Ожидание партнера","Повторная проверка","Успешно"]
}


def createNewPage(payloadparams,content=blocks):
    try:
        url = "https://api.notion.com/v1/pages"

        payload = json.dumps({
            "parent": {
                "database_id": ntn_db_id
            },
            "properties": {
                "Имя партнера": {
                    "title": [
                        {
                            "text": {
                                "content": payloadparams["parnter_name"]
                            }
                        }
                    ]
                },
                "Статус": {
                    "select": {
                        "name": payloadparams["status"]
                    }
                },
                "Ссылка на Slack": {
                    "url": payloadparams["slack_url"]
                },
                "Ссылка на кабинет разработчика": {
                    "url": payloadparams["dev_url"]
                },
                "Ссылка на приложение": {
                    "url": payloadparams["app_url"]
                }
            },

            "children": content
        })

        headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise Exception(f"Error in post page. Notion response: {response.text}")
        print(response)
    except Exception as e:
        raise e

