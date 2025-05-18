import types
import sys
import pytest

# Dummy hardware classes
class DummyADC:
    def __init__(self, values):
        self.values = list(values)
        self.index = 0
        self.call_count = 0
    def read(self):
        self.call_count += 1
        if self.index < len(self.values):
            val = self.values[self.index]
            self.index += 1
        else:
            val = self.values[-1]
        return val

class DummyPin:
    OUT = 0
    def __init__(self, pin, mode=None):
        self.pin = pin
    def value(self, val=None):
        pass

dummy_machine = types.ModuleType('machine')
# Will assign ADC dynamically in helper

dummy_machine.Pin = DummyPin
sys.modules['machine'] = dummy_machine

from gp2y0a21yk import GP2Y0A21YK

def create_sensor(readings):
    adc = DummyADC(readings)
    dummy_machine.ADC = lambda pin: adc
    sensor = GP2Y0A21YK(0)
    sensor.set_enabled(True)
    return sensor, adc

def test_voltage_conversion():
    sensor, adc = create_sensor([512])
    volt = sensor.get_distance_volt()
    expected = 512 * (3300 / 1023)
    assert pytest.approx(expected, rel=1e-3) == volt
    assert adc.call_count == 1

def test_centimeter_mapping():
    sensor, adc = create_sensor([200])
    cm = sensor.get_distance_centimeter()
    idx = 200 // 4
    expected = sensor.LUT_3V[idx]
    assert cm == expected
    assert adc.call_count == 1

def test_averaging_reads_multiple_times():
    readings = [200, 180, 160]
    sensor, adc = create_sensor(readings)
    sensor.set_averaging(3)
    cm = sensor.get_distance_centimeter()
    expected = (sensor.LUT_3V[50] + sensor.LUT_3V[45] + sensor.LUT_3V[40]) // 3
    assert cm == expected
    assert adc.call_count == 3
