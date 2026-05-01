# Evan Huizinga and Brad Ames

from smbus2 import SMBus, i2c_msg
import numpy as np
from datetime import datetime

class LogDatabase:

    # Constant Variables
    MEM_SIZE = 512
    BASE_ADDR = 0x000
    NUM_LOGS_ADDR = 0x002
    FIRST_LOG_ADDR = 0x004
    LOG_SIZE = 6
    MAX_NUM_LOGS = 127

    I2C_ID = 0x51

    def __init__(self):
        # Initalize I2C
        self.fram = SMBus(1)

    def float2bytes(self, floatingPt):
        # Convert float to 4-byte list for storage
        if type(floatingPt) != float:
            raise Exception("float2bytes expects type 'float'.")

        floatBytes = np.float32(floatingPt).tobytes()
        return [int(np.ubyte(b)) for b in floatBytes]

    def bytes2float(self, floatBytes):
        # Convert 4-byte list back to float
        if type(floatBytes) != list:
            raise Exception("bytes2float expects type 'list'.")
        elif len(floatBytes) != 4:
            raise Exception("bytes2float expects 4 bytes.")

        return np.frombuffer(bytes(floatBytes), dtype=np.float32)[0]

    def getDeviceStruct(self, dev_addr, mem_addr, data, rbuf):
        # Create I2C read/write structures for FRAM access
        if type(mem_addr) == int:
            temp_addr = [(mem_addr >> 8) & 0xFF, mem_addr & 0xFF]
        else:
            temp_addr = mem_addr

        if rbuf > 0:
            write = i2c_msg.write(dev_addr, temp_addr)
            read = i2c_msg.read(dev_addr, rbuf)
            return (write, read)
        else:
            write = i2c_msg.write(dev_addr, temp_addr + data)
            return (write, None)

    def storeByte(self, addr, byte):
        # Write a single byte to given memory address
        (w, _) = self.getDeviceStruct(self.I2C_ID, addr, [byte], 0)
        self.fram.i2c_rdwr(w)                     

    def fetchByte(self, addr):
        # Read a single byte from given memory address
        (w, r) = self.getDeviceStruct(self.I2C_ID, addr, [], 1)
        self.fram.i2c_rdwr(w, r)
        return list(r)[0]

    def storeBlock(self, addr, byteList):
        # Write multiple bytes starting at given address
        for i in range(len(byteList)):
            self.storeByte(addr + i, byteList[i])

    def fetchBlock(self, addr, numBytes):
        # Read multiple bytes starting at given address
        return [self.fetchByte(addr + i) for i in range(numBytes)]

    def eraseBlock(self, addr, numBytes):
        # Clear a block of memory by writing zeros
        for i in range(numBytes):
            self.storeByte(addr + i, 0x00)

    def getTimeOfDay(self):
        # Get current time as [hour, minute]
        now = datetime.now()
        return [now.hour, now.minute]

    def createLog(self, weight):
        # Create log entry with time and weight bytes
        timeOfDay = self.getTimeOfDay()
        weightBytes = self.float2bytes(weight)
        return timeOfDay + weightBytes

    def fetchNumLogs(self):
        # Retrieve number of stored logs
        return self.fetchByte(self.NUM_LOGS_ADDR)

    def storeNumLogs(self, numLogs):
        # Store number of logs in metadata
        self.storeByte(self.NUM_LOGS_ADDR, numLogs)

    def incrementNumLogs(self):
        # Increment stored log count by 1
        num_logs = self.fetchNumLogs()
        self.storeNumLogs(num_logs + 1)

    def storeLog(self, log):
        # Store new log in next available location
        num_logs = self.fetchNumLogs()

        if num_logs >= self.MAX_NUM_LOGS:
            print("Error: Log memory full.")
            return

        addr = self.FIRST_LOG_ADDR + (num_logs * self.LOG_SIZE)
        self.storeBlock(addr, log)
        self.incrementNumLogs()

    def fetchLogs(self):
        # Retrieve all stored logs from memory
        num_logs = self.fetchNumLogs()
        logs = []

        for i in range(num_logs):
            addr = self.FIRST_LOG_ADDR + (i * self.LOG_SIZE)
            logs.append(self.fetchBlock(addr, self.LOG_SIZE))

        return logs
