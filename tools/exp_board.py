#!/usr/bin/env python3

import re
import subprocess

def get_path_by_id(device_id):
    device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus').decode(), dinfo.pop('device').decode())
                devices.append(dinfo)
    for device in devices:
        if device['id'].decode() == device_id:
            return device


usb_id = '04d8:ef98'
d = get_path_by_id(usb_id)

for i in d:
    print(i, d[i])
