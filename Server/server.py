#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Global read-only values"""

import machine
import setup
import socket

setup.connectToWiFi()

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

header = """HTTP/1.1 200 OK
Content-Length: %d
Connection: Closed
Content-Type: text/html; charset=iso-8859-1

"""

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

def handleConnection():
    cl, addr = s.accept()
    print('Client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline().strip()
        if not line or len(line) == 0:
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    content = html % ('\n'.join(rows))
    response = "%s%s" % (header % len(content), content)
    cl.send(response)
    cl.close()

def main():
    while True:
        handleConnection()