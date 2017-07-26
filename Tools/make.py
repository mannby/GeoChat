#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Make ESP"""

import os, serial, esp8266, config

CODE_DIR = '../Server'
FILE_DIR = '../Static'

CODE_EXTENSIONS = set(['.py'])
STATIC_EXTENSIONS = set(['.html'])

def code_files():
    """Return list of python files"""
    files = os.listdir(CODE_DIR)
    return [i for i in files if os.path.splitext(i)[1] in CODE_EXTENSIONS]

def static_files():
    """Return list of static files"""
    files = os.listdir(FILE_DIR)
    return [i for i in files if os.path.splitext(i)[1] in STATIC_EXTENSIONS]

def copy_file(ser, filedir, filename):
    """Copy a file to the ESP"""
    print 'Copy %s' % (filename)
    contents = open("%s/%s" % (filedir, filename)).read()
    esp8266.writeFile(ser, filename, contents)

def copy_files(ser):
    """Copy files to ESP"""
    print '=== Code files'
    for filename in code_files():
        copy_file(ser, CODE_DIR, filename)
    print '=== Static files'
    for filename in static_files():
        copy_file(ser, STATIC_DIR, filename)

def main():
    """Do stuff"""
    # Device resets on close on serial port?
    ser = serial.Serial(config.CONN_NAME, config.BAUD, timeout=0)
    try:
        if not esp8266.establishPrompt(ser):
            print 'Failed to establish MicroPython prompt'
            return
        else:
            print 'Got MicroPython prompt'
        copy_files(ser)
    finally:
        ser.close()

if __name__ == "__main__":
    main()
