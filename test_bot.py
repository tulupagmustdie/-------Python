import unittest
from datetime import date, timedelta
from unittest.mock import patch, Mock
import bot


class BotTests(unittest.TestCase):
    def setUp(self):
        bot.dialogs = {}
        bot.cities = [{"name": "Москва", "code": "MOW"}, {"name": "Санкт-Петербург", "code": "LED"}]
        self.sender = patch.object(bot, "send").start()
        self.addCleanup(patch.stopall)

    def message(self, text):
        bot.handle_message({"chat": {"id": 1, "type": "private"}, "text": text})

    def test_start_and_group(self):
        self.message("/start")
        self.sender.assert_called_once()
        bot.handle_message({"chat": {"id": 2, "type": "group"}, "text": "/start"})
        self.sender.assert_called_once()


if __name__ == "__main__":
    unittest.main()
