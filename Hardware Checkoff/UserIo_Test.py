from UserIo import UserIo
import time
import RPi.GPIO as GPIO

def testCallbackFunction (channel):
    print(f"Button pressed on channel: {channel}")

user_io = UserIo()
time.sleep(0.5)

print("Waiting for button press")

user_io.setPushButton1Callback(testCallbackFunction)
user_io.setPushButton2Callback(testCallbackFunction)
user_io.setPushButton3Callback(testCallbackFunction)

try:
    while True:
        user_io.turnOnLed1()
        user_io.turnOnLed2()
        user_io.turnOnLed3()
        time.sleep(1)

        user_io.turnOffLed1()
        user_io.turnOffLed2()
        user_io.turnOffLed3()
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping test")
    GPIO.cleanup()