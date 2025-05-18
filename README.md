# GP2Y0A21YK MicroPython Library

MicroPython library for interfacing with the GP2Y0A21YK IR distance sensor.


## Features

- Read raw sensor values
- Convert raw values to voltage
- Convert raw values to distance in centimeters
- Set averaging for more stable readings
- Enable/disable the sensor via a digital pin

## Installation

To use this library, you need to copy the `gp2y0a21yk` folder to your MicroPython device.

## Usage

Here's an example of how to use the GP2Y0A21YK library in your MicroPython project.

```python
from gp2y0a21yk import GP2Y0A21YK
import machine

# Initialize the sensor (assuming the sensor is connected to ADC pin 0)
sensor = GP2Y0A21YK(0)
sensor.begin(0)

# Get distance in centimeters
distance = sensor.get_distance_centimeter()
print("Distance:", distance, "cm")
```
