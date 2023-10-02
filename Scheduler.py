from typing import Callable
import time
import logging

logger = logging.getLogger('Scheduler')


class Task:
    def __init__(self, startTimeMs: int, durationMs: int, callback: Callable[[None], None], reloading: bool) -> None:
        self.startTimeMs = startTimeMs
        self.durationMs = durationMs
        self.callback = callback
        self.reloading = reloading

    def getStartTime(self) -> int:
        return self.startTimeMs

    def setStartTime(self, startTimeMs: int) -> None:
        self.startTimeMs = startTimeMs

    def getDuration(self) -> int:
        return self.durationMs

    def getFct(self) -> Callable[[None], None]:
        return self.callback

    def isReloading(self) -> bool:
        return self.reloading


class Scheduler:
    def __init__(self) -> None:
        self.taskList = []

    def loop(self) -> None:

        taskForDelete = []

        for task in self.taskList:
            # https://arduino.stackexchange.com/questions/12587/how-can-i-handle-the-millis-rollover/12588#12588
            if self.__millis() - task.getStartTime() > task.getDuration():
                # Call the function
                task.getFct()()

                if task.isReloading():
                    task.setStartTime(self.__millis())
                else:
                    # mark current task to delete
                    taskForDelete.append(task)

        for task in taskForDelete:
            self.taskList.remove(task)

        logger.debug("JobList size: %i", len(self.taskList))

    def oneShoot(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        self.taskList.append(Task(self.__millis(), timePeriodMs, callback, False))

    def scheduleEach(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        self.taskList.append(Task(self.__millis(), timePeriodMs, callback, True))

    def __millis(self) -> int:
        return int(time.time() * 1000)
