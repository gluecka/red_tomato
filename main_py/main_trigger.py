import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time
import datetime
import statistics
# from models import SensorValueTrasformator
# import json

# read config.json File
# with open('config.json', 'r') as f:
#     config = json.load(f)

# BCM --> take the numbers of the pins like on the raspberry plan
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

# # create i2c bus
i2c = busio.I2C(board.SCL, board.SDA)

# create object of ADC (Analog Digital Converter) using i2c bus
ads = ADS.ADS1115(i2c)

sensor_output = AnalogIn(ads, ADS.P0)



# set the allowed wathering time
focus_hour = 23

timecheck = datetime.time(focus_hour, 0, 0)

if timecheck > datetime.datetime.now().time():
    print(datetime.datetime.now().strftime("%H:%M:%S"))
    print(sensor_output.value)
else:
    print("Time is not after 21:00:00")


# test
GPIO.setup(26, GPIO.OUT)
time.sleep(2)
GPIO.setup(26, GPIO.IN)