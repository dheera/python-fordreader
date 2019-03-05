#!/usr/bin/env python3

import ELM327
import utils

# modules

MOD_ABS = 0x760     # Anti-lock brake system
MOD_BC = 0x726      # Body control
MOD_API = 0x7D0     # Accessory protocol interface
MOD_OBDII = 0x7E0   # OBD-II standard
MOD_SAS = 0x797     # Steering angle sensor

# commands

CMD_ABS_WHEEL_SPEED_FL = 0x222B06
CMD_ABS_WHEEL_SPEED_FR = 0x222B07
CMD_ABS_WHEEL_SPEED_RL = 0x222B08
CMD_ABS_WHEEL_SPEED_RR = 0x222B09
CMD_ABS_ACCELERATION_LON = 0x222B0C
CMD_ABS_ACCELERATION_LAT = 0x222B11
CMD_ABS_STEERING_ANGLE = 0x223302
CMD_ABS_TOTAL_DISTANCE = 0x22DD01
CMD_ABS_VEHICLE_SPEED = 0x22F40D

CMD_API_GPS = 0x228012

CMD_BC_BATTERY_CHARGE = 0x224028
CMD_BC_BATTERY_TEMPERATURE = 0x224029
CMD_BC_INSIDE_TEMPERATURE = 0x22DD04
CMD_BC_OUTSIDE_TEMPERATURE = 0x22DD05
CMD_BC_IGNITION_SWITCH = 0x22411F

CMD_OBDII_RPM = 0x22F40C
CMD_OBDII_TOTAL_DISTANCE = 0x22DD01
CMD_OBDII_VEHICLE_SPEED = 0x221505

CMD_SAS_STEERING_ANGLE = 0x22203A

class FordReader(object):
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 500000, timeout_serial = 0.1, timeout_resp = 0.05, debug = False):
        self.debug = debug
        self.device = ELM327.ELM327(port = port, baudrate = baudrate, timeout_serial = timeout_serial, timeout_resp = timeout_resp, debug = debug)

    def read_abs_acceleration_lat(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_ACCELERATION_LAT, (5,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 256.0

    def read_abs_acceleration_lon(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_ACCELERATION_LON, (5,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 256.0

    def read_abs_steering_angle(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_STEERING_ANGLE, (5,))
        if resp == None:
            return
        return (int.from_bytes(resp[0][3:], "big") - 7800) / 10.0

    def read_abs_total_distance(self):
        resp = self.device.query(MOD_OBDII, MOD_OBDII + 8, CMD_ABS_TOTAL_DISTANCE, (6,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_abs_vehicle_speed(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_VEHICLE_SPEED, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_abs_wheel_speed_fl(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_WHEEL_SPEED_FL, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_abs_wheel_speed_fr(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_WHEEL_SPEED_FR, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_abs_wheel_speed_rl(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_WHEEL_SPEED_RL, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_abs_wheel_speed_rr(self):
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_WHEEL_SPEED_RR, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_obdii_rpm(self):
        resp = self.device.query(MOD_OBDII, MOD_OBDII + 8, CMD_OBDII_RPM, (5,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 4.0

    def read_obdii_total_distance(self):
        resp = self.device.query(MOD_OBDII, MOD_OBDII + 8, CMD_OBDII_TOTAL_DISTANCE, (6,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_obdii_vehicle_speed(self):
        resp = self.device.query(MOD_OBDII, MOD_OBDII + 8, CMD_OBDII_VEHICLE_SPEED, (5,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 128.0

    def read_pc_accelerator_fraction(self):
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_ACCELERATOR_FRACTION, (5,))
        if resp == None:
            return
        return int.from_bytes(resp[3:], "big") / 255.0

    def read_api_gps(self):
        resp = self.device.query(MOD_API, MOD_API + 8, CMD_API_GPS, (6,7,7,))
        # TODO: figure out how to decode this
        return resp

