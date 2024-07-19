"""
Project: mutipro_lab. Class: Worker.
"""

__author__ = "Evgeny Kazanov"

from multiprocessing import Process
import os
import time

from multipro_lab.signal_utils import ignore_sigint
from multipro_lab.message_receiver import MessageReceiver


class Worker(object):

    def __init__(self, name=None, block=False):
        if block:
            self.main_loop_sleep_time = None
        else:
            self.main_loop_sleep_time = 0.01
        self.proc = None
        self.name = name
        self.main_input_q = None
        self.msg_receiver = MessageReceiver(block=block)
        self.msg_router = None
        """The MessageRouter object is added during the Worker registration in
        Main class object.
        """
        self._exit_flag = False
        self.msg_receiver.register_handler(
            message_type="exit", message_handler=self._exit
        )

    def set_main_input_q(self, main_input_q=None):
        self.main_input_q = main_input_q
        return

    def set_msg_router(self, msg_router=None):
        self.msg_router = msg_router
        return

    def run_worker(self):
        if self.msg_router.task_queue:
            args = (
                self.main_input_q,
                self.msg_receiver.in_q,
                self.msg_router.task_queue,
            )
        else:
            args = (self.main_input_q, self.msg_receiver.in_q, None)
        self.proc = Process(target=self._main_loop, args=args)
        self.proc.start()
        return self.proc

    def worker_action(self):
        msg = "Unimplemented method: {}".format(self.__class__ + "." + __name__)
        raise Exception(msg)

    def _main_loop(self, main_input_q, msg_receiver_in_q, task_queue):
        ignore_sigint()
        # Redefine queues after a fork
        self.main_input_q = main_input_q
        self.msg_receiver.in_q = msg_receiver_in_q
        if self.msg_router.task_queue:
            self.msg_router.task_queue = task_queue
        while not self._exit_flag:
            self.worker_action()
            self.msg_receiver.get_messages()
            if not self.main_loop_sleep_time is None:
                time.sleep(self.main_loop_sleep_time)
        return

    def _exit(self, msg_data):
        self._exit_flag = True
        return
