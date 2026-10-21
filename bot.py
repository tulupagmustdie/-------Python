import time
from pathlib import Path



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