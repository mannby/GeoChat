#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Constrol ESP with MicroPython"""

import os, serial, config, time

def establishPrompt(ser, poke = True):
    """Get ESP into controllable state. Return true or false"""
    start = time.time()
    doneTime = start + config.SERIAL_CONN_TIMEOUT
    # Sometimes, would like to poke immediate, sometimes,
    # e.g. when writing line-by-line, not
    actionTime = start + config.SERIAL_POKE_TIMEOUT
    actions = ['\n', '\x03']
    sawPrompt = False
    buffer = ''
    while not sawPrompt and time.time() < doneTime:
        r = ser.read(512)
        buffer += r
        #buffer = buffer[-4:]
        if buffer[-4:] == '>>> ':
            sawPrompt = True
        else:
            if poke and time.time() > actionTime:
                actionTime += config.SERIAL_POKE_TIMEOUT
                ser.write(actions[0])
                ser.flush()
                if len(actions) > 1:
                    del actions[0]
    #if not sawPrompt or True:
    #    print "BUFFER: %s" % (buffer)
    return sawPrompt

def sendLine(ser, line):
    ser.write(line)
    ser.write('\r')
    #ser.flush()
    #print "wrote %s" % (line.strip())
    return establishPrompt(ser, False)

def writeFile(ser, filename, contents):
    """Save a file
    Precondition: Have established prompt"""
    if not sendLine(ser, 'zzz = open("%s", "w")' % (filename)):
        print 'Failed to open file %s' % (filename)
        return
    lines = contents.split('\n')
    for line in lines:
        if not sendLine(ser, 'zzz.write("%s\\n")' % (line.replace('\\', '\\\\').replace('"', '\\"'))):
            print 'Failed to write %s' % (filename)
            return
    if not sendLine(ser, 'zzz.close()'):
        print 'Failed to close %s' % (filename)

def main():
    """Do stuff"""
    ser = serial.Serial(config.CONN_NAME, config.BAUD, timeout=0)
    try:
        if establishPrompt(ser):
            print 'Got control over ESP8266'
        else:
            print 'Didn\'t get control over ESP8266'
    finally:
        ser.close()

if __name__ == "__main__":
    main()
