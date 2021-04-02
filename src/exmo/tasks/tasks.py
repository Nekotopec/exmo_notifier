from typing import Optional, Coroutine, Callable, Awaitable
from .actions import Action
from .conditions import Condition


class Task:
    """Task class."""

    _action: Action = None
    _condition: Condition = True

    def set_action(self, action: Action):
        self._action = action

    def set_condition(self, condition: Condition):
        self._condition = condition

    def check_condition(self, response):
        return self._condition.check(response)

    # action must be coroutine
    async def do_action(self, response):
        return await self._action.do(response)


