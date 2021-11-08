from network import ETH, WLAN
import time
import ujson
import machine
from machine import RTC
import pycom
from get_time import get_current_time
import socket

print('\nStarting LoRaWAN concentrator')
# Disable Hearbeat
pycom.heartbeat(False)

# Define callback function for Pygate events
def machine_cb (arg):
    evt = machine.events()
    if (evt & machine.PYGATE_START_EVT):
        # Green
        pycom.rgbled(0x103300)
    elif (evt & machine.PYGATE_ERROR_EVT):
        # Red
        pycom.rgbled(0x331000)
    elif (evt & machine.PYGATE_STOP_EVT):
        # RGB off
        pycom.rgbled(0x000000)

# register callback function
machine.callback(trigger = (machine.PYGATE_START_EVT | machine.PYGATE_STOP_EVT | machine.PYGATE_ERROR_EVT), handler=machine_cb)

# Try the Ethernet Connection first
print('Trying to connect ethernet...',end='')
timer = 0
eth_flag = False
try:
   eth = ETH()
   eth.init()

   while not eth.isconnected():
       print('.',end='')
       time.sleep(1)
       timer += 1
       if timer > 10: break

   if eth.isconnected():
       print('Ethernet Connected OK')
       print(eth.ifconfig())
       eth_flag = True
except:
    print('Ethernet Exception')

# Connect to WiFi if Ethernet not available
if not eth_flag:
    print('Ethernet Connection not available')
    print('Loading Wifi config from config_wlan.json...')
    with open("config_wlan.json", "r") as wc:
        wc = ujson.load(wc)

    print('Connecting '+wc["acp_id"]+' to WiFi ssid '+wc["ssid"]+'.',end='')

    # Connect to a Wifi Network
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(ssid=wc["ssid"], auth=(WLAN.WPA2, wc["passphrase"]), hostname=wc["acp_id"])

    while not wlan.isconnected():
        print('.', end='')
        time.sleep(1)    
    print(wlan.ifconfig())
    print("WLAN Connected OK\n")

# Ensure that the interface is ready
time.sleep(2)

# Sync time using a socket connection to a local website
print('Syncing RTC...', end='')
rtc = RTC()
current_time = get_current_time()
print('Web time.. ' + str(current_time))
rtc.init(current_time)
print('RTC OK.. ' + str(rtc.now()))

# Read the GW config file from Filesystem
with open('/flash/global_config.json','r') as fp:
    buf = fp.read()

# Start the Pygate
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)
