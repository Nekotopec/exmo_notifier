from .tasks import Task
from abc import ABC, abstractmethod


class TaskCollection(ABC):

    @abstractmethod
    def __iter__(self):
        return self

    @abstractmethod
    def pop(self, key):
        """Pop key from collection."""
        pass

    @abstractmethod
    def add(self, key: int, value: Task):
        """Add task to collection."""
        pass


class DictTaskCollection(TaskCollection):
    """Collection with dict core."""

    def __init__(self):
        self._collection = dict()

    def __iter__(self):
        yield from self._collection.items()

    def pop(self, key):
        """Pop key from dict collection."""
        return self._collection.pop(key, None)

    def add(self, key: int, value: Task):
        """Add key and value to dict collection."""
        self._collection[key] = value
