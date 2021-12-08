from network import LoRa
import socket
import time
import ubinascii
import struct

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

print("Creating LoRa instance: LORAWAN / EU868")
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("LoRa instance created for dev_eui: "+ubinascii.hexlify(lora.mac()).decode('utf-8'))

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9F435D0771964CB8B6F65F4F0B470B37')
#uncomment to use LoRaWAN application provided dev_eui
dev_eui = ubinascii.unhexlify('70B3D57ED00499AC')
dev_addr = struct.unpack(">l", ubinascii.unhexlify('260BF2DE'))[0]
app_swkey = ubinascii.unhexlify('DF60E78A1701E9489E54E716B85BDA17')
nwk_swkey = ubinascii.unhexlify('C8C99A4D960334B1308BEC0C43687865')

# Uncomment for US915 / AU915 & Pygate
# for i in range(0,8):
#     lora.remove_channel(i)
# for i in range(16,65):
#     lora.remove_channel(i)
# for i in range(66,72):
#     lora.remove_channel(i)

#print("Joining Lora network OTAA with app_eui zeroes and app_key: "+ubinascii.hexlify(app_key).decode('utf-8'))
# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
#lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

print("Joining Lora network ABP with app_eui zeroes and app_key: "+ubinascii.hexlify(app_key).decode('utf-8'))
# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

print("Sending 0x010203 to LoRaWAN network")

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print("Optional received data:" + ubinascii.hexlify(data).decode('utf-8'))
