import pycom
import time

pycom.heartbeat(False)
while True:
    pycom.rgbled(0x000007) # green
    time.sleep(1)
    pycom.rgbled(0x000700) # yellow
    time.sleep(1)
    pycom.rgbled(0x070000) # red
    time.sleep(1)
