# Pycom Sensors

Install (includes mpfshell):
```
git clone https://github.com/AdaptiveCity/sensor_pycom
cd sensor_pycom
python -m venv venv
source venv/bin/activate
python -m pip install pip --upgrade
python -m pip install wheel
python -m pip install -r requirements.txt
```

## Development tools

Essentially this is TTY access to the 'REPL' interface to MicroPython on the LoPy boards, plus the
ability to upload/download files including `boot.py` and `main.py`. TBH after you get the `>>>` REPL
prompt plus the file xfer ability, these tools are pretty similar.

## mpfshell

https://github.com/wendlers/mpfshell

The latest version (Oct 2021) 1.9.2 has issues that caused it NOT to work on my Ubuntu 20.04 workstation (other people are
reporting the same issue). Downgrading to 1.9.1 worked fine with `pip install mpfshell==0.9.1`

### Notes on Pymakr (from Pycom - install issues with serialport)


https://pycom.io/products/supported-networks/pymakr/

Git repo with useful install tips: https://atom.io/packages/pymakr

This is the 'obvious' choice from pycom. It's an add-on package for Atom or VS Code. A caveat is there are many Node/Python
dependencies (see install tips) and often you need to upgrade/downgrade other software on your workstation.

Personally I prefer the tool to connect to the LoPy NOT integrated into one of my editors.

### Notes on Pybytes (from Pycom)

https://pybytes.pycom.io

This requires a pycom login, and is the 'cloud' version of their dev environment incorporating an online version pf Pymakr. LoPy
boards have built in pybytes support

It relies on the WiFi support built into the LoPy, and the LoPy board will connect back to pycom.io which can then control
your board.

So Pycom provide a fair amount of value-add but it's up to you whether you want your boards to be connecting to pycom or not.

## Notes on rshell

https://github.com/dhylands/rshell

Simple python pip install on your workstation
Pretty old - on my Linux machine this would crash any time I tried transferring files to the LoPy - there are interweb threads
discussing timing issues with the code.

