"""
Project: mutipro_lab. Class: TaskQueue.

DONE: Add a Queue attribute.
DONE: Add a TaskQueue.get_task() method.
DONE: Add a Main.task_queue attribute.
DONE: Add a task_queue argument to Main.__init_().
 - task_queue=False.
DONE: Add a Worker.task_queue attribute.
DONE: Add Worker.task_queue setting in Main.register_worker.
 - if task_queue==True set Main.task_queue = TaskQueue().
 - set Worker.task_queue attribute.
TODO: Develop sending a task using MessageRouter
TODO: Add TaskQueue section to README
TODO: Add an example for the TaskQueue.
TODO: Task should be sent to TaskQueue using MessageRouter.
"""

from multiprocessing import Queue

from queue import Empty


class TaskQueue(object):
    """ """

    def __init__(
        self,
    ):
        """ """
        self.task_queue = Queue()

    def get_task(self):
        """Get task from the self.task_queue queue."""
        try:
            task = self.task_queue.get(block=False)
        except Empty:
            return None
        return task

    def send_task(self, task):
        self.task_queue.put(task)
        return
