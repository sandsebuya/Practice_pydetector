# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from test import start_from,disable_module, get_event



import logging
import os
import sys
import time


class MyService:
	FIFO = '/home/nikolay/tmp'
	def __init__(self):
		self.logger = self._init_logger()
		if not os.path.exists(MyService.FIFO):
			os.mkfifo(MyService.FIFO)
		self.fifo = os.open(MyService.FIFO, os.O_RDWR | os.O_NONBLOCK)
		self.logger.info('Pydetector instance created')
	def _init_logger(self):
        	logger = logging.getLogger(__name__)
        	logger.setLevel(logging.DEBUG)
        	return logger

	def start(self):
		self.logger.info("Started up")
		start_from()
	def stop(self):
        	self.logger.info('Cleaning up...')
        	disable_module(get_event())
        	sys.exit(0)


if __name__ == '__main__':
	service = MyService()
	service.start()

# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
