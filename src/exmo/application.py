from .tasks.task_factory import TaskFactory
from .loops import OrderApiBigLoop, TradesBigLoop
import asyncio


class ExmoApplication:

    def __init__(self):
        self.order_big_loop = OrderApiBigLoop()
        self.trades_big_loop = TradesBigLoop()
        self.loops = [self.order_big_loop, self.trades_big_loop]

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        """Set event loop for current application."""

        for big_loop in self.loops:
            big_loop.set_loop(loop)
