# Evan Huizinga and Brad Ames

import pigpio
from time import sleep
import numpy as np

class FanController:
    # Constant variables
    PWM_GPIO_PIN = 12
    PWM_GPIO_FREQ = 100

    def __init__(self):
        # Initalize pigpio and configure GPIO pin
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.PWM_GPIO_PIN, pigpio.OUTPUT)
        
    def setFanSpeed(self, speed):
        # Set fan speed using PWM duty cycle (0-1)
        duty_cycle = int(speed * 1_000_000)  # pigpio uses range [0, 1e6]
        self.pwm.hardware_PWM(self.PWM_GPIO_PIN, self.PWM_GPIO_FREQ, duty_cycle)
