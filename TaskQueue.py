from queue import Queue
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable

from PythonLib.Scheduler import Scheduler


class State(Enum):
    Init = 1
    Started = 2
    Finished = 3


class TaskQueueTask(ABC):

    def __init__(self) -> None:
        self.status = State.Init

    @abstractmethod
    def loop(self) -> None:
        raise NotImplementedError

    def getStatus(self) -> State:
        return self.status


class TaskQueue:
    def __init__(self) -> None:
        self.jobList = Queue()
        self.currentJob: TaskQueueTask = None

    def add(self, task: TaskQueueTask) -> None:
        self.jobList.put(task)

    def cancel(self) -> None:
        self.currentJob = None

    def loop(self) -> None:

        if not self.currentJob:
            if not self.jobList.empty():
                self.currentJob = self.jobList.get()

        if self.currentJob:
            self.currentJob.loop()
            if self.currentJob.getStatus() == State.Finished:
                self.currentJob = None


class TaskQueueExecuteOperation(TaskQueueTask):
    def __init__(self, fct: Callable[[str], None]) -> None:
        super().__init__()
        self.fct = fct

    def loop(self) -> None:
        self.fct()
        self.status = State.Finished


class TaskQueueWait(TaskQueueTask):
    def __init__(self, timeMs: int) -> None:
        super().__init__()
        self.timeMs = timeMs
        self.startTime: int = None

    def loop(self) -> None:
        if self.status == State.Init:
            self.startTime = Scheduler.getMillis()
            self.status = State.Started

        if Scheduler.getMillis() - self.startTime > self.timeMs:
            self.status = State.Finished
