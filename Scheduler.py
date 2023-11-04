
from typing import Callable
import time
import logging

logger = logging.getLogger('Scheduler')


class Task:
    """
    A class used to represent a Task.

    ...

    Attributes
    ----------
    startTimeMs : int
        a timestamp indicating when the task should start
    durationMs : int
        the duration of the task in milliseconds
    callback : Callable[[None], None]
        the function that is called when the task is executed
    reloading : bool
        a flag indicating whether the task should be reloaded after execution

    Methods
    -------
    getStartTime():
        Returns the start time of the task
    setStartTime(startTimeMs: int):
        Sets the start time of the task
    getDuration():
        Returns the duration of the task
    getFct():
        Returns the callback function of the task
    isReloading():
        Returns the reloading status of the task
    """

    def __init__(self, startTimeMs: int, durationMs: int, callback: Callable[[None], None], reloading: bool) -> None:
        self.startTimeMs = startTimeMs
        self.durationMs = durationMs
        self.callback = callback
        self.reloading = reloading

    def getStartTime(self) -> int:
        """Returns the start time of the task"""
        return self.startTimeMs

    def setStartTime(self, startTimeMs: int) -> None:
        """Sets the start time of the task"""
        self.startTimeMs = startTimeMs

    def getDuration(self) -> int:
        """Returns the duration of the task"""
        return self.durationMs

    def getFct(self) -> Callable[[None], None]:
        """Returns the callback function of the task"""
        return self.callback

    def isReloading(self) -> bool:
        """Returns the reloading status of the task"""
        return self.reloading


class Scheduler:
    """
    A class used to represent a Scheduler.

    ...

    Attributes
    ----------
    taskList : list
        a list of tasks to be executed

    Methods
    -------
    loop():
        Executes tasks from the task list based on their start time and duration
    oneShoot(callback: Callable[[None], None], timePeriodMs: int):
        Adds a new non-reloading task to the task list
    scheduleEach(callback: Callable[[None], None], timePeriodMs: int):
        Adds a new reloading task to the task list
    __millis():
        Returns the current time in milliseconds
    getTaskSize():
        Returns the number of tasks in the task list
    """

    def __init__(self) -> None:
        self.taskList = []

    def loop(self) -> None:
        """Executes tasks from the task list based on their start time and duration"""

        taskForDelete = []

        for task in self.taskList:
            # https://arduino.stackexchange.com/questions/12587/how-can-i-handle-the-millis-rollover/12588#12588
            if self.__millis() - task.getStartTime() > task.getDuration():
                try:
                    # Call the function
                    task.getFct()()
                except BaseException:
                    logging.exception('')

                if task.isReloading():
                    task.setStartTime(self.__millis())
                else:
                    # mark current task to delete
                    taskForDelete.append(task)

        for task in taskForDelete:
            self.taskList.remove(task)

        logger.debug("JobList size: %i", len(self.taskList))

    def oneShoot(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        """Adds a new non-reloading task to the task list"""
        self.taskList.append(Task(self.__millis(), timePeriodMs, callback, False))

    def scheduleEach(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        """Adds a new reloading task to the task list"""
        self.taskList.append(Task(self.__millis(), timePeriodMs, callback, True))

    def __millis(self) -> int:
        """Returns the current time in milliseconds"""
        return int(time.time() * 1000)

    def getTaskSize(self) -> int:
        """Returns the number of tasks in the task list"""
        return len(self.taskList)
