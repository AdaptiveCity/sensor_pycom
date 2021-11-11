#
# WiFi test script
#
# REQUIRED:
#   config_wlan.json - contains wifi passphrase
#   uping.py         - for ping test


from network import WLAN
import ubinascii
from uping import ping
import machine
from machine import RTC
import time
import ujson

print("Instantiating WLAN")
wlan = WLAN()

print("Calling wlan.init()")
wlan.init(mode=WLAN.STA)

mac_str = ubinascii.hexlify(wlan.mac().sta_mac).decode('utf-8')
print("Using WiFi mac address: "+mac_str)

print("Scanning for WiFi networks")
ssids = wlan.scan()
if len(ssids) == 0:
    print("No WiFi networks found")
else:
    for s in ssids:
        print("    found ssid "+s[0])

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
print(" OK\n")

# Loop until we have an IP address
ip_connected_count = 0
while True:
    if ip_connected_count == 20:
        print("No wlan IP address after 20 seconds, rebooting")
        machine.reset()
    ips = wlan.ifconfig()
    if ips[0] != '0.0.0.0':
        print('WLAN connection successful with '+ips[0])
        #break
    print('WLAN IP not ready '+str(ips))
    ip_connected_count += 1
    time.sleep(1)

print("Connected status:" + str(wlan.isconnected()))

print("IP settings: " + str(wlan.ifconfig()))

# Sync time via NTP server for GW timestamps on Events
print('Syncing RTC via ntp...', end='')
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

while not rtc.synced():
    print('.', end='')
    time.sleep(.5)
print(" OK\n")

print("Ping test (cdbb.uk):")
ping('cdbb.uk')
