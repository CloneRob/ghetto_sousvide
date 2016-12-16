from TempControl import *
import sys

def main():
    print('Temperatur Reading')
    sensor_reader = SensorReader()
    power_cntrl = PowerController('23172412', '123141212')
    temp_cntrl = TempController(sensor_reader, power_cntrl, 21.22)
    temp_cntrl.run()
    sys.exit(1)


if __name__ == '__main__':
    main()
