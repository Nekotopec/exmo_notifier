import asyncio
import logging
import ssl

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.webhook import SendMessage, get_new_configured_app
from aiohttp import web
import exmo
import settings
from telebot.telebot import WebhookBot

# Creating bot.
bot = WebhookBot(settings.TELEGRAM_TOKEN)
bot.prepare_bot(webhook_url=settings.WEBHOOK_URL,
                webhook_path=settings.WEBHOOK_PATH,
                webhook_ssl_cert=settings.WEBHOOK_SSL_CERT,
                webhook_ssl_priv=settings.WEBHOOK_SSL_PRIV)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['threshold'])
async def set_threshold(message: types.Message):
    threshold = message.text.split(' ')[1]
    try:
        await exmo.start_comparing(threshold)
        text = F'Threshold = {threshold} was set.'
    except Exception as e:
        text = f'Exception was occurred \n{e}'
    return await bot.send_message(message.chat.id, text)


@dp.message_handler(chat_id=243279187)
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def send_notification(bid_top: int, ask_top: int, chat_id: int):
    """Send notification about bid and ask top information."""
    message = ('ALARM!\n'
               f'bid_top:\t {bid_top}\n'
               f'ask_top:\t {ask_top}')
    await bot.send_message(chat_id, message)


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.WEBHOOK_SSL_CERT,
                            settings.WEBHOOK_SSL_PRIV)
    app = bot.init_app(dp)

    # Start web-application.
    web.run_app(app, host=settings.WEBAPP_HOST, port=settings.WEBHOOK_PORT,
                ssl_context=context)
