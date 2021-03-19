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

bot = Bot(settings.TELEGRAM_TOKEN)
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


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(app):
    print(settings.WEBHOOK_URL)

    # Get current webhook status
    webhook = await bot.get_webhook_info()

    if webhook.url != settings.WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()

        # Set new URL for webhook
        await bot.set_webhook(settings.WEBHOOK_URL,
                              certificate=open(settings.WEBHOOK_SSL_CERT, 'rb'))

    # insert code here to run it after start


async def on_shutdown(app):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


async def send_notification(bid_top: int, ask_top: int, chat_id: int):
    """Send notification about bid and ask top information."""
    message = ('ALARM!\n'
               f'bid_top:\t {bid_top}\n'
               f'ask_top:\t {ask_top}')
    await bot.send_message(chat_id, message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = get_new_configured_app(dispatcher=dp, path=settings.WEBHOOK_PATH)
    # Setup event handlers.
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Generate SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.WEBHOOK_SSL_CERT,
                            settings.WEBHOOK_SSL_PRIV)

    # Start web-application.
    web.run_app(app, host=settings.WEBAPP_HOST, port=settings.WEBHOOK_PORT,
                ssl_context=context)
