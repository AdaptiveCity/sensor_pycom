from network import ETH, WLAN
import time
import ujson
import machine
from machine import RTC, Pin, Timer, WDT
import pycom
from get_time import get_current_time
import socket

wdt = WDT(timeout=1250000)

class Monitor:
    def __init__(self):
        with open("boot_info.json", "r") as boot_file:
            self.boot_info = ujson.load(boot_file)
        self.boot_info["boot"]+=1
        print(self.boot_info)
        self.write_boot_info()
        self.led = 0x000000
    
    def set_led(self, colour):
        if colour == 'red':
            self.led+= 0x330000
        elif colour == 'green':
            self.led+=0x003300
        elif colour == 'blue':
            self.led+=0x000033
        else:
            self.led = 0x00000
        pycom.rgbled(self.led)

    def write_boot_info(self):
        with open('boot_info.json', 'w') as boot_file:
            boot_update = ujson.dumps(self.boot_info)
            boot_file.write(boot_update)

monitor = Monitor()

class Clock:

    def __init__(self):
        self.__alarm = Timer.Alarm(self._wdt_handler, 600, periodic=True)
        self.fail = 0

    def _wdt_handler(self, alarm):
        socket_flag = False
        try:
            s = socket.getaddrinfo('cdbb.uk',443)[0][-1]
            if s[0] == '128.232.98.113':
                socket_flag = True
        except:
            print('Unable to get address info. Possibly an internet connectivity issue.')

        if socket_flag:
            if self.fail != 0:
                self.fail == 0
            wdt.feed()
        else:
            monitor.set_led('blue')
            self.fail+=1
            if self.fail == 2:
                monitor.boot_info['reboot']+=1
                monitor.write_boot_info()
            print('Error getting address info.')


print('\nStarting LoRaWAN concentrator')
# Disable Hearbeat
pycom.heartbeat(False)

clock = Clock()

# Define callback function for Pygate events
def machine_cb (arg):
    evt = machine.events()
    if (evt & machine.PYGATE_START_EVT):
        # Green
        # pycom.rgbled(0x103300)
        monitor.set_led('green')
    elif (evt & machine.PYGATE_ERROR_EVT):
        # Red
        # pycom.rgbled(0x331000)
        monitor.set_led('red')
    elif (evt & machine.PYGATE_STOP_EVT):
        # RGB off
        # pycom.rgbled(0x000000)
        monitor.set_led('off')

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

# clock = Clock()

# Read the GW config file from Filesystem
with open('/flash/global_config.json','r') as fp:
    buf = fp.read()

# Start the Pygate
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)