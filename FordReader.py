#!/usr/bin/env python3

import ELM327
import utils

# modules

MODULE_ABS = 0x760     # Anti-lock brake system
MODULE_API = 0x7D0     # Accessory protocol interface
MODULE_OBDII = 0x7E0   # OBD-II standard
MODULE_PC = 0x7E8      # Powertrain control
MODULE_SAS = 0x797     # Steering angle sensor

# pids

PID_ABS_STEERING_ANGLE = 0x223302

PID_API_GPS = 0x228012

PID_OBDII_VEHICLE_SPEED = 0x221505
PID_OBDII_RPM = 0x22F40C

PID_PC_ACCELERATOR_FRACTION = 0x22032B

PID_SAS_STEERING_ANGLE = 0x22203A

class FordReader(object):
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 500000, timeout_serial = 0.1, timeout_response = 0.05, debug = False):
        self.debug = debug
        self.device = ELM327(port = port, baudrate = baudrate, timeout_serial = timeout_serial, timeout_response = timeout_response, debug = debug)

    def read_abs_steering_angle(self):
        response = self.device.query(
            MODULE_ABS,
            MODULE_ABS + 8,
            PID_ABS_STEERING_ANGLE,
            (5))
        if response == None:
            return
        return (utils.bytes2int(x[3:4]) - 7800) / 10.0

    def read_obdii_vehicle_speed(self):
        response = self.device.query(
            MODULE_OBDII,
            MODULE_OBDII + 8,
            PID_OBDII_VEHICLE_SPEED,
            (5))
        if response == None:
            return
        return utils.bytes2int(x[3:4]) / 128.0

    def read_obdii_rpm(self):
        response = self.device.query(
            MODULE_OBDII,
            MODULE_OBDII + 8,
            PID_OBDII_RPM,
            (5))
        if response == None:
            return
        return utils.bytes2int(x[3:4]) / 4.0

    def read_pc_accelerator_fraction(self):
        response = self.device.query(
            MODULE_PCM,
            MODULE_PCM + 8,
            PID_PC_ACCELERATOR_FRACTION,
            (5))
        if response == None:
            return
        return utils.bytes2int(x[3:4]) / 255.0

    def read_api_gps(self):
        response = self.device.query(
            MODULE_API,
            MODULE_API + 8,
            PID_API_GPS,
            (6,7,7))
        # TODO: figure out how to decode this
        return response

