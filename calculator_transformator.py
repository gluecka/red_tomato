import json
import statistics
import datetime

class ConfigClass:
    # define the path of configfile directly in init line as parameter
    def __init__(self, config_path='config.json'):
        
        # open and put the config data in a self.... parameter
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # for loop with each key - value pair to deploy that for further operations
        for key, value in self.config.items():
            setattr(self, key, value)



class SensorValueTrasformator(ConfigClass):
    def __init__(self, imput_value: list):
        # inherit the parameters of parents class
        super().__init__()
        self.imput_value = imput_value

    @property
    def percent_calculation(self) -> float:
            self.low_wather = self.config['low_wather']
            self.high_wather = self.config['high_wather']
            self.list_of_soil_condition = []

            for sensor in self.imput_value:

                if sensor >= self.low_wather:
                    soil_condition = 0
                elif sensor <= self.high_wather:
                    soil_condition = 100
                else:
                    gradient = -100 / (self.low_wather - self.high_wather)
                    y_distance = 100 - (gradient * self.high_wather)
                    soil_condition = round(gradient * sensor + y_distance, 2)
                self.list_of_soil_condition.append(soil_condition)

            soil_condition = round(statistics.mean(self.list_of_soil_condition), 2)
            return soil_condition

    @property
    def time_check(self) -> bool:
        self.start_wathering_time_range = self.config['start_wathering_time_range']
        self.stop_wathering_time_range = self.config['stop_wathering_time_range']

        start_time = datetime.time(self.start_wathering_time_range, 0, 0)
        stop_time = datetime.time(self.stop_wathering_time_range, 0, 0)

        if start_time <= datetime.datetime.now().time() or datetime.datetime.now().time() <= stop_time:
            return True
        else:
            return False

    @property
    def trigger_desicion(self) -> bool:
        def __init__(self):
            self.trigger_limit = self.config['trigger_limit']

        if self.percent_calculation <= self.trigger_limit and self.time_check == True:
            return True
        else:
            return False