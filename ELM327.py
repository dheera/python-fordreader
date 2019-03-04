#!/usr/bin/env python3
import os
import serial
import struct
import sys
import time

class ELM327(object):
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 500000, timeout_serial = 0.1, timeout_response = 0.05, debug = False):
        self.debug = debug
        self.ser = serial.Serial(port, baudrate = baudrate, timeout = timeout)

        self.last_header = None
        self.last_response_address = None
        self.last_command_str = None

        self.reset()

    def reset(self):
        if debug:
            print("resetting ...")
        self.send("ATZ")    # reset
        time.sleep(0.5)
        self.send("ATS0")   # spaces off
        self.send("ATE0")   # echo off
        self.send("ATL0")   # line feeds off
        self.send("ATH1")   # headers on
        self.send("ATST%02d" % int(timeout_response / 0.004)) # response timeout

    def query(self, header, response_address, command, response_structure):
        if header != self.last_header:
            self.send("ATSH%06x" % header)
            self.last_header = header

        if response_address != self.last_response_address:
            self.send("ATCRA%08x" % response_address)
            self.last_response_address = response_address

        response_num_frames = len(response_structure)
        if command <= 0xFFFF:
            command_str = "%04x%d" % (command, response_num_frames)
        else:
            command_str = "%06x%d" % (command, response_num_frames)

        if command_str != last_command_str:
            self.send(command_str)
            last_command_str = command_str
        else:
            self.send("")

        response = self.receive(response_num_frames)

    def receive(self, num_frames):
        response = []
        for i in range(num_frames):
            response.append(self.ser.read_until('\r'))
        if debug:
            print("received:", response)
        return response

    def send(self, cmd):
        bytes_out = (cmd + "\r").encode()
        if debug:
            print("sending:", bytes_out)
        self.ser.send(bytes_out)

