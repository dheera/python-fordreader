#!/usr/bin/env python3

import ELM327

# modules

MOD_ABS = 0x760     # Anti-lock brake system
MOD_BC = 0x726      # Body control
MOD_API = 0x7D0     # Accessory protocol interface
MOD_OBDII = 0x7E0   # OBD-II standard
MOD_PC = 0x7E0      # Powertrain control
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

CMD_SAS_STEERING_ANGLE = 0x22203A

CMD_OBDII_RPM = 0x22F40C
CMD_OBDII_TOTAL_DISTANCE = 0x22DD01
CMD_OBDII_VEHICLE_SPEED = 0x221505

CMD_PC_ACCELERATOR_FRACTION = 0x22032B
CMD_PC_PRESSURE_BAROMETRIC = 0x22F433
CMD_PC_TEMPERATURE_AMBIENT = 0x22057D
CMD_PC_TEMPERATURE_INTAKE = 0x22F40F
CMD_PC_TIME_SINCE_ENGINE_START = 0x221126
CMD_PC_TOTAL_DISTANCE = 0x22DD01


class FordReader(object):
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 500000, timeout_serial = 0.1, timeout_resp = 0.05, debug = False):
        self.debug = debug
        self.device = ELM327.ELM327(port = port, baudrate = baudrate, timeout_serial = timeout_serial, timeout_resp = timeout_resp, debug = debug)

    ### ABS Anti-lock brake system ###

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
        resp = self.device.query(MOD_ABS, MOD_ABS + 8, CMD_ABS_TOTAL_DISTANCE, (6,))
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

    ### API Accesory protocol interface ###

    def read_api_gps(self):
        """GPS location of the car. Returns a dict with lat, lon, heading fields."""
        resp = self.device.query(MOD_API, MOD_API + 8, CMD_API_GPS, (6,7,7))
        if resp == None:
            return
        lat = int.from_bytes(resp[1][1:3], "big", signed=True) / 60.0
        lon = int.from_bytes(resp[1][5:7], "big", signed=True) / 60.0
        heading = int.from_bytes(resp[2][3:5], "big") / 1.0
        return {"lat": lat, "lon": lon, "heading": heading}

    ### OBDII Standard methods ###

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

    ### PC Powertrain control ###

    def read_pc_accelerator_fraction(self):
        """How much the gas pedal is depressed, from 0.0 (not pressed) to 1.0 (full)."""
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_ACCELERATOR_FRACTION, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 255.0

    def read_pc_pressure_barometric(self):
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_PRESSURE_BAROMETRIC, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_pc_temperature_ambient(self):
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_TEMPERATURE_AMBIENT, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 2.0 - 40

    def read_pc_temperature_intake(self):
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_TEMPERATURE_INTAKE, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") - 40

    def read_pc_time_since_engine_start(self):
        """Time since engine started, in seconds. Maxes out at 255."""
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_TIME_SINCE_ENGINE_START, (4,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    def read_pc_total_distance(self):
        resp = self.device.query(MOD_PC, MOD_PC + 8, CMD_PC_TOTAL_DISTANCE, (6,))
        if resp == None:
            return
        return int.from_bytes(resp[0][3:], "big") / 1.0

    ### SAS Steering angle sensor

    def read_sas_steering_angle(self):
        resp = self.device.query(MOD_SAS, MOD_SAS + 8, CMD_SAS_STEERING_ANGLE, (6,6,7))
        if resp == None:
            return
        angle_sign = int.from_bytes(resp[1][4]) * 2 - 1
        angle_mag = int.from_bytes(resp[0][3:5]) * (90.0 / 2048.0)
        return angle_sign * angle_mag

