import time
from datetime import datetime, date
from pathlib import Path

import requests
from dotenv import dotenv_values

FOLDER = Path(__file__).resolve().parent
config = {}
dialogs = {}
cities = []
HELP = "Нажми «Создать парсер» или отправь /new. Введи города и дату. /cancel — отмена."


def telegram(method, data):
    """Отправить запрос Telegram и вернуть его результат."""
    url = "https://api.telegram.org/bot" + config["TELEGRAM_BOT_TOKEN"] + "/" + method
    response = requests.post(url, json=data, timeout=20)
    if response.status_code != 200:
        hints = {401: "Проверь TELEGRAM_BOT_TOKEN в .env.",
                 409: "Останови другие экземпляры бота; возможен также конфликт с webhook.",
                 429: "Слишком много запросов. Повтори позже."}
        raise ValueError("Telegram: HTTP " + str(response.status_code) + ". " + hints.get(response.status_code, "Повтори позже."))
    try:
        answer = response.json()
    except ValueError:
        raise ValueError("Telegram вернул ответ не в формате JSON.") from None
    if not answer.get("ok"):
        raise ValueError("Telegram не выполнил запрос.")
    return answer["result"]


def send(chat_id, text):
    telegram("sendMessage", {"chat_id": chat_id, "text": text,
             "reply_markup": {"keyboard": [["Создать парсер"]], "resize_keyboard": True}})


def handle_message(message):
    if message["chat"]["type"] != "private":
        return
    text = message.get("text", "").strip()
    if not text:
        return
    chat_id = message["chat"]["id"]
    if text in ("/new", "Создать парсер"):
        send(chat_id, "Создание маршрута появится на следующем этапе.")
    else:
        send(chat_id, "Привет! Это учебный бот поиска авиабилетов. Нажми «Создать парсер».")



def main():
    global config
    config = dotenv_values(FOLDER / ".env", encoding="utf-8-sig", interpolate=False)
    if not config.get("TELEGRAM_BOT_TOKEN"):
        print("Заполни TELEGRAM_BOT_TOKEN в .env.")
        return
    offset = 0
    print("Бот запущен. Остановка: Ctrl+C.")
    while True:
        try:
            updates = telegram("getUpdates", {"offset": offset, "timeout": 10, "allowed_updates": ["message"]})
            for update in updates:
                offset = update["update_id"] + 1
                if "message" in update:
                    handle_message(update["message"])
        except (requests.RequestException, ValueError) as error:
            print("Ошибка запроса:", type(error).__name__)
            time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Бот остановлен.")
