from abc import ABC, abstractmethod
from exmo.api.public import PublicExmoApi
from exmo.tasks.task_collections import TaskCollection
from .tasks.task_factory import TaskFactory
import asyncio
from .tasks.actions import Action
from .tasks.conditions import Condition

public_api = PublicExmoApi()


class AbstractBigLoop(ABC):

    def __init__(self):
        self.task_factory = TaskFactory()
        self._tasks_collection = self.task_factory.get_task_collection()

    def create_task(self, task_id: int, action: Action, condition: Condition):
        self.task_factory.create_task(task_id, action, condition)

    @abstractmethod
    async def loop(self):
        """Big loop."""
        pass

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        loop.create_task(self.loop())


class ApiBigLoop(AbstractBigLoop):

    @abstractmethod
    async def get_api_response(self) -> dict:
        """Get response from exmo api."""
        pass

    async def loop(self):
        while True:
            api_response = await self.get_api_response()
            should_delete = set()
            for task_id, task in self._tasks_collection:
                if task.check_condition(api_response):
                    await task.do_action(api_response)
                    should_delete.add(task_id)
            for task_id in should_delete:
                self.task_factory.delete_task(task_id)

            await asyncio.sleep(10)


class OrderApiBigLoop(ApiBigLoop):

    async def get_api_response(self) -> dict:
        return await public_api.order_book(['BTC_USD'])


class TradesBigLoop(ApiBigLoop):

    async def get_api_response(self) -> dict:
        return await public_api.trades(['BTC_USD'])
