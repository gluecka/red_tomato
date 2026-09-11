import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time
import datetime
import statistics
from calculator_transformator import SensorValueTrasformator
import json

# read config.json File
with open('config.json', 'r') as f:
    config = json.load(f)

# BCM --> take the numbers of the pins like on the raspberry plan
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

# create object of i2c bus
i2c = busio.I2C(board.SCL, board.SDA)

# create object of ADC (Analog Digital Converter) using i2c bus
ads = ADS.ADS1115(i2c)

# write values in a list and calculate the average value
while True:
    list_of_values = []
    for x in range(config['list_loop_counter_trigger']):
        try:
            sensor_output = AnalogIn(ads, ADS.P0)
            list_of_values.append(sensor_output.value)
        except:
            list_of_values.append(100)
        time.sleep(0.5)

# if a boolean variable is true, the wathering is started, if false, the wathering is stopped
# create decision object and set the necessary values
    object_decision = SensorValueTrasformator(list_of_values)

    try:
        if object_decision.trigger_decision == True:
            GPIO.setup(26, GPIO.OUT)

            print(f'Percentage: {object_decision.percent_calculation}')
            print("Wathering is started")

            time.sleep(config['wathering_time'])
            GPIO.setup(26, GPIO.IN)

            print("Wathering is stopped")

            time.sleep(config['effect_time'])
        else:
            GPIO.setup(26, GPIO.IN)
            time.sleep(1)
    except:
        GPIO.setup(26, GPIO.IN)
        time.sleep(1)

    del list_of_values # -> delete the list to free up memory