from FanController import FanController
from time import sleep

fan_controller = FanController()

# Test required speeds
fan_controller.setFanSpeed(.25)
print("Fan Speed: 25%")
sleep(3)

fan_controller.setFanSpeed(.5)
print("Fan Speed: 50%")
sleep(3)

fan_controller.setFanSpeed(.75)
print("Fan Speed: 75%")
sleep(3)

fan_controller.setFanSpeed(1)
print("Fan Speed: 100%")
sleep(3)

fan_controller.setFanSpeed(0)
print("Fan Speed: 0%")
sleep(3)
