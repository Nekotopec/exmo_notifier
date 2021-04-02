from abc import ABC, abstractmethod
from aiogram import Bot


class Notificator(ABC):

    @abstractmethod
    async def notify(self, message):
        pass


class TelegramNotificator(Notificator):
    def __init__(self, bot: Bot, chat_id: int):
        self.chat_id = chat_id
        self.bot = bot

    async def notify(self, message):
        return await self.bot.send_message(self.chat_id, message)
