import machine
import time

class GP2Y0A21YK:
    LUT_3V = [
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 79,
		76, 73, 71, 69, 67, 65, 63, 62, 60, 58, 57, 52, 50, 49, 48, 47,
		49, 48, 47, 46, 45, 44, 43, 43, 42, 41, 40, 40, 39, 38, 37, 37,
		36, 36, 35, 35, 34, 33, 33, 32, 32, 31, 31, 31, 30, 30, 29, 29,
		29, 28, 28, 27, 27, 27, 26, 26, 26, 25, 25, 25, 25, 24, 24, 24,
		23, 23, 23, 23, 22, 22, 22, 22, 22, 21, 21, 21, 21, 20, 20, 20,
		20, 20, 20, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 17,
		17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
		15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14,
		13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12,
		12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11,
		11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10,
		10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  

    LUT_5V = [
		255, 127, 93, 77, 67, 60, 54, 50, 47, 44, 42, 40, 38, 36, 35, 34,
		32, 31, 30, 30, 29, 28, 27, 27, 26, 26, 25, 25, 24, 22, 20, 19,
		19, 18, 18, 17, 17, 17, 16, 16, 16, 15, 15, 15, 14, 14, 14, 13,
		13, 13, 13, 13, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 10,
		10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9,
		8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7,
		7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6,
		6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
		6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
		5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, distance_pin, vcc_pin=None):
        self._distance_pin = machine.ADC(machine.Pin(distance_pin))
        self._vcc_pin = machine.Pin(vcc_pin, machine.Pin.OUT) if vcc_pin is not None else None
        self._average = 1
        self._ref_voltage = 3.3  # Default reference voltage for most MicroPython boards
        self._enabled = False
        if self._vcc_pin:
            self.set_enabled(True)
        
    def begin(self, distance_pin, vcc_pin=None):
        self.__init__(distance_pin, vcc_pin)
        
    def set_averaging(self, avg):
        self._average = avg
        
    def get_distance_raw(self):
        return self._distance_pin.read() if self._enabled else 1023
        
    def get_distance_volt(self):
        return self._map_gp2y0a21yk_v(self.get_distance_raw())
        
    def get_distance_centimeter(self):
        return self._map_gp2y0a21yk_cm(self.get_distance_raw())
        
    def _map_gp2y0a21yk_v(self, value):
        return value * (3300 / 1023) if self._ref_voltage == 3.3 else value * (5000 / 1023)
        
    def _map_gp2y0a21yk_cm(self, value):
        sum_val = 0
        for _ in range(self._average):
            index = value // 4
            sum_val += self._transfer_function_lut(index)
        return sum_val // self._average
        
    def _transfer_function_lut(self, index):
        lut = self.LUT_3V if self._ref_voltage == 3.3 else self.LUT_5V
        return lut[index]
        
    def set_ref_voltage(self, ref_v):
        self._ref_voltage = ref_v
        
    def is_closer(self, threshold):
        return threshold > self.get_distance_centimeter()
        
    def is_farther(self, threshold):
        return threshold < self.get_distance_centimeter()
        
    def set_enabled(self, status):
        self._enabled = status
        if self._vcc_pin:
            self._vcc_pin.value(1 if self._enabled else 0)

# Example usage:
# sensor = GP2Y0A21YK(0)  # Assuming the sensor is connected to ADC0
# sensor.begin(0)  # Initialize the sensor
# distance = sensor.get_distance_centimeter()
# print("Distance:", distance, "cm")
