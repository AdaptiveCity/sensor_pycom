#!/usr/bin/env python
# author: ijl20

# See https://docs.pycom.io for more information regarding library specifics

import time
import pycom
import machine

from pycoproc_2 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01

from network import LoRa
import socket
import time
import ubinascii

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9F435D0771964CB8B6F65F4F0B470B37')
# Note for the TTN registration you can find the LoPy4 preset dev_ui via:
# >>> from network import LoRa
# >>> lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# >>> ubinascii.hexlify(lora.mac())
# You do not need to set this value in this code

pycom.heartbeat(False)
pycom.rgbled(0x000007) # blue
time.sleep(1)
pycom.rgbled(0x000000) # off
time.sleep(1)
pycom.rgbled(0x000007) # blue

pycoproc = Pycoproc()
if pycoproc.read_product_id() != Pycoproc.USB_PID_PYSENSE:
    raise Exception('Not a Pysense')

si = SI7006A20(pycoproc)
print("\nSI7006A20 Temperature: " + str(si.temperature()) + " deg C")

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

print("Creating LoRa instance: LORAWAN / EU868")
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("LoRa instance created for dev_eui: "+ubinascii.hexlify(lora.mac()).decode('utf-8'))

#uncomment to use LoRaWAN application provided dev_eui
#dev_eui = ubinascii.unhexlify('70B3D549938EA1EE')

# Uncomment for US915 / AU915 & Pygate
# for i in range(0,8):
#     lora.remove_channel(i)
# for i in range(16,65):
#     lora.remove_channel(i)
# for i in range(66,72):
#     lora.remove_channel(i)

print("Joining Lora network OTAA with app_eui zeroes and app_key: "+ubinascii.hexlify(app_key).decode('utf-8'))
# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
pycom.rgbled(0x000700) # green

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

print("Sending 0xFF00 to LoRaWAN network")

# send some data
s.send(bytes([0xff, 0x00]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print("Optional received data:" + ubinascii.hexlify(data).decode('utf-8'))

pycom.rgbled(0x000000) # off

while True:
    for i in range(10):
        time.sleep(29.5) # Sleep for 29.5 seconds
        pycom.rgbled(0x000700) # green
        time.sleep(0.5) # Sleep for 0.5 seconds
        pycom.rgbled(0x000000) # off

    pycom.rgbled(0x000007) # blue
    time.sleep(2) # Sleep for 2 seconds

    temp = si.temperature()
    print("Read temperature " + str(temp) + " C")
    temp_byte0 = int(temp) # This only works for +ve temperatures
    temp_byte1 = int((temp - temp_byte0) * 100)
    msg_bytes = bytearray([temp_byte0, temp_byte1])
    s.setblocking(True)

    print("Sending "+ str(ubinascii.hexlify(msg_bytes)) + " to LoRaWAN network")

    # send some data
    s.send(msg_bytes)

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print("Optional received data:" + ubinascii.hexlify(data).decode('utf-8'))

    pycom.rgbled(0x000000) # off
