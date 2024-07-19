#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
The BaseApp multiprocess application example.
Run main class and two workers.

Run main process and two worker processes.

main process sends messages to workers. Worker01 sends messages to main.

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


class UserWorker01(Worker):

    def __init__(self, *args, **kwargs):
        super(UserWorker01, self).__init__(*args, **kwargs)
        # self.main_loop_sleep_time = .1
        self.msg_receiver.register_handler(
            message_type="print", message_handler=self._msg_handl_print_msg
        )

    def worker_action(self):
        return

    def _msg_handl_print_msg(self, msg_body=None):
        print(
            "PID: {}; Worker: {}; Message: {}".format(os.getpid(), self.name, msg_body)
        )
        return


class UserWorker02(Worker):

    def __init__(self, *args, **kwargs):
        super(UserWorker02, self).__init__(*args, **kwargs)
        self.main_loop_sleep_time = 0.1
        self.timer_1 = Timer(interval=1)
        self.msg_receiver.register_handler(
            message_type="print", message_handler=self._msg_handl_print_msg
        )

    def worker_action(self):
        if self.timer_1.check_timer():
            self._send_message_to_main()
        return

    def _msg_handl_print_msg(self, msg_body=None):
        print(
            "PID: {}; Worker: {}; Message: {}".format(os.getpid(), self.name, msg_body)
        )
        return

    def _send_message_to_main(self):
        self.msg_router.send_message(
            receiving_object_name="main",
            message_type="print",
            message_body="Message from Worker_01 to main",
        )
        return


class UserMain(Main):

    def __init__(self, *args, **kwargs):
        self.timer_1 = Timer(interval=1)
        self.sec_cnt = 0
        self.timer_2 = Timer(interval=2)
        self.timer_3_5 = Timer(interval=3.5)
        super(UserMain, self).__init__(*args, **kwargs)
        self.msg_receiver.register_handler(
            message_type="print", message_handler=self._msg_handl_print_msg
        )

    def main_action(self):
        if self.timer_1.check_timer():
            self.sec_cnt += 1
            print("{}".format(self.sec_cnt))
        if self.timer_2.check_timer():
            self._send_msg_to_worker_01()
        if self.timer_3_5.check_timer():
            self._send_msg_to_worker_02()
        return

    def _send_msg_to_worker_01(self):
        print("Main: Send message from Main to Worker_01")
        self.msg_router.send_message(
            receiving_object_name="Worker_01_blocking_msg_reading",
            message_type="print",
            message_body="Message from Main to Worker_01",
        )
        return

    def _send_msg_to_worker_02(self):
        print("Main: Send message from Main to Worker_02")
        self.msg_router.send_message(
            receiving_object_name="Worker_02",
            message_type="print",
            message_body="Message from Main to Worker_02",
        )
        return

    def _msg_handl_print_msg(self, msg_body=None):
        print("Main. Message received: {}".format(msg_body))


print(__doc__)
time.sleep(1)

main = UserMain()
main.main_loop_sleep_time = 0.1
worker = UserWorker01(name="Worker_01_blocking_msg_reading", block=True)
main.register_worker(worker=worker)
worker = UserWorker02(name="Worker_02")
main.register_worker(worker=worker)

main.run()

sys.exit(0)
