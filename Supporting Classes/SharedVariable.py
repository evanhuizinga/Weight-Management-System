# Evan Huizinga & Brad Ames

from threading import Lock 

class SharedVariable:
	value = None
	lock = None

	def __init__(self, value):
		self.value = value
		self.lock = Lock()

	def set(self, value):
		self.lock.acquire()
		self.value = value
		self.lock.release()

	def get(self):
		return self.value
