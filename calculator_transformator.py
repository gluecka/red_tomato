import json
import statistics

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


    # @percent_calculation
    # def trigger_desicion(self) -> bool:
    #     def __init__(self):
    #         self.trigger_limit = self.config['trigger_limit']

    #     if soil_condition <= self.trigger_limit:
    #         return True
    #     else:
    #         return False