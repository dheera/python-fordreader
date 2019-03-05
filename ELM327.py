#!/usr/bin/env python3
import os
import serial
import struct
import sys
import time
import binascii

class ELM327(object):
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 500000, timeout_serial = 0.1, timeout_resp = 0.02, debug = False):
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

        self.ser.reset_input_buffer()
        self.send("ATZ")    # reset
        time.sleep(0.1)
        self.ser.reset_input_buffer()
        time.sleep(1)
        resp = self.ser.read_until(b'>')
        self.send("ATS0")   # spaces off
        resp = self.ser.read_until(b'>')
        self.send("ATE0")   # echo off
        resp = self.ser.read_until(b'>')
        self.send("ATL0")   # line feeds off
        resp = self.ser.read_until(b'>')
        self.send("ATH0")   # headers on
        resp = self.ser.read_until(b'>')
        self.send("ATST%02d" % int(self.timeout_resp / 0.004)) # resp timeout
        resp = self.ser.read_until(b'>')

        self.ser.reset_input_buffer()

    def query(self, header, resp_address, command, resp_structure):
        if header != self.last_header:
            self.ser.reset_input_buffer()
            self.send("ATSH%06x" % header)
            self.ser.read_until(b'>')
            self.last_header = header

        if resp_address != self.last_resp_address:
            self.ser.reset_input_buffer()
            self.send("ATCRA%08x" % resp_address)
            self.ser.read_until(b'>')
            self.last_resp_address = resp_address

        resp_num_frames = len(resp_structure)
        if command <= 0xFFFF:
            command_str = "%04x%d" % (command, resp_num_frames)
        else:
            command_str = "%06x%d" % (command, resp_num_frames)

        self.ser.reset_input_buffer()
        self.send(command_str)

        resp = self.receive(resp_num_frames)

        if resp == None:
            return

        for i, line in enumerate(resp):
            if resp_structure[i] != len(line):
                if self.debug:
                    print("invalid response, discarding")
                return

        return resp

    def receive(self, num_frames):
        resp = []
        if num_frames > 1:
            line = self.ser.read_until(b'\r')

        for i in range(num_frames):
            line = self.ser.read_until(b'\r')
            line = line.replace(b'\r',b'')
            line = line.replace(b'>',b'')
            line = line.replace(b'\r',b'')

            if len(line) >= 3 and line[1:2] == b':':
                line = line[2:]

            try:
                line_bytes = binascii.unhexlify(line)
            except binascii.Error:
                if self.debug:
                    print("error: received:", line)
                return

            resp.append(line_bytes)

        if self.debug:
            print("received:", resp)

        return resp

    def send(self, cmd):
        bytes_out = (cmd + "\r").encode()
        if self.debug:
            print("sending:", bytes_out)
        self.ser.write(bytes_out)

