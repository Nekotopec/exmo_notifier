from exmo.tasks.actions import Action


class NotifyAction(Action):

    def __init__(self, notificator):
        self.notificator = notificator

    async def do(self, context):
        bid_top = context.get('BTC_USD').get('bid_top')
        ask_top = context.get('BTC_USD').get('ask_top')
        message = ('ALARM!\n'
                   f'bid_top:\t {bid_top}\n'
                   f'ask_top:\t {ask_top}')
        return await self.notificator.notify(message)
