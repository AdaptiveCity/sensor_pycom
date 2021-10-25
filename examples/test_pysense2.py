#!/usr/bin/env python
#

# See https://docs.pycom.io for more information regarding library specifics

import time
import pycom
import machine

from pycoproc_2 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

pycoproc = Pycoproc()
if pycoproc.read_product_id() != Pycoproc.USB_PID_PYSENSE:
    raise Exception('Not a Pysense')

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True

mp = MPL3115A2(pycoproc,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
print("\nMPL3115A2 temperature: " + str(mp.temperature())+ " deg C")
print("Altitude: " + str(mp.altitude())+" m")
mpp = MPL3115A2(pycoproc,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
print("Pressure: " + str(mpp.pressure())+ " Pa")

si = SI7006A20(pycoproc)
print("\nSI7006A20 Temperature: " + str(si.temperature()) + " deg C")
print("Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")
t_ambient = 24.4
print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + " %RH")


lt = LTR329ALS01(pycoproc)
print("\nLTR329ALS01 Light (channel Blue, channel Red): " + str(lt.light())," Lux: ", str(lt.lux()), " lux")

li = LIS2HH12(pycoproc)
print("\nLIS2HH12 Acceleration: " + str(li.acceleration()))
print("Roll: " + str(li.roll()))
print("Pitch: " + str(li.pitch()))

# set your battery voltage limits here
vmax = 4.2
vmin = 3.3
battery_voltage = pycoproc.read_battery_voltage()
battery_percentage = (battery_voltage - vmin / (vmax - vmin))*100
print("Battery voltage: " + str(battery_voltage), " percentage: ", battery_percentage)
if(pybytes_enabled):
    pybytes.send_signal(1, mpp.pressure())
    pybytes.send_signal(2, si.temperature())
    pybytes.send_signal(3, lt.light())
    pybytes.send_signal(4, li.acceleration())
    pybytes.send_battery_level(int(battery_percentage))
    print("Sent data to pybytes")
