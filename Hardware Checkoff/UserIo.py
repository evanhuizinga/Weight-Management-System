# Provided Class File for User I/O

import RPi.GPIO

class UserIo:
	PB1_GPIO_PIN = 26
	PB2_GPIO_PIN = 19
	PB3_GPIO_PIN = 13
	LED1_GPIO_PIN = 21
	LED2_GPIO_PIN = 20
	LED3_GPIO_PIN = 16
	gpio = None

	def __init__(self):
		self.gpio = RPi.GPIO
		self.gpio.setmode(self.gpio.BCM)
		inputs = [self.PB1_GPIO_PIN, self.PB2_GPIO_PIN, self.PB3_GPIO_PIN]
		self.gpio.setup(inputs, self.gpio.IN)
		outputs = [self.LED1_GPIO_PIN, self.LED2_GPIO_PIN, self.LED3_GPIO_PIN]
		self.gpio.setup(outputs, self.gpio.OUT)
		

	def turnOnLed1(self):
		self.gpio.output(self.LED1_GPIO_PIN, 1)

	def turnOffLed1(self):
		self.gpio.output(self.LED1_GPIO_PIN, 0)

	def turnOnLed2(self):
		self.gpio.output(self.LED2_GPIO_PIN, 1)

	def turnOffLed2(self):
		self.gpio.output(self.LED2_GPIO_PIN, 0)

	def turnOnLed3(self):
		self.gpio.output(self.LED3_GPIO_PIN, 1)

	def turnOffLed3(self):
		self.gpio.output(self.LED3_GPIO_PIN, 0)

	def setPushButton1Callback(self, callback):
		self.gpio.add_event_detect(self.PB1_GPIO_PIN, self.gpio.FALLING, callback=callback, bouncetime=200)
 
	def setPushButton2Callback(self, callback):
		self.gpio.add_event_detect(self.PB2_GPIO_PIN, self.gpio.FALLING, callback=callback, bouncetime=200)

	def setPushButton3Callback(self, callback):
		self.gpio.add_event_detect(self.PB3_GPIO_PIN, self.gpio.FALLING, callback=callback, bouncetime=200)
