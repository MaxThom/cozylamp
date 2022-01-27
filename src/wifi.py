import socket
import network
import time
from machine import Pin
import config

#led = Pin(2, Pin.OUT)
AP_SSID = 'esp32-sunlight'
AP_PASSWORD = '123456789'

MAX_WAIT_SEC = 10
wlan=None
s=None

def initializeNetwork():
  print("Initializing network ...")
  if(connectWifi(config.config["ssid"],config.config["password"])):
    print("WIFI !")
    config.status["network"] = "wifi 📶"
  else:
    print("HOTSPOT !")
    config.status["network"] = "hotspot 🖧"
    createHotspot(AP_SSID,AP_PASSWORD)

def connectWifi(ssid,passwd):
  global wlan
  try:
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)

    wait_cycle = 0
    while(wlan.ifconfig()[0]=='0.0.0.0'):
      time.sleep(1)
      wait_cycle = wait_cycle + 1
      if wait_cycle >= MAX_WAIT_SEC:
        return False
    print(wlan.ifconfig())
    return True
  except:
    return False

def closeWifi():
  if (s):
    s.close()
  wlan.disconnect()
  wlan.active(False)

def createHotspot(ssid,password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while not ap.active():
        pass
    print('network config:', ap.ifconfig())