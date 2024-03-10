from queue import Queue
from abc import ABC, abstractmethod


class TaskQueueTask(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass


class TaskQueue:
    def __init__(self) -> None:
        self.queue = Queue()

    def add(self, task: TaskQueueTask) -> None:
        self.queue.put(task)

        while not self.queue.empty():
            item = self.queue.get()
            item.execute()
