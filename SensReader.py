import os
import sys

class SensorError(Exception):
    pass

def sensor_list():
    sensors_file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
    w1_slaves = [w1_slave.split('\n')[0] for w1_slave in sensors_file.readlines()]
    sensors_file.close()
    return w1_slaves

class SensorReader(object):

    def __init__(self):
        self.sensors = sensor_list()
        self.n_sensors = len(self.sensors)

    def get_sensors(self):
        return self.sensors

    @staticmethod
    def poll_temperature(sensor):
        sensor_file = open('/sys/bus/w1/devices/' + sensor + '/w1_slave')
        sensor_data = sensor_file.read()
        sensor_file.close()
        temp_asstr = sensor_data.split('\n')[1].split('=')[1]
        return float(temp_asstr)/1000

    def temperature_list(self):
        temp_list = []
        for sensor in self.sensors:
            temp_list.append(SensorReader.poll_temperature(sensor))

        return temp_list
