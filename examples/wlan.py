# For now, this example shows commands to type at the REPL.
# Note the auth password has to be created as described in cam_wifi.md
from network import WLAN
wlan = WLAN()
wlan.init(mode=WLAN.STA)
wlan.connect("UniOfCam-IoT",auth=(WLAN.WPA2,"mbRgRHsK"),hostname="ijl20-lopy4-ddc4b2")
wlan.isconnected()
wlan.ifconfig()
from uping import ping
ping('cdbb.uk')
