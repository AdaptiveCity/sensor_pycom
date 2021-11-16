from network import ETH, WLAN
import time
import ujson
import machine
from machine import RTC, Pin, Timer
import pycom
from get_time import get_current_time
import socket

class Clock:

    def __init__(self):
        self.seconds = 0
        self.__alarm = Timer.Alarm(self._rtc_handler, 1200, periodic=True)

    def _rtc_handler(self, alarm):
        # Sync time using a socket connection to a local website
        pycom.rgbled(0x00007f)
        print('Syncing RTC...', end='')
        rtc = RTC()
        print('Current RTC..', rtc.now())
        current_time = get_current_time()
        print('Web time.. ' + str(current_time))
        rtc.init(current_time)
        print('RTC OK.. ' + str(rtc.now()))
        time.sleep(10)
        pycom.rgbled(0x103300)

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

# check if the PyEthernet module is connected
print('PyEthernet Pins: ',[Pin('P17')(), Pin('P18')(), Pin('P19')(), Pin('P21')(), Pin('P22')(), Pin('P23')()])
pyethernet_pin_active = sum([Pin('P17')(), Pin('P18')(), Pin('P19')(), Pin('P21')(), Pin('P22')(), Pin('P23')()]) >= 4

# Try the Ethernet Connection first
print('Trying to connect ethernet...',end='')
timer = 0
eth_flag = False

if pyethernet_pin_active:
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
else:
   print('PyEthernet not connected or faulty.')

# Connect to WiFi if Ethernet not available
if not eth_flag:
    print('Ethernet Connection not available')
    print('Loading Wifi config from config_wlan.json...')
    with open("config_wlan.json", "r") as wc:
        wc = ujson.load(wc)

    # Connect to a Wifi Network
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(ssid=wc["ssid"], auth=(WLAN.WPA2, wc["passphrase"]), hostname=wc["acp_id"])

    wlan_connect_count = 0
    while not wlan.isconnected():
        if wlan_connect_count == 30:
            print("WLAN not connected for 30 seconds - rebooting")
            machine.reset()
        print('.', end='')
        wlan_connect_count += 1
        time.sleep(1)
    print(" OK\n")

    # Loop until we have an IP address
    ip_connected_count = 0
    while True:
        if ip_connected_count == 30:
            print("No wlan IP address after 30 seconds, rebooting")
            machine.reset()
        ips = wlan.ifconfig()
        if ips[0] != '0.0.0.0':
            print('WLAN connection successful with '+ips[0])
            break
        print('WLAN IP not ready '+str(ips))
        ip_connected_count += 1
        time.sleep(1)

    print("Connected status:" + str(wlan.isconnected()))

    print("IP settings: " + str(wlan.ifconfig()))

# Sync time using a socket connection to a local website
print('Syncing RTC...', end='')
rtc = RTC()
current_time = get_current_time()
print('Web time.. ' + str(current_time))
rtc.init(current_time)
print('RTC OK.. ' + str(rtc.now()))

clock = Clock()

# Read the GW config file from Filesystem
with open('/flash/global_config.json','r') as fp:
    buf = fp.read()

# Start the Pygate
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)