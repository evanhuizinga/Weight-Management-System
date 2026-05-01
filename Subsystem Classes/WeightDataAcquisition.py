# Evan Huizinga & Brad Ames

import sys
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Hardware Checkoff')
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Supporting Classes')

from RepeatingTimer import RepeatingTimer
from WeightSensor import WeightSensor

class WeightDataAcquisition:
    def __init__(self, sharedWeight):
        self.weightSensor = WeightSensor()
        self.sharedWeight = sharedWeight
        self.timer = RepeatingTimer(self.readWeight, .02)
        
    def start(self):
        self.timer.start()
        
    def readWeight(self):
        output_code = self.weightSensor.getAdcOutputCode()
        voltage = self.weightSensor.calculateVoltage(output_code)
        weight = self.weightSensor.calculateWeightGrams(voltage)
        self.sharedWeight.set(weight)
