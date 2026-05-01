# Evan Huizinga & Brad Ames

import sys
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Hardware Checkoff')
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Supporting Classes')

from UserIo import UserIo
from threading import Thread
from LogDatabase import LogDatabase
from WeightSensor import WeightSensor
from LogCommands import Command
import time

class UserInterface:

	def __init__(self, currentWeight, cmdQ, respQ):
		# Initialize Object
		self.currentWeight = currentWeight
		self.currentThreshold = WeightSensor.ADC_MAX_WEIGHT
		self.maxNumLogs = LogDatabase.MAX_NUM_LOGS
		self.logsEmpty = False
		self.logsFull = False
		self.userIo = UserIo()
		self.cmdQ = cmdQ
		self.respQ = respQ
		self.terminalIntf = Thread(target=self.terminalInterface)
		self.physicalIntf = Thread(target=self.physicalInterface)
		
	def start(self):
		# Start Threads
		self.terminalIntf.start()
		self.physicalIntf.start()

	def pbCallback(self, channel):
		if channel == UserIo.PB1_GPIO_PIN:
			self.cmdQ.put(Command.STORE)
			num_logs = self.respQ.get()
			if num_logs >= self.maxNumLogs:
				self.logsFull = True
			self.logsEmpty = False
		elif channel == UserIo.PB2_GPIO_PIN:
			self.cmdQ.put(Command.FETCH)
			resp = self.respQ.get()
			print(resp)
		elif channel == UserIo.PB3_GPIO_PIN:
			self.cmdQ.put(Command.ERASE)
			self.respQ.get() # Wait for confirmation before updating status
			self.logsEmpty = True
			self.logsFull = False
		
		self.printMenu()

	def physicalInterface(self):
		self.userIo.setPushButton1Callback(self.pbCallback)
		self.userIo.setPushButton2Callback(self.pbCallback)
		self.userIo.setPushButton3Callback(self.pbCallback)

		while True:
			weight = self.currentWeight.get()
			time.sleep(0.1) # Small delay to lower CPU usage

			# Turn on LED 1 if logs are empty, else turn it off
			if self.logsEmpty:
				self.userIo.turnOnLed1()
			else:
				self.userIo.turnOffLed1()

			# Turn on LED 2 if logs are full, else turn it off
			if self.logsFull:
				self.userIo.turnOnLed2()
			else:
				self.userIo.turnOffLed2()

			# Turn on LED 3 if weight is above threshold, else turn it off
			if weight > self.currentThreshold:
				self.userIo.turnOnLed3()
			else:
				self.userIo.turnOffLed3()

			

	def printMenu(self):
		print()
		print("0 - Print current weight")
		print("1 - Update log weight threshold")
		print("2 - Force storing of the currently held log")
		print("3 - Fetch/Print all of the logs to the screen.")
		print("4 - Clear all logs in non-volatile memory")
		print()

	def terminalInterface(self):
		# Check storage with fetch command
		self.cmdQ.put(Command.FETCH)
		resp = self.respQ.get()
		if len(resp) == 0:
			self.logsEmpty = True
		while(1):
			self.printMenu()
			option = int(input("Option :"))
			print()

			if option == 0:
				print(f"Current weight: {self.currentWeight.get(): .2f} grams")
			elif option == 1:
				self.currentThreshold = float(input("New weight threshold (grams): "))
			elif option == 2:
				self.cmdQ.put(Command.STORE)
				num_logs = self.respQ.get()
				if num_logs >= self.maxNumLogs:
					self.logsFull = True
				self.logsEmpty = False
			elif option == 3:
				self.cmdQ.put(Command.FETCH)
				resp = self.respQ.get()
				print(resp)
			elif option == 4:
				self.cmdQ.put(Command.ERASE)
				self.respQ.get() # Wait for confirmation before updating status
				self.logsEmpty = True
				self.logsFull = False
			else:
				print("Invalid option.")