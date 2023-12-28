from PythonLib.Scheduler import Scheduler


class Throttle:
    def __init__(self, deadTimeMs: int) -> None:
        self.deadTimeMs = deadTimeMs
        self.lastRequestTime = None

    def triggerAndCheck(self) -> bool:
        if self.lastRequestTime is None:
            self.lastRequestTime = Scheduler.getMillis()
            return True
        else:
            if Scheduler.getMillis() - self.lastRequestTime > self.deadTimeMs:
                self.lastRequestTime = Scheduler.getMillis()
                return True

        return False
