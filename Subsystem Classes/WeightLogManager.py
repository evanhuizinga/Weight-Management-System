# Evan Huizinga & Brad Ames

import sys
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Hardware Checkoff')
sys.path.append('/home/pi/Desktop/CSE_321L_Final/Supporting Classes')

from threading import Thread
from LogDatabase import LogDatabase
from LogCommands import Command

class WeightLogManager:
    def __init__(self, sharedWeight, cmdQ, respQ):
        self.logDB = LogDatabase()
        self.sharedWeight = sharedWeight
        self.cmdQ = cmdQ
        self.respQ = respQ
        self.prosCMD = Thread(target=self.processCommands)
        
    def start(self):
        self.prosCMD.start()
        
    def processCommands(self):
        while True:
            cmd = self.cmdQ.get()
            if cmd == Command.STORE:
                weight = self.sharedWeight.get()
                log = self.logDB.createLog(weight)
                self.logDB.storeLog(log)
                num_logs = self.logDB.fetchNumLogs()
                self.respQ.put(num_logs)
            elif cmd == Command.FETCH:
                logs = self.logDB.fetchLogs()
                self.respQ.put(logs)
            elif cmd == Command.ERASE:
                self.logDB.storeNumLogs(0)
                self.respQ.put(0)
