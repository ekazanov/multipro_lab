"""
Project: mutipro_lab. Class: ExitSignalReceiver.
"""

import signal


class ExitSignalReceiver(object):

    def __init__(self):
        self.exit_flag = False
        signal.signal(signal.SIGINT, self.set_exit_flag)
        signal.signal(signal.SIGTERM, self.set_exit_flag)

    def set_exit_flag(self, signum, frame):
        if not self.exit_flag:
            self.exit_flag = True
            return
        return


def ignore_sigint():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    return
