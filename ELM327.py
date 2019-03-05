#!/usr/bin/env python3
import os
import serial
import struct
import sys
import time

class ELM327(object):
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 500000, timeout_serial = 0.1, timeout_resp = 0.05, debug = False):
        self.debug = debug
        self.ser = serial.Serial(port, baudrate = baudrate, timeout = timeout_serial)

        self.last_header = None
        self.last_resp_address = None
        self.last_command_str = None
        self.timeout_resp = timeout_resp

        self.reset()

    def reset(self):
        if self.debug:
            print("resetting ...")
        self.send("ATZ")    # reset
        time.sleep(1.0)
        self.send("ATS0")   # spaces off
        time.sleep(0.1)
        self.send("ATE0")   # echo off
        time.sleep(0.1)
        self.send("ATL0")   # line feeds off
        time.sleep(0.1)
        self.send("ATH0")   # headers on
        time.sleep(0.1)
        self.send("ATST%02d" % int(self.timeout_resp / 0.004)) # resp timeout
        time.sleep(0.1)

        self.ser.reset_input_buffer()

    def query(self, header, resp_address, command, resp_structure):
        if header != self.last_header:
            self.send("ATSH%06x" % header)
            self.last_header = header

        if resp_address != self.last_resp_address:
            self.send("ATCRA%08x" % resp_address)
            self.last_resp_address = resp_address

        resp_num_frames = len(resp_structure)
        if command <= 0xFFFF:
            command_str = "%04x%d" % (command, resp_num_frames)
        else:
            command_str = "%06x%d" % (command, resp_num_frames)

        self.ser.reset_input_buffer()
        self.send(command_str)

        resp = self.receive(resp_num_frames)

    def receive(self, num_frames):
        resp = []
        for i in range(num_frames):
            resp.append(self.ser.read_until(b'\r'))
        if self.debug:
            print("received:", resp)
        return resp

    def send(self, cmd):
        bytes_out = (cmd + "\r").encode()
        if self.debug:
            print("sending:", bytes_out)
        self.ser.write(bytes_out)

