import glob
import os
import time

class DigitalSensors:
    def __init__(self):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = os.path.join(device_folder, 'w1_slave')
    
    def __read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        return lines
    
    def read_temp(self):
        lines = self.__read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return round(temp_c, 2)