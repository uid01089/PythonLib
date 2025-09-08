import asyncio
from typing import Callable
from datetime import datetime, timedelta, time


class AsyncScheduler:

    def __init__(self) -> None:
        self.background_tasks = set()

    async def oneShoot(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        """Adds a new non-reloading task to the task list."""

        async def fct():
            await asyncio.sleep(timePeriodMs / 1000)
            await callback()

        task = asyncio.create_task(fct())
        self.background_tasks.add(task)
        task.add_done_callback(self.background_tasks.remove)

    async def scheduleEach(self, callback: Callable[[None], None], timePeriodMs: int) -> None:
        """Adds a new reloading task to the task list."""
        async def fct():
            while True:
                await asyncio.sleep(timePeriodMs / 1000)
                await callback()

        task = asyncio.create_task(fct())
        self.background_tasks.add(task)
        task.add_done_callback(self.background_tasks.remove)

    async def scheduleAtTime(self, callback: Callable[[None], None], startTime: time, reloading: timedelta = None) -> None:
        """Adds a new time-based task to the task list."""

    async def scheduleAtDate(self, callback: Callable[[None], None], startDate: datetime, reloading: timedelta = None) -> None:
        """Adds a new date-based task to the task list."""
