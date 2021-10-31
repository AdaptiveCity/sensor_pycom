import pycom
import time

pycom.heartbeat(False)
while True:
    print("blue")
    pycom.rgbled(0x000007) # blue
    time.sleep(1)
    print("green")
    pycom.rgbled(0x000700) # green
    time.sleep(1)
    print("red")
    pycom.rgbled(0x070000) # red
    time.sleep(1)
