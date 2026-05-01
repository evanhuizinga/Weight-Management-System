# Evan Huizinga & Brad Ames

import sys
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Hardware Checkoff')
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Supporting Classes')
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Subsystem Classes')

from queue import Queue
from SharedVariable import SharedVariable
from WeightDataAcquisition import WeightDataAcquisition
from FanSpeedController import FanSpeedController
from WeightLogManager import WeightLogManager
from UserInterface import UserInterface
from LogCommands import Command
import time

class WeightManager:
    def __init__(self):
        self.currentWeight = SharedVariable(0)
        self.cmdQ = Queue()
        self.respQ = Queue()
        self.weightSensor = WeightDataAcquisition(self.currentWeight)
        self.fanController = FanSpeedController(self.currentWeight)
        self.weightLog = WeightLogManager(self.currentWeight, self.cmdQ, self.respQ)
        self.userInterface = UserInterface(self.currentWeight, self.cmdQ, self.respQ)
        
    def start(self):
        self.weightSensor.start()
        self.fanController.start()
        self.weightLog.start()
        self.userInterface.start()
        
if __name__ == "__main__":
    weightSystem = WeightManager()
    weightSystem.start()
    
    while True:
        time.sleep(0.1) # Keep main thread alive while subsystems run