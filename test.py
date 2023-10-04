import requests
import re
def magicSearch(keywords):
    url = f"https://t4u.rety87nm.ru/search?text={keywords}"
    response = requests.request("POST", url).json()
    opentask = []
    for item in response["data"]:
        if item["status"] == "Беклог":
            key = item["key"]
            opentask.append({
                "key":key,
                "text":item["summary"]
            })
    return opentask

def formattedMessage(opentask):
    message = ""
    for task in opentask:
        key = re.search(r"<a.*?>(.*?)</a>", task["key"]).group(1)
        link = re.search(r"href='(.*?)'", task["key"]).group(1)
        text = task["text"]

        message += f"<{link}|{key}> {text}\n"
    return message

text = input()
tasks = magicSearch(text)
message = formattedMessage(tasks)

print(message)