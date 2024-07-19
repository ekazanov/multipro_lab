#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: mutipro_lab. Class: BaseAppMain.

"""


__author__ = "Evgeny Kazanov"

import time

from multipro_lab.message_receiver import MessageReceiver
from multipro_lab.message_router import MessageRouter
from multipro_lab.signal_utils import ExitSignalReceiver
from multipro_lab.task_queue import TaskQueue


class Main(object):

    def __init__(self, check_workers=False, task_queue=False):
        self.main_loop_sleep_time = 0.01
        self.worker_arr = []
        self.worker_to_check_arr = []
        self.check_workers = check_workers
        self.msg_receiver = MessageReceiver()
        self.msg_router = MessageRouter()
        self.exit_signal_receiver = ExitSignalReceiver()
        self._exit_flag = False
        self.name = "main"
        self.msg_router.register_receiving_object(receiving_object=self)
        if task_queue:
            self.task_queue = TaskQueue()
            self.msg_router.register_task_queue(task_queue=self.task_queue)
        else:
            self.task_queue = None

    def register_worker(self, worker=None):
        self.worker_arr.append(worker)
        worker.set_main_input_q(main_input_q=self.msg_receiver.in_q)
        worker.set_msg_router(self.msg_router)
        # worker.set_task_queue(task_queue=self.task_queue)
        self.msg_router.register_receiving_object(receiving_object=worker)
        if self.check_workers:
            self.worker_to_check_arr.append(worker)
        return

    def run(self):
        self._run_workers()
        self._main_loop()
        return

    def _run_workers(self):
        for worker in self.worker_arr:
            worker.run_worker()
        return

    def main_action(self):
        msg = "Unimplemented method: {}".format(
            str(self.__class__) + "." + str(__name__)
        )
        raise Exception(msg)

    def _main_loop(self):
        while True:
            self.main_action()
            self.msg_receiver.get_messages()
            # Exit by signal
            if self.exit_signal_receiver.exit_flag:
                break
            # Exit by exit() call
            if self._exit_flag:
                break
            time.sleep(self.main_loop_sleep_time)
        self._exit_workers()
        for worker in self.worker_arr:
            worker.proc.join()
        return

    def _exit_workers(self):
        # send exit message to workers
        for worker in self.worker_arr:
            self.send_exit_msg(worker)
        return

    def send_exit_msg(self, worker):
        self.msg_router.send_message(
            receiving_object_name=worker.name, message_type="exit", message_body=None
        )
        return

    def exit(self):
        """Exit the application."""
        self._exit_flag = True
        return


if __name__ == "__main__":
    main = Main()
    main.run()
