from WeightSensor import WeightSensor

weight_sensor = WeightSensor()

# Call 3 functions test
output_code = weight_sensor.getAdcOutputCode()
print("Output Code: ", output_code)
voltage = weight_sensor.calculateVoltage(output_code)
print("Voltage (V): ", voltage)
weight_grams = weight_sensor.calculateWeightGrams(voltage)
print("Weight (g): ", weight_grams)

# Call getWeightGrams() test
weight_direct = weight_sensor.getWeightGrams()
print("Weight from getWeightGrams(): ", weight_direct)