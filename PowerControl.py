from time import gmtime, strftime
import time

class PowerController(object):
    immersion_state = False
    pump_state = False

    def __init__(self, immersion_signal, pump_signal, init_t=10):
        self.immersion_signal = immersion_signal
        self.pump_signal = pump_signal

        print('Connection to immersion heater')
        self.immersion_on()
        time.sleep(init_t)
        self.immersion_off()

        print('Connection to pump heater')
        self.pump_on()
        time.sleep(init_t)
        self.pump_off()

    def immersion_on(self):
        if not self.immersion_ison():
            print('Turning on immersion heater at ' + strftime('%Y-%m-%d %H:%M:%S', gmtime()))
            self.immersion_state = True
            PowerController.power_on(self.immersion_signal)
            return True
        else:
            return False

    def pump_on(self):
        if not self.pump_ison():
            print('Turning on pump at ' + strftime('%Y-%m-%d %H:%M:%S', gmtime()))
            self.pump_state = True
            PowerController.power_on(self.pump_signal)
            return True
        else:
            return False

    def immersion_off(self):
            print('Turning off immersion heater at ' + strftime('%Y-%m-%d %H:%M:%S', gmtime()))
            PowerController.power_off(self.immersion_signal)
            past_state = self.immersion_state
            self.immersion_state = False
            return past_state

    def pump_off(self):
        print('Turning off pump at ' + strftime('%Y-%m-%d %H:%M:%S', gmtime()))
        PowerController.power_off(self.pump_signal)
        past_state = self.pump_state
        self.pump_state = False
        return past_state

    def immersion_ison(self):
        return self.immersion_state

    def pump_ison(self):
        return self.pump_state

    @staticmethod
    def power_on(signal):
        PowerController._send(signal + ' -t')

    @staticmethod
    def power_off(signal):
        PowerController._send(signal + ' -f')

    @staticmethod
    def _send(signal):
        pass
