import time

from TaskQueue import TaskQueueExecuteOperation, TaskQueue, TaskQueueWait


def main() -> None:

    taskQueue = TaskQueue()
    taskQueue.add(TaskQueueExecuteOperation(lambda: print("Hallo 1")))
    taskQueue.add(TaskQueueWait(5000))
    taskQueue.add(TaskQueueExecuteOperation(lambda: print("Hallo 2")))
    taskQueue.add(TaskQueueWait(1000))
    taskQueue.add(TaskQueueExecuteOperation(lambda: print("Hallo 3")))
    taskQueue.add(TaskQueueWait(500))
    taskQueue.add(TaskQueueExecuteOperation(lambda: print("Hallo 4")))

    while (True):

        time.sleep(0.25)
        taskQueue.loop()


if __name__ == '__main__':
    main()
