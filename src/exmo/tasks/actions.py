from abc import ABC, abstractmethod


class Action(ABC):

    @abstractmethod
    def do(self, context):
        pass
