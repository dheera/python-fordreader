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
        """Resets the device and sets parameters ready for querying."""
        if self.debug:
            print("resetting ...")

        self.reset_buffers()

        self.send("ATZ")    # reset
        time.sleep(1)

        self.reset_buffers()

        if self.debug:
            print("setting parameters ...")

        self.send_and_wait_for_ok("ATE0")   # echo off
        self.send_and_wait_for_ok("ATS0")   # spaces off
        self.send_and_wait_for_ok("ATL0")   # line feeds off
        self.send_and_wait_for_ok("ATH0")   # headers on
        self.send_and_wait_for_ok("ATST%02d" % int(self.timeout_resp / 0.004)) # resp timeout

        time.sleep(0.5)

        self.reset_buffers()

    def query(self, header, resp_address, command, resp_structure):
        """
        Issues a CAN query expecting a response.
        header: message header, usually related to the module you expect to hear from
        resp_address: the module you actually want to hear from, usually header + 8
        command: the command, often 22xxxx for extended PIDs
        resp_structure: a tuple of ints indicating the structure you expect back.
          For example (4,) means you expect a single line message with 4 bytes.
          (6,6) means you expect two lines each with 6 bytes.
        """
        if self.debug:
            print("query: ", header, resp_address, command, resp_structure)

        if header != self.last_header:
            self.send_and_wait_for_ok("ATSH%06x" % header)
            self.last_header = header

        if resp_address != self.last_resp_address:
            self.send_and_wait_for_ok("ATCRA%08x" % resp_address)
            self.last_resp_address = resp_address

        resp_num_frames = len(resp_structure)
        if command <= 0xFFFF:
            command_str = "%04x%d" % (command, resp_num_frames)
        else:
            command_str = "%06x%d" % (command, resp_num_frames)

        self.ser.reset_input_buffer()
        self.send(command_str)

        resp = self.receive_message()

        if resp == None:
            return

        if tuple(map(len, resp)) != resp_structure:
            if self.debug:
                print("response did not match expected structure", resp)
                return

        return resp

    def receive(self):
        """Receives a single line over serial, agnostic to the content of the line."""
        if self.debug:
            print("receive")

        line = self.ser.read_until(b'\r')
        return(line)

    def receive_message(self):
        """
        Receives a CAN bus message, including multi-line messages, in which case
        it repeatedly calls receive() until it gets the correct number of bytes.
        A single line message looks like this:
        DEADBEEF
        A multi line message looks like this (refer to ELM327 documentation):
        010
        0:DEADBEEF
        1:5ADDBEEF
        where 010 specifies the total number of bytes expected to be received (in hex).
        """
        resp = [] 

        if self.debug:
            print("receive_message")

        line = self.receive().replace(b'>',b'').replace(b'\r',b'')

        if b'NO DATA' in line:
            return

        if b'CAN ERROR' in line:
            return

        i = 0

        if len(line) == 3:
            # multi line message
            total_num_bytes = int.from_bytes(binascii.unhexlify(b"0" + line), byteorder = "big")
            received_num_bytes = 0

            if self.debug:
                print("begin multi-line response for bytes: ", total_num_bytes)

            while received_num_bytes < total_num_bytes and i < 10:
                line = self.receive().replace(b'>', b'').replace(b'\r',b'')
                try:
                    line_bytes = binascii.unhexlify(line[2:])
                    received_num_bytes += len(line_bytes)
                    resp.append(line_bytes)
                except binascii.Error:
                    if self.debug:
                        print("error: received:", line)
                    return

                # give up if 10 consecutive receives fail to give the correct total number of bytes
                i += 1

        else:
            # single-line message
            try:
                line_bytes = binascii.unhexlify(line)
                resp.append(line_bytes)
            except binascii.Error:
                if self.debug:
                    print("error: received:", line)
                return

        if self.debug:
            print("received:", resp)

        return resp

    def send(self, cmd):
        """
        Sends a line.
        """
        if self.debug:
            print("send", cmd)

        bytes_out = (cmd + "\r").encode()
        self.ser.write(bytes_out)

    def send_and_wait_for_ok(self, cmd):
        """
        Sends a command and blocks until it receives OK, or
        gives up after 10 tries. Used for AT commands.
        """
        if self.debug:
            print("send_and_wait_for_ok", cmd)

        for i in range(10):
            if self.debug:
                print("send attempt", i)
            self.reset_buffers()
            self.send(cmd)
            resp = self.receive()
            if b"OK" in resp:
                if self.debug:
                    print("received OK, exiting", resp)
                return
            else:
                if self.debug:
                    print("did not receive OK, received ", resp)

        if self.debug:
            print("giving up")

    def reset_buffers(self):
        """Clears serial input and output buffers."""
        if self.debug:
            print("reset_buffers")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

