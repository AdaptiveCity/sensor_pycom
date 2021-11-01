# Pycom example files

## Hints

* Read the example `.py` program BEFORE downloading to the LoPy - at the top of the file you may find lib file references which need
downloading to the LoPy `lib` directory (as with `test_pysense2.py` below), or there may be unique settings needed for your
usage (e.g. the `test_wlan.py` example requires you set SSID and PASSPHRASE values for your WiFi network).

* The examples below use the `mpfshell` to interact with the LoPy (i.e. to transfer files and provide a serial terminal
connection to the LoPy micropython REPL loop). Alternatives include `rshell` and `pymakr`.

## Example, using test_pysense2.py

Clone this repo as in `sensor_pycom/README.md`.

If necessary, use `tools/tty.sh` to check your /dev/ttyACMx entries.

In this example we will assume `ttyACM0`, and will use `examples/test_pysense2.py` as the example program.

So FIRST, view `test_pysense2.py` in your editor, and you will see it requires additional libraries due to
the following imports:
```
from pycoproc_2 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2
```
These libraries can be found at https://github.com/pycom/pycom-libraries, and this repo contains copies
in `libs/pysense2`. We will transfer the files to the LoPy using `mpfshell`. Note that `mpfshell` appears
to have commands to transfer multiple files (`mput`) but these might be buggy and it was easier for
me to transfer the files one at a time using the TAB autocompletion which worked ok for me on Linux.

Note the 'local' commands (`lcd`, `lpwd`, `lls`) refer to files on your PC, while the regular commands
(`cd`, `pwd`, `ls`) refer to the LoPy.

```
$ mpfshell ttyACM0
Connected to LoPy4

** Micropython File Shell v0.9.1, sw@kaltpost.de **
-- Running on Python 3.8 using PySerial 3.5 --

mpfs [/flash]> cd lib
mpfs [/flash/lib]> lcd libs/pysense2
mpfs [/flash/lib]> lls

Local files:

       SI7006A20.py
       LIS2HH12.py
       pycoproc_2.py
       MPL3115A2.py
       LTR329ALS01.py

mpfs [/flash/lib]> put SI7006A20.py SI7006A20.py
mpfs [/flash/lib]> put LIS2HH12.py LIS2HH12.py
mpfs [/flash/lib]> put pycoproc_2.py pycoproc_2.py
mpfs [/flash/lib]> put MPL3115A2.py MPL3115A2.py
mpfs [/flash/lib]> put LTR329ALS01.py LTR329ALS01.py
mpfs [/flash/lib]> ls

Remote files in '/flash/lib':

 <dir> ..
       LIS2HH12.py
       LTR329ALS01.py
       MPL3115A2.py
       SI7006A20.py
       pycoproc_2.py

mpfs [/flash/lib]> cd ..
mpfs [/flash]>
```
Now we will use similar commands to copy the `test_pysense2.py` program:
```
$ mpfshell ttyACM0
Connected to LoPy4

** Micropython File Shell v0.9.1, sw@kaltpost.de **
-- Running on Python 3.8 using PySerial 3.5 --

mpfs [/flash]>
```
At `mpfs` prompt use `put` command to copy `test_pysense2.py` from PC to LoPy:
```
mpfs [/flash]> lcd examples
mpfs [/flash]> put test_pysense2.py test_pysense2.py
mpfs [/flash]> ls

Remote files in '/flash':

 <dir> ..
 <dir> cert
 <dir> lib
 <dir> sys
       boot.py
       main.py
       test_pysense2.py

mpfs [/flash]>
```
At the REPL prompt, we can execute the test program with the python `execfile`:
```
$ mpfshell ttyACM0
Connected to LoPy4

** Micropython File Shell v0.9.1, sw@kaltpost.de **
-- Running on Python 3.8 using PySerial 3.5 --

mpfs [/flash]> repl
>
*** Exit REPL with Ctrl+] ***

Pycom MicroPython 1.20.2.r4 [v1.11-ffb0e1c] on 2021-01-12; LoPy4 with ESP32
Pybytes Version: 1.6.1
Type "help()" for more information.
>>> execfile("test_pysense2.py")
MPL3115A2 temperature: 23.3125
Altitude: 2.1875
Pressure: 101315.2
Temperature: 24.74003 deg C and Relative Humidity: 46.82974 %RH
Dew point: 12.5992 deg C
Humidity Ambient for 24.4 deg C is 47.76081%RH
Light (channel Blue, channel Red): (102, 59)  Lux:  246.2267 lx
Acceleration: (-0.02709961, 0.00402832, 1.024048)
Roll: 1.515877
Pitch: -0.239812
Battery voltage: 4.701756
Battery voltage: 4.701756  percentage:  102.5053
>>>
```
At this point you can exit the REPL python prompt with `Ctrl-]` and then quit `mpfshell` with `Ctrl-D`.

## test_wlan.py

This script will test your wifi connection.

### Step 1. Get the LoPy4 WiFi mac address

At the REPL prompt (i.e. via `mpfshell` or similar), get the WLAN mac address with:
```
from network import WLAN
import binascii
wl = WLAN()
binascii.hexlify(wl.mac().sta_mac)
```
e.g. we will assume `ABCDEF010203` in example below.

### Step 2. Register the device to access your network (if necessary)

These instructions are for "UniOfCam-IoT" but the `config_wlan.json` file created below will allow connection to any
WiFi network with a WPA passphrase.

A guide available here: https://help.uis.cam.ac.uk/service/wi-fi/unicam-iot-wifi

The actual registration site is here: https://uws-cppm-a1.wireless.cam.ac.uk/guest/mac_index.php

After entering the wlan mac address, you will receive an email with a unique passphrase.

### Step 3. Give the LoPy4 the required WiFi credentials

Copy the file `examples/config_wlan.json` to `secrets/config_wlan.json`.

Edit that file to contain the credentials for your device, e.g.
```
{
    "acp_id": "ijl20-lopy4-010203",
    "ssid": "UniOfCam-IoT",
    "passphrase": "ijLJzEve"
}
```

Via an `mpfshell` prompt (or similar):
```
put secrets/config_wlan.json config_wlan.json
```

###  Step 4. Copy `uping.py` and `test_wlan.py` to the LoPy4

Via an `mpfshell` prompt (or similar):
```
put examples/uping.py uping.py
put examples/test_wlan.py test_wlan.py
```


## Run `test_wlan.py`

Via an `mpfshell` prompt (or similar):
```
mpfs [/flash]> repl
>
*** Exit REPL with Ctrl+] ***

Pycom MicroPython 1.20.2.r6 [v1.11-c5a0a97] on 2021-10-28; LoPy4 with ESP32
Type "help()" for more information.
>>> execfile("test_wlan.py")
```
If successful, you will see something like:
```
Instantiating WLAN
Calling wlan.init()
Using WiFi mac address: ABCDEF010203
Scanning for WiFi networks
    found ssid UniOfCam-IoT
    found ssid w-107-CB3-0FD
    found ssid eduroam
    found ssid UniOfCam
    found ssid UniOfCam-Guest
    found ssid co2mesh
    found ssid Internal-CL
    found ssid wgb
Loading Wifi config from config_wlan.json...
Connecting ijl20-lopy4-d67e6c to WiFi ssid UniOfCam-IoT..... OK

Connected status:True
IP settings: ('10.254.236.12', '255.252.0.0', '10.255.255.254', '131.111.8.42')
Syncing RTC via ntp..... OK

Ping test (cdbb.uk):
PING cdbb.uk (128.232.98.113): 64 data bytes
84 bytes from 128.232.98.113: icmp_seq=1, ttl=61, time=7.051000 ms
84 bytes from 128.232.98.113: icmp_seq=2, ttl=61, time=8.395000 ms
84 bytes from 128.232.98.113: icmp_seq=3, ttl=61, time=12.400000 ms
84 bytes from 128.232.98.113: icmp_seq=4, ttl=61, time=10.401000 ms
4 packets transmitted, 4 packets received
>>>
```
