# Pygate

## Pygate Assembly

Components:
* Pygate board
* LoPy4 board (or alternative)
* Pygate case
* LoRa antenna with IPX tail connector
* USB C cable

Assemble:
* Connect LoPy4 onto Pygate board
* Connect Lora antenna tail to Pygate board (NOT the LoPy4)
* Place board in Pygate Case BOTTOM (insert USB first, than settle board on pegs)
* From screws/buttons bag place button inserts in slots
* On Pygate case TOP: Thread antenna plug (on end of tail) through existing hole, affix nut.
* Place TOP of case on BOTTOM - buttons should click on press - affix with 4 screws.
* Attach via USB C cable to your PC

## Firmware update (required to get Pygate support)

* Run tools/tty.sh (simple script) to see which tty the Pygate is connected to, e.g. `/dev/ttyACM0`.
* Install `pycom-fwtool` from https://pycom.io/downloads/#firmware
* Enter command `pycom-fwtool` & follow instructions:
  - Firmware to download is `pygate`
  - Region EU868
* If this doesn't work first time, try again...

## Connect a TTY to the Pygate LoPy4

Install the serial tool of your choice, e.g. `pymakr`, `rshell`, `mpfshell`.

My personal preference is `mpfshell` but frankly any that works is ok. Generally you have issues relating to serial
port support.

The basic idea of this console support is you have two levels of prompt, i.e. initially you
see `mpfs [/flash]>` which is like a 'command line' prompt (Ctr-D to exit) supporting `get` and `put` commands for file transfer, and
the `repl` command drops you into the LoPy Python interpreter prompt (Ctrl-] to quit).
The README instructions for installing this repo include installing `mpfshell` (it's a Python program), e.g.
here's a console log:
```
(venv) ijl20@ijl20-tosh-laptop:~/src/sensor_pycom/examples$ mpfshell ttyACM0
Connected to LoPy4

** Micropython File Shell v0.9.2, sw@kaltpost.de **
-- Running on Python 3.8 using PySerial 3.5 --

mpfs [/flash]> put uping.py
mpfs [/flash]> repl
>
*** Exit REPL with Ctrl+] ***

Pycom MicroPython 1.20.2.r4 [v1.11-ffb0e1c] on 2021-01-12; LoPy4 with ESP32
Type "help()" for more information.
>>>
```

## Test the Pygate WiFi connection

Start the `mpfshell` (or other) console to talk to the LoPy.
Copy the `ping` utility, e.g. via:
```
put examples/uping.py uping.py
```

Then use the `repl` command to drop into Python on the LoPy4, and enter the following. You will see results occasionally
between the statements (e.g. wlan.isconnected() should return `True`).

For the `wlan.connect()` you must insert the correct SSID and WPA passphrase.

```
from network import WLAN
wlan = WLAN()
wlan.init(mode=WLAN.STA)
wlan.connect(<SSID>,auth=(WLAN.WPA2,<PASSPHRASE>))
wlan.isconnected()
wlan.ifconfig()
from uping import ping
ping('cdbb.uk')
```

## Create Gateway on TTN V3 console

At the Pygate REPL prompt (i.e. via `mpfshell` or similar), get the WLAN mac address with:
```
from network import WLAN
import binascii
wl = WLAN()
binascii.hexlify(wl.mac().sta_mac)
```
e.g. we will assume `ABCDEF010203` in example below.

At https://eu1.cloud.thethings.network/console select "Gateways" and "Add Gateway".

Gateway ID: csn-pygate-[LAST 6 DIGITS OF WLAN MAC] e.g. `csn-pygate-010203`.

Gateway EUI: [BEEF<WLAN MAC] e.g. `BEEFABCDEF010203`

Gateway Server Address: `eu1.cloud.thethings.network`

Frequency Plan: `EU_863_870_TTN`

## Create `global_config.json`

On the TTN V3 console entry for the gateway, click the `[Download global_conf.json]` button (at bottom of gateway config).

Open the `global_conf.json` file in your editor. Delete the `gateway_conf` property at the bottom of the file, DELETE the comma above
that property to keep the JSON valid.

Add a NEW `gateway_conf` property (I recommend at the top, it is easier to find) containing the TTN `Gateway EUI`
property value as the `gateway_ID` property in the file. E.g.:
```
    "gateway_conf": {
        "gateway_ID": "BEEFABCDEF010203",
        "server_address": "eu1.cloud.thethings.network",
        "serv_port_up": 1700,
        "serv_port_down": 1700,
        "keepalive_interval": 10,
        "stat_interval": 30,
        "push_timeout_ms": 100,
        "forward_crc_valid": true,
        "forward_crc_error": false,
        "forward_crc_disabled": false
    },
```
SAVE this file as `gateway_config.json` (note the small file change from `gateway_conf.json`, just to reduce the chance of
a mixup). This file (`gateway_config.json`) will be loaded by `main.py`.

## Create `main.py`

This assumes you have already checked connecting the Pygate to your WiFi network is going to work by testing with the
steps earlier in this README.

Copy the file `pygate/main.py` and open with your editor.

For typical home WPA passphrase authentication, edit the line
```
wlan.connect(ssid='<YOUR SSID>', auth=(WLAN.WPA2, "<YOUR PASSPHRASE>"))
```
to contain the correct SSID and passphrase for your WiFi network. If you are using enterprise authentication, then try
```
wlan.connect(ssid='YOUR SSID', auth=(WLAN.WPA2_ENT, 'username', 'password'))
```
Save the file as `main.py` - you will be downloading this file to the Pygate.

## Copy `main.py` and `global_config.json` to the Pygate.

Using your console tool, e.g. `mpfshell`, copy `main.py` and `global_config.json` from your PC to the Pygate.

At the Pygate REPL prompt, you can trigger a soft reboot with `Ctrl-D`.

You should see encouraging messages appearing in the REPL console saying the Pygate is connecting to TTN V3 ok, and equally
encouraging messages on the TTN console showing the Pygate springing into life. In due course you should see the
all-important `Receive uplink message ... ` messages on the TTN console, which is your sensor data flowing into the TTN
application. If so, congratulations.
