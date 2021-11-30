import pycom
import time
import machine

pycom.heartbeat(False)
pycom.heartbeat_on_boot(False)
pycom.wifi_on_boot(False)

time.sleep(0.1)
pycom.rgbled(0x00ff00) # green
time.sleep(0.1)
pycom.rgbled(0x000000) # off
time.sleep(0.1)

machine.sleep(500)

time.sleep(0.1)
pycom.rgbled(0x00ff00) # green
time.sleep(0.1)
pycom.rgbled(0x000000) # off
time.sleep(0.1)

machine.deepsleep(3000)
