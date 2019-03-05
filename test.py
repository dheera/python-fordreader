#!/usr/bin/env python3

from FordReader import FordReader
import time

f = FordReader(debug=False)
#while True:
#    print("rpm", f.read_obdii_rpm())
#    print("speed", f.read_obdii_vehicle_speed())
#    print("total_distance", f.read_obdii_total_distance())

while True:
    print("steering angle", f.read_abs_steering_angle())
    print("speed", f.read_abs_vehicle_speed())
