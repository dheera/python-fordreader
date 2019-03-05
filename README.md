# python-fordreader

Reads extended PID attributes from an OBD device connected to a Ford car.

Example usage:

```
#!/usr/bin/env python3

f = FordReader(port = "/dev/ttyUSB0", baudrate = 500000)
while True:
    print("rpm", f.read_obdii_rpm())
    print("speed", f.read_obdii_vehicle_speed())
    print("total_distance", f.read_obdii_total_distance())
```

Avoid switching back and forth between multiple modules. For example, if you need to read steering wheel angle and speed, instead of reading steering wheel angle from the SAS module and speed from the OBDII module, you can read both from the ABS module as follows (although the ABS reported speed has less precision than the OBDII reported speed):


```
#!/usr/bin/env python3

f = FordReader(port = "/dev/ttyUSB0", baudrate = 500000)
while True:
    print("steering angle", f.read_abs_steering_angle())
    print("speed", f.read_abs_vehicle_speed())

```


