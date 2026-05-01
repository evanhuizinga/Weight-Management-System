# Evan Huizinga & Brad Ames

from threading import Timer

class RepeatingTimer(object):

	def __init__(self, function, interval, *args):
		super(RepeatingTimer, self).__init__()
		self.args = args
		self.function = function
		self.interval = interval

	def start(self):
		self.callback()
		
	def stop(self):
		self.interval = False
		
	def callback(self):
		if self.interval:
			self.function(*self.args)
			Timer(self.interval, self.callback, ).start()
