#!/usr/bin/env python3

from FordReader import FordReader
import time

f = FordReader(debug=True)
while True:
    f.read_obdii_rpm()
    time.sleep(0.01)
