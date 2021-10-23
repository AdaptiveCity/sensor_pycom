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

## Create/copy `main.py` and `global_config.json`

See this repo /pygate directory, with an example `main.py` and `global_config.json`
