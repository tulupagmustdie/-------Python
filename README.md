# Поиск авиабилетов 

Заложена основа Telegram-бота: переменные окружения, запросы к Telegram API,
команды `/start` и `/help`, получение сообщений через `getUpdates`.
Поиск маршрутов и цен пока не реализован.

## Запуск

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

