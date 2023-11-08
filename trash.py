from slack_sdk import WebClient
import json
from config import slack_user_token
import codecs


def search_in_slack(slack_token, query):
    # Создание экземпляра WebClient с использованием токена авторизации Slack
    client = WebClient(token=slack_token)

    # Выполнение поиска по запросу
    response = client.search_messages(query=query)

    # Форматирование результатов поиска в JSON
    search_results = []
    for message in response["messages"]["matches"]:
        text = codecs.decode(message["text"].decode('unicode_escape'))
        result = {
            "text": text,
            "user": message["user"],
            "channel": message["channel"]["name"],
            "timestamp": message["ts"],
        }
        search_results.append(result)

    # Загрузка результата поиска в формате JSON
    json_results = json.dumps(search_results)
    # decoded_results = codecs.decode(json_results.encode('utf-8'), 'unicode_escape').decode('utf-8')
    # Возвращение результатов поиска в формате JSON
    return json_results



query = "facebook"

result = search_in_slack(slack_user_token, query)
print(result)