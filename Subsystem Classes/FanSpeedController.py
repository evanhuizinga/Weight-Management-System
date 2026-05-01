# Evan Huizinga & Brad Ames

import sys
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Hardware Checkoff')
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Supporting Classes')

from RepeatingTimer import RepeatingTimer
from FanController import FanController
from WeightSensor import WeightSensor

class FanSpeedController:
    def __init__(self, sharedWeight):
        self.fan = FanController()
        self.sharedWeight = sharedWeight
        self.timer = RepeatingTimer(self.updateFanSpeed, .01) # 1/100 Hz = .01s
        
    def start(self):
        self.timer.start()
        
    def updateFanSpeed(self):
        weight = self.sharedWeight.get()
        speed = min(abs(weight/WeightSensor.ADC_MAX_WEIGHT), 1)
        self.fan.setFanSpeed(speed)
        