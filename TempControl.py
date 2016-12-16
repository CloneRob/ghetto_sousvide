from collections import deque
from SensReader import *
from PowerControl import *
import time

class TempController(object):
    immersion_temp = 0.0
    meat_temp1 = 0.0
    meat_temp2 = 0.0
    meat_delta = 0.0
    temp_hist = deque([], 10)

    def __init__(self, sensor_reader, power_controller, target_t):
        self.sensor_reader = sensor_reader
        self.power_controller = power_controller
        self.target_t = target_t

    def update(self, debug=False):
        try:
            # self.immersion_temp, self.meat_temp1, self.meat_temp2 = self.sensor_reader.temperature_list()
            self.immersion_temp, self.meat_temp1, self.meat_temp2 = self.sensor_reader.temperature_list()[0], 3.0, 3.7
        except ValueError:
            emsg = 'One ore more sensors stopped responding\nPower will be shutting off'
            self.power_controller.immersion_off()
            self.power_controller.pump_off()
            raise SensorError(emsg)


        self.meat_delta = (self.meat_temp1 + self.meat_temp2)/2.0
        self.temp_hist.append((self.immersion_temp, self.meat_temp1, self.meat_temp2))
        print('Current immersion temp: {}, and meat1, meat2: {} {}'
                .format(self.immersion_temp, self.meat_temp1, self.meat_temp2))
        

    def run(self):
        threshold_t = self.target_t - 1.0
        while(True):
            self.update()
            if (self.immersion_temp < threshold_t):
                self.power_controller.immersion_on()
            elif (self.immersion_temp - self.meat_delta < 1.0 and self.meat_delta < self.target_t):
                self.power_controller.immersion_on()
                self.power_controller.pump_on()
            elif (self.immersion_temp >= self.target_t):
                self.power_controller.immersion_off()
                if self.meat_delta < self.target_t:
                    self.power_controller.pump_on()
                else:
                    self.power_controller.pump_off()
            time.sleep(1)
