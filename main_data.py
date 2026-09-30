import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time
import datetime
from calculator_transformator import SensorValueTrasformator
from influxdb import InfluxDBClient
import os
from dotenv import load_dotenv
load_dotenv()


#import from .env File
USER = os.environ.get('INFLUX_USER')
PASSWORD = os.environ.get('INFLUX_PASSWORD')
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('INFLUX_DATABASE')
PORT = os.environ.get('INFLUX_PORT')

# BCM --> take the numbers of the pins like on the raspberry plan
GPIO.setmode(GPIO.BCM)
# GPIO.setup(26, GPIO.IN) set correct gpio !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# create object of i2c bus
i2c = busio.I2C(board.SCL, board.SDA)

# create object of ADC (Analog Digital Converter) using i2c bus
ads = ADS.ADS1115(i2c)

while True:
    list_of_values = []
    # loop to collect data from sensor
    for x in range(10):
        try:
            sensor_output = AnalogIn(ads, ADS.P0)
            list_of_values.append(sensor_output.value)
        except:
            list_of_values.append(100)
        time.sleep(0.5)
    
    object_percent = SensorValueTrasformator(list_of_values)

    if object_percent.trigger_decision == True:
        status = 1
    else:
        status = 0


    # !!!!!!!!!!!!!!!!!!! create post request to influxDB !!!!!!!!!!!!!!!!!!!!!!

    # set influx client object
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DATABASE)

    json_payload = []

    data_1 = {
        'measurement' : 'soil_condition',
        'time' : datetime.datetime.now(),
        'fields' : {
        'Status Bewässerung' : status,
        'Erdfeuchtigkeit' : object_percent.percent_calculation
        }
    }

    json_payload.append(data_1)

    # write data in influxdb
    # client.write_points(json_payload)
    print(json_payload)
    del json_payload, list_of_values
    time.sleep(2)


    # activate write mode 
    # set correct host on ip of docker
    # deactivate line with print mode