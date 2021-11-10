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

## Pygate board 'dfu-utils' firmware update

See the general instructions in the [main README of this repo](../README.md).

## Pygate pycom-fwtool update (required to get Pygate support)

* Run tools/tty.sh (simple script) to see which tty the Pygate is connected to, e.g. `/dev/ttyACM0`.
* Install `pycom-fwtool` from https://pycom.io/downloads/#firmware
* Enter command `pycom-fwtool` & follow instructions:
  - Firmware to download is `pygate`
  - Region EU868
  - do not enable pybytes support (unless you want to manage your device via Pycom's website)
* If this doesn't work first time, try again...

Two additional hints:
1. `pycom-fwtool` sometimes has problems downloading the firmware directly from the web e.g. with "Error creating Device record".
In that case you can manually download the software from https://docs.pycom.io/advance/downgrade/ and use the "install from
local file" option in `pycom-fwtool`.

2. You can confirm you have the 'Pygate' firmware installed via the REPL - this should not give an error:
```
import machine
machine.PYGATE_START_EVT
```
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

## Get the LoPy4 WiFi mac address

At the Pygate REPL prompt (i.e. via `mpfshell` or similar), get the WLAN mac address with:
```
from network import WLAN
import binascii
wl = WLAN()
binascii.hexlify(wl.mac().sta_mac)
```
e.g. we will assume `ABCDEF010203` in example below.

## Register the device to access your network (if necessary)

These instructions are for "UniOfCam-IoT" but the `config_wlan.json` file created below will allow connection to any
WiFi network with a WPA passphrase.

A guide available here: https://help.uis.cam.ac.uk/service/wi-fi/unicam-iot-wifi

The actual registration site is here: https://uws-cppm-a1.wireless.cam.ac.uk/guest/mac_index.php

After entering the wlan mac address, you will receive an email with a unique passphrase.

Copy the file `pygate/config_wlan.json` to `secrets/pygate-010203_config_wlan.json`.

Edit that file to contain the credentials for your device, e.g.
```
{
    "acp_id": "csn-pygate-010203",
    "ssid": "UniOfCam-IoT",
    "passphrase": "ijLJzEve"
}
```

Via an `mpfshell` prompt (or similar):
```
put secrets/pygate-010203_config_wlan.json config_wlan.json
```

## Test the Pygate WiFi connection

Start the `mpfshell` (or other) console to talk to the LoPy.
Copy the `ping` utility, e.g. via:
```
put examples/uping.py uping.py
put examples/test_wlan.py test_wlan.py
```

Then use the `repl` command to drop into Python on the LoPy4.

```
execfile('test_wlan.py')
```
The test should complete with a successful ping.

## Create Gateway on TTN V3 console

At https://eu1.cloud.thethings.network/console select "Gateways" and "Add Gateway".

Gateway ID: csn-pygate-[LAST 6 DIGITS OF WLAN MAC] e.g. `csn-pygate-010203`.

Gateway EUI: 16 bytes [BEEF+WLAN MAC] e.g. `BEEFABCDEF010203`

Gateway Server Address: `eu1.cloud.thethings.network`

Frequency Plan: `EU_863_870_TTN`

## Create `global_config.json`

On the TTN V3 console entry for the gateway, click the `[Download global_conf.json]` button (at bottom of gateway config).

Copy this `global_conf.json` file to `secrets/pygate-010203_global_config.json`.

Open this file in your editor. Delete the `gateway_conf` property at the bottom of the file, DELETE the comma above
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
SAVE this file ( i.e. as `secrets/pygate-010203_global_config.json`) (note the small file change from the original
`global_conf.json`, just to reduce the chance of a mixup).

Via an `mpfshell` prompt (or similar):
```
put secrets/pygate-010203_global_config.json global_config.json
```

## Copy `main.py` to the Pygate

Via an `mpfshell` prompt (or similar):
```
put pygate/main.py main.py
```

## Copy `get_time.py` to the Pygate

NTP Sync fails sometimes, especially with Ethernet, hence we use our own time sync module for RTC.
Via an `mpfshell` prompt (or similar):
```
put pygate/get_time.py get_time.py
```

## Check the required files are on the Pygate

Via an `mpfshell` prompt (or similar):
```
mpfs [/flash]> ls

Remote files in '/flash':

 <dir> ..
 <dir> cert
 <dir> lib
 <dir> sys
       boot.py
       config_wlan.json
       global_config.json
       main.py
       uping.py
```

## Start the Pygate and check it connects to TTN ok

At the Pygate REPL prompt, you can trigger a soft reboot with `Ctrl-D`.

You should see encouraging messages appearing in the REPL console saying the Pygate is connecting to TTN V3 ok, and equally
encouraging messages on the TTN console showing the Pygate springing into life. In due course you should see the
all-important `Receive uplink message ... ` messages on the TTN console, which is your sensor data flowing into the TTN
application. If so, congratulations. You should be able to unplug the USB, see the Pygate cease sending messages to the
TTN console, and re-plugging the USB should cause the Pygate to restart and reconnect.

## PoE (optional)

You can add the Pycom PoE board to the Pygate board, and if the Pygate was connecting successfully previously while
powered via USB and connecting via WiFi, it should successfully connect via the PoE/Ethernet connection.

The PoE/Ethernet connection defaults to using a DHCP client - if you want to override the `ifconfig` settings, see
https://docs.pycom.io/firmwareapi/pycom/network/eth/
