#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Timer class to be used in an event loop.
"""

__author__ = "Evgeny Kazanov"

import sys
import time


class Timer(object):
    """ """

    def __init__(self, interval=None, one_time=False):
        """Timer class to be used in an event loop.

        Usage:
            1) Before the event loop create a timer object:
                timer_obj = Timer(interval=<Interval, s>)
            2) In the event loop call check_timer:
                timer_obj.check_timer()
            3) If at the call moment the current time does not exeed
               the initialisaton_time + interval, check_timer()
               returns False.
            4) If at the call moment the current time exeeds the
               initialisaton_time + interval, check_timer() returns
               True one time. Every next call returns False to the
               moment when time exeeds initialisaton_time + interval * 2,
               etc.
            5) If one_time argument is True, timer returns True only one
               time.
        """
        self._prev_time = time.time()
        self.interval = interval
        self.one_time = one_time
        self.do_nothing = False

    def check_timer(self):
        if self.do_nothing:
            return False
        cur_time = time.time()
        if cur_time - self.interval >= self._prev_time:
            self._prev_time = cur_time
            if self.one_time:
                self.do_nothing = True
            return True
        else:
            return False


if __name__ == "__main__":
    TIMER_02 = Timer(interval=2.0)
    TIMER_03_5 = Timer(interval=3.5)
    TIMER_07_ONE_TIME = Timer(interval=7, one_time=True)
    TIMER_15_EXIT = Timer(interval=15, one_time=True)
    time_cnt = 0
    while True:
        time.sleep(0.1)
        time_cnt += 1
        print("{}".format(time_cnt))
        if TIMER_02.check_timer():
            print("TIMER_02")
        if TIMER_03_5.check_timer():
            print("TIMER_03_5")
        if TIMER_07_ONE_TIME.check_timer():
            print("TIMER_07_ONE_TIME")
        if TIMER_15_EXIT.check_timer():
            print("TIMER_15_EXIT")
            break
    sys.exit(0)
