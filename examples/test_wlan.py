# For now, this example shows commands to type at the REPL.
# Note the auth password has to be created as described in cam_wifi.md

ssid = "Forster-Lewis"
passphrase = "middlehall"

from network import WLAN
import ubinascii
from uping import ping
import time

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

print("Connecting to "+ssid+" with passphrase "+passphrase)
#wlan.connect("UniOfCam-IoT",auth=(WLAN.WPA2,"mbRgRHsK"),hostname="ijl20-lopy4-ddc4b2")
wlan.connect(ssid,auth=(WLAN.WPA2,passphrase),hostname="ijl20-lopy4-ddc4b2")

time.sleep(2)

while not wlan.isconnected():
    print("Waiting to connect to "+ssid)
    time.sleep(1)

print("Connected status:" + str(wlan.isconnected()))

print("IP settings: " + str(wlan.ifconfig()))

print("Ping test:")
ping('cdbb.uk')
