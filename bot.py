import time
from pathlib import Path

import requests
from dotenv import dotenv_values

FOLDER = Path(__file__).resolve().parent
config = {}
HELP = "Привет! Бот для поиска авиабилетов. Сейчас доступны /start и /help."


def telegram(method, data):
    """Сделать запрос к API Telegram."""
    url = "https://api.telegram.org/bot" + config["TELEGRAM_BOT_TOKEN"] + "/" + method
    response = requests.post(url, json=data, timeout=20)
    if response.status_code != 200:
        raise ValueError("Telegram недоступен. Код: " + str(response.status_code))
    answer = response.json()
    if not answer.get("ok"):
        raise ValueError("Telegram не выполнил запрос.")
    return answer["result"]

def send(chat_id, text):
    telegram("sendMessage", {"chat_id": chat_id, "text": text})


def handle_message(message):
    """Обработать текстовые команды в личном чате."""
    if message["chat"]["type"] != "private":
        return
    text = message.get("text", "").strip()
    if not text:
        return
    chat_id = message["chat"]["id"]
    if text.split()[0] in ("/start", "/help"):
        send(chat_id, HELP)
    else:
        send(chat_id, "Поиск маршрутов добавим на следующем этапе. Отправь /help.")
