# Evan Huizinga and Brad Ames

import spidev as spi
import gpiozero as gpio

class WeightSensor:

    # ADC Constants
    ADC_VREF = 4.096
    ADC_LEN = 10
    ADC_STEP_SIZE = .004
    ADC_CLK_SPEED = 50000
    ADC_CLK_MODE = 0b00
    ADC_MAX_WEIGHT = 350
    GRAMS_PER_POUND = 1/453.6

    def __init__(self):
        # Initalize SPI object for ADC communication
        self.adcObj = spi.SpiDev()
        self.adcObj.open(0,0)
        self.adcObj.max_speed_hz = self.ADC_CLK_SPEED
        self.adcObj.mode = self.ADC_CLK_MODE

        # Initialize push button on GPIO 23
        pbObj = gpio.InputDevice(23)

    def getAdcOutputCode(self):
        # Reads raw data from ADC and converts it into 10-bit output code
        adcData = self.adcObj.readbytes(2)
        
        firstByte = adcData[0]
        secondByte = adcData[1]

        # Mask and shift bits
        combinedNum = firstByte << 8 | secondByte
        maskedNum = (combinedNum & 0x1FF8) >> 3
        return maskedNum
        
        # maskedFirstByte = firstByte & 0x1F
        # maskedSecondByte = secondByte >> 3
        # shiftedFirstByte = maskedFirstByte << 5
        #combinedNum = shiftedFirstByte | maskedSecondByte
        # return combinedNum

    def calculateVoltage(self, outputCode):
        # Converts ADC output code to voltage.
        voltage = outputCode * self.ADC_STEP_SIZE
        return voltage
        
    def calculateWeightGrams(self, voltage):
        # Converts voltage reading to weight in grams using calibration
        weightGrams = (125 * voltage) - 14
        return weightGrams

    def getWeightGrams(self):
    # get Weight in grams in a single call instead of 3
        output_code = self.getAdcOutputCode()
        voltage = self.calculateVoltage(output_code)
        weight = self.calculateWeightGrams(voltage)
        return weight

