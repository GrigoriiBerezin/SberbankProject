import json
import os
import logging

import requests

URL = "http://127.0.0.1:8000/api/v1/messages/"
logging.basicConfig(level=logging.DEBUG)


def format_message(message: dict) -> dict:
    return {
        "url": message.get("URL"),
        "name": message.get("Название", "Без названия"),
        "content": message.get("Текст сообщения"),
        "createdAt": message.get("Дата сообщения").replace(", ", " ")
    }


if __name__ == '__main__':
    for json_file in filter(lambda x: x.endswith(".json"), os.listdir()):
        logging.debug(f"reading file {json_file}...")
        with open(json_file, "r", encoding="utf-8") as file:
            messages = json.loads(file.read())
            logging.debug(f"messages count: {len(messages)}")
            for formatted_message in map(format_message, messages):
                logging.debug(f"sending on {URL} body: {formatted_message}")
                response = requests.post(URL, data=formatted_message)
                logging.debug(f"response status: {response.status_code.real}")
