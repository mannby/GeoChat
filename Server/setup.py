#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Global read-only values"""

import network, time, config

def connectToWiFi():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network %s' % (config.CONN_WIFI))
        sta_if.active(True)
        sta_if.connect(config.CONN_WIFI, config.CONN_PASSWORD)
        maxtries = 10
        while maxtries > 0 and not sta_if.isconnected():
            maxtries -= 1
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())
