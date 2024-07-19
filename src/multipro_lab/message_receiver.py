"""
Project: mutipro_lab. Class: MessageReceiver.
"""

from multiprocessing import Queue
from queue import Empty


class MessageReceiver(object):
    """
    Message format:
        ["<msg_type>", <msg_body>]

    Where:
        <msg_type> - String.
        <msg_body> - any valid Python type.
    """

    def __init__(self, block=False):
        self.message_handler_d = {}
        self.in_q = Queue()
        self.block = block

    def register_handler(self, message_type=None, message_handler=None):
        self.message_handler_d[message_type] = message_handler
        return

    def _get_message(self):
        try:
            msg_type, msg_body = self.in_q.get(block=self.block)
        except Empty:
            return (None, None)
        return (msg_type, msg_body)

    def get_messages(self):
        # In blocking mode get one message.
        if self.block:
            msg_type, msg_body = self._get_message()
            self.message_handler_d[msg_type](msg_body)
            return
        # Get all messages in non blocking mode.
        while True:
            msg_type, msg_body = self._get_message()
            if (msg_type, msg_body) == (None, None):
                break
            # Execute message handler
            self.message_handler_d[msg_type](msg_body)
        return
