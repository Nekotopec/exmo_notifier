import asyncio
import logging
import ssl

from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.webhook import SendMessage, get_new_configured_app
from aiohttp import web
import exmo
import settings
from telebot.telebot import WebhookBot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from exmo.application import ExmoApplication
from notificators import TelegramNotificator
from actions import NotifyAction
from conditions import LessTopBidCondition

# Exmo application.
exmo_app = ExmoApplication()

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
    task_id = message.chat.id
    try:
        notificator = TelegramNotificator(bot, task_id)
        action = NotifyAction(notificator)
        condition = LessTopBidCondition(threshold)
        exmo_app.order_big_loop.create_task(task_id=task_id,
                                            action=action,
                                            condition=condition)
        text = F'Threshold = {threshold} was set.'
    except Exception as e:
        text = f'Exception was occurred \n{e}'
    return await bot.send_message(message.chat.id, text)


@dp.message_handler(chat_id=243279187)
async def echo(message: types.Message):
    mes = await send_notification(12, 12, chat_id=243279187)
    await asyncio.sleep(5)
    await mes.delete()
    await message.delete()

    keyboard_markup = build_inline_keyboard()

    # return SendMessage(message.chat.id,
    #                    message.text,
    #                    reply_markup=keyboard_markup)


async def send_notification(bid_top: int, ask_top: int, chat_id: int):
    """Send notification about bid and ask top information."""
    message = ('ALARM!\n'
               f'bid_top:\t {bid_top}\n'
               f'ask_top:\t {ask_top}')
    return await bot.send_message(chat_id, message)


def build_inline_keyboard():
    button = KeyboardButton('/check')
    reply_keyboard_markup = ReplyKeyboardMarkup([[button]])
    return reply_keyboard_markup


def get_current_bot():
    """Return running bot."""
    return bot


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.WEBHOOK_SSL_CERT,
                            settings.WEBHOOK_SSL_PRIV)
    app = bot.init_app(dp)
    loop = asyncio.get_event_loop()
    exmo_app.set_loop(loop)

    # Start web-application.
    executor.start_webhook(dispatcher=dp,
                           webhook_path=bot._webhook_path,
                           loop=loop,
                           on_startup=bot.on_startup,
                           port=settings.WEBHOOK_PORT,
                           on_shutdown=bot.on_shutdown,
                           ssl_context=context)
    # web.run_app(app, host=settings.WEBAPP_HOST, port=settings.WEBHOOK_PORT,
    #             ssl_context=context)
