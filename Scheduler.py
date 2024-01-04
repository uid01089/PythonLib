from typing import Callable, List
from datetime import datetime, timedelta, time
import logging
import time as oldTime

logger = logging.getLogger('PythonLib.Scheduler')


class Task:
    def __init__(self, callback: Callable[[None], None]) -> None:
        self.callback = callback

    def getFct(self) -> Callable[[None], None]:
        """Returns the callback function of the task"""
        return self.callback


class AbsDateTask(Task):
    def __init__(self, startDate: datetime, callback: Callable[[None], None], reloading: timedelta = None) -> None:
        super().__init__(callback)
        self.startDate = startDate
        self.reloading = reloading

    def getStartDate(self) -> datetime:
        return self.startDate

    def setStartDate(self, startDate: datetime) -> None:
        self.startDate = startDate

    def getReloading(self) -> timedelta:
        return self.reloading


class AbsTimeTask(Task):
    def __init__(self, startTime: time, callback: Callable[[None], None], reloading: timedelta = None) -> None:
        super().__init__(callback)
        self.startTime = startTime
        self.reloading = reloading

    def getStartTime(self) -> time:
        return self.startTime

    def setStartTime(self, startTime: time) -> None:
        self.startTime = startTime

    def getReloading(self) -> timedelta:
        return self.reloading


class RelMsTask(Task):
    """A class used to represent a Task."""

    def __init__(self, startTimeMs: int, durationMs: int, callback: Callable[[None], None], reloading: bool) -> None:
        super().__init__(callback)
        self.startTimeMs = startTimeMs
        self.durationMs = durationMs
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

    def isReloading(self) -> bool:
        """Returns the reloading status of the task"""
        return self.reloading


class Scheduler:
    """A class used to represent a Scheduler."""

    def __init__(self) -> None:
        self.relMsTaskList: List[RelMsTask] = []
        self.absDateTaskList: List[AbsDateTask] = []
        self.absTimeTaskList: List[AbsTimeTask] = []

    def __loopRelMsTaskList(self) -> None:
        """Executes tasks from the relMsTaskList based on their start time and duration."""
        deleteRelMsTaskList: List[RelMsTask] = []

        for task in self.relMsTaskList:
            # https://arduino.stackexchange.com/questions/12587/how-can-i-handle-the-millis-rollover/12588#12588
            if Scheduler.getMillis() - task.getStartTime() > task.getDuration():
                try:
                    # Call the function
                    task.getFct()()
                except BaseException:
                    logging.exception('')

                if task.isReloading():
                    task.setStartTime(Scheduler.getMillis())
                else:
                    # mark current task to delete
                    deleteRelMsTaskList.append(task)

        for task in deleteRelMsTaskList:
            self.relMsTaskList.remove(task)

        logger.debug("JobList size: %i", len(self.relMsTaskList))

    def __loopAbsDateTaskList(self) -> None:
        """Executes tasks from the absDateTaskList based on their start date."""
        deleteAbsDateTaskList: List[AbsDateTask] = []

        for task in self.absDateTaskList:
            if datetime.now() > task.getStartDate():
                try:
                    # Call the function
                    task.getFct()()
                except BaseException:
                    logging.exception('')

                if task.getReloading():
                    task.setStartDate(task.getStartDate() + task.getReloading())
                else:
                    # mark current task to delete
                    deleteAbsDateTaskList.append(task)

        for task in deleteAbsDateTaskList:
            self.absDateTaskList.remove(task)

        logger.debug("JobList size: %i", len(self.absDateTaskList))

    def __loopAbsTimeTaskList(self) -> None:
        """Executes tasks from the absTimeTaskList based on their start time."""
        deleteAbsTimeTaskList: List[AbsTimeTask] = []

        for task in self.absTimeTaskList:
            if datetime.now().time() > task.getStartTime():
                try:
                    # Call the function
                    task.getFct()()
                except BaseException:
                    logging.exception('')

                if task.getReloading():
                    task.setStartTime((datetime.combine(datetime.today(), task.getStartTime()) + task.getReloading()).time())
                else:
                    # mark current task to delete
                    deleteAbsTimeTaskList.append(task)

        for task in deleteAbsTimeTaskList:
            self.absDateTaskList.remove(task)

        logger.debug("JobList size: %i", len(self.absDateTaskList))

    def loop(self) -> None:
        """Executes tasks from all task lists."""
        self.__loopAbsDateTaskList()
        self.__loopAbsTimeTaskList()
        self.__loopRelMsTaskList()

    def oneShoot(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        """Adds a new non-reloading task to the task list."""
        self.relMsTaskList.append(RelMsTask(Scheduler.getMillis(), timePeriodMs, callback, False))

    def scheduleEach(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        """Adds a new reloading task to the task list."""
        self.relMsTaskList.append(RelMsTask(Scheduler.getMillis(), timePeriodMs, callback, True))

    def scheduleAtTime(self, callback: Callable[[None], None], startTime: time, reloading: timedelta = None) -> None:
        """Adds a new time-based task to the task list."""
        self.absTimeTaskList.append(AbsTimeTask(startTime, callback, reloading))

    def scheduleAtDate(self, callback: Callable[[None], None], startDate: datetime, reloading: timedelta = None) -> None:
        """Adds a new date-based task to the task list."""
        self.absDateTaskList.append(AbsDateTask(startDate, callback, reloading))

    @staticmethod
    def getMillis() -> int:
        """Returns the current time in milliseconds."""
        return int(oldTime.time() * 1000)

    @staticmethod
    def getSeconds() -> int:
        """Returns the current time in seconds."""
        return int(oldTime.time())

    def getTaskSize(self) -> int:
        """Returns the number of tasks in the task list."""
        return len(self.relMsTaskList) + len(self.absDateTaskList) + len(self.absTimeTaskList)
