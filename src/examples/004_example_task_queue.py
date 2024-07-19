#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
The BaseApp multiprocess application example.

TaskQueue usage.

Exit using Ctrl-C.
"""

from __future__ import print_function

__author__ = "Evgeny Kazanov"

import os
import sys
import time

from multipro_lab.main import Main
from multipro_lab.worker import Worker
from multipro_lab.timer import Timer


class UserWorker(Worker):

    def __init__(self, *args, **kwargs):
        super(UserWorker, self).__init__(*args, **kwargs)
        self.main_loop_sleep_time = 0.1

    def worker_action(self):
        task = self.msg_router.task_queue.get_task()
        if task is None:
            return None
        result = self.do_task(task[0], task[1])
        print(
            "Worker_name={}, a = {}, b = {}, result = {}".format(
                self.name, task[0], task[1], result
            )
        )
        return True

    def do_task(self, a, b):
        result = a * b
        return result


class UserMain(Main):

    def __init__(self, *args, **kwargs):
        self.timer_1 = Timer(interval=1)
        self.timer_2_5 = Timer(interval=2.5)
        super(UserMain, self).__init__(*args, **kwargs)

    def main_action(self):
        if self.timer_1.check_timer():
            print("----- Timer 1 -----")
            self.msg_router.task_queue.send_task([1, 4])
            self.msg_router.task_queue.send_task([2, 6])
            self.msg_router.task_queue.send_task([3, 8])
            self.msg_router.task_queue.send_task([4, 9])
            self.msg_router.task_queue.send_task([5, 11])
            self.msg_router.task_queue.send_task([6, 13])
        if self.timer_2_5.check_timer():
            print("----- Timer2.5 -----")
            self.msg_router.task_queue.send_task([21, 9])
            self.msg_router.task_queue.send_task([23, 11])
            self.msg_router.task_queue.send_task([25, 13])
        return


print(__doc__)
time.sleep(1)

main = UserMain(task_queue=True)
main.main_loop_sleep_time = 0.1
worker = UserWorker(name="Worker_01")
main.register_worker(worker=worker)
worker = UserWorker(name="Worker_02")
main.register_worker(worker=worker)
worker = UserWorker(name="Worker_03")
main.register_worker(worker=worker)


main.run()

sys.exit(0)
