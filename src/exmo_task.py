from aiohttp import ClientSession
import json
import asyncio
import telegram_bot
import aiogram
from typing import NamedTuple


class OrderData(NamedTuple):
    """Order data from exmo."""
    top_ask: float
    top_bid: float
    ask: list
    bid: list


async def notify(chat_id: int, bot: aiogram.Bot, data: OrderData):
    await bot.send_message(chat_id, '')


async def start_comparing(threshold):
    loop = asyncio.get_running_loop()
    if tasks:
        task = tasks.pop()
        task.cancel()
    task = loop.create_task(compare_bit_with_threshold(float(threshold)))
    tasks.append(task)


async def get_bid(client: ClientSession):
    url = "https://api.exmo.com/v1.1/order_book"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = 'pair=BTC_USD&limit=100'
    try:
        response = await client.post(url, headers=headers, data=payload)
    except Exception:
        return None

    if response.status == 200:
        received_data = await response.json()
        return received_data
    else:
        return None


async def compare_bit_with_threshold(threshold: float):
    while True:
        async with ClientSession() as client:
            received_data = await get_bid(client)
        print(received_data)
        bid_top = received_data.get('BTC_USD').get('bid_top')
        if bid_top and float(bid_top) < threshold:
            ask_top = received_data.get('BTC_USD').get('ask_top')
            await telegram_bot.send_notification(ask_top=ask_top,
                                                 bid_top=bid_top,
                                                 chat_id=243279187)
            break
        await asyncio.sleep(60)
