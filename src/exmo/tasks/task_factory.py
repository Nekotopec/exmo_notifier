from .task_collections import TaskCollection, DictTaskCollection
from .tasks import Task
from settings import DEFAULT_TASK_COLLECTION
from .conditions import Condition
from .actions import Action


class TaskFactoryException(Exception):
    pass


class TaskExistentError(TaskFactoryException):
    """Task with task_id doesn't exist."""
    pass


class TaskFactory:

    def __init__(self, task_collection: TaskCollection = None):
        """
        Create new task factory and initialize new task collection or use
        existing one.

        Args:
            task_collection (TaskCollection): task collection.
                Default DictTaskCollection
        """

        if not task_collection:
            task_collection = DEFAULT_TASK_COLLECTION()
        self._task_collection = task_collection

    def get_task_collection(self):
        return self._task_collection

    def create_task(self, task_id: int, action: Action, condition: Condition):
        task = Task()
        task.set_action(action)
        task.set_condition(condition)
        self._task_collection.add(key=task_id, value=task)
        return task

    def delete_task(self, task_id):
        """Delete task from task collection."""
        task = self._task_collection.pop(task_id)
        if task is None:
            raise TaskExistentError(f'Task wit task_id={task_id} '
                                    f'doesn\'t exist.')
        return task
