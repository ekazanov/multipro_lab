#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
The BaseApp multiprocess application example.
Run main class and two workers.

1. Create the UserMain class.

2. Create the UserWorker classes.

3. Run the everything.

4. Exit by the Ctrl-C.
"""
from __future__ import print_function

__author__ = "Evgeny Kazanov"

import time

from multipro_lab.main import Main
from multipro_lab.worker import Worker


class UserWorker(Worker):

    def __init__(self, *args, **kwargs):
        super(UserWorker, self).__init__(*args, **kwargs)
        self.main_loop_sleep_time = 1

    def worker_action(self):
        print("UsersWorker: {}".format(self.name))
        return


class UserMain(Main):

    def main_action(self):
        print("UserMain.main_action()")
        return


print(__doc__)
time.sleep(1)

main = UserMain()
main.main_loop_sleep_time = 0.5
worker = UserWorker(name="Worker 01")
main.register_worker(worker=worker)
worker = UserWorker(name="Worker 02")
main.register_worker(worker=worker)
main.run()
